"""复刻 OpenCode 1.18.25 的权限判定语义，检验 agent 配置的实际拦截效果。

来源（app.asar -> out/main/chunks/node-BBwF64dM.js，静态提取）:

    function permissions(info, tools) {            // frontmatter 的 permission ->
        ... typeof rule === "string" ->
            rules.push({ action, resource: "*", effect: rule })
        ... 对象形式 rule ->
            rules.push(...Object.entries(rule).map(([resource, effect]) => ({action, resource, effect})))
    }

    function evaluate2(action, resource, ...rulesets) {   // 多条规则 -> 一条
        return rulesets.flat().findLast(rule =>
            wildcard.match(action, rule.action) && wildcard.match(resource, rule.resource)
        ) ?? { action, resource: "*", effect: "ask" }
    }

    function denied(input, rules) {         // 多资源任一 deny -> 整体 deny
        return input.resources.some(r => evaluate2(input.action, r, rules).effect === "deny")
    }

    PermissionV2.assert: effect === "deny" -> 抛 BlockedError（短路，后续写盘不执行）
                         effect === "allow" -> 放行
                         其它            -> 弹窗等用户

本脚本只复刻判定函数，用于回答「某条配置会不会真的拦住某次调用」。
"""

from __future__ import annotations

import fnmatch

DEFAULT_EFFECT = "ask"


def normalize_action(action: str) -> str:
    return "edit" if action in ("write", "patch") else action


def permissions(conf: dict | None) -> list[dict]:
    """把 frontmatter 的 permission 映射成规则数组（保序）。"""
    rules: list[dict] = []
    for action, rule in (conf or {}).items():
        if not rule:
            continue
        if isinstance(rule, str):
            rules.append({"action": action, "resource": "*", "effect": rule})
        else:
            for resource, effect in rule.items():
                rules.append({"action": action, "resource": resource, "effect": effect})
    return rules


def match(value: str, pattern: str) -> bool:
    if pattern == "*":
        return True
    if "*" in pattern or "?" in pattern:
        return fnmatch.fnmatchcase(value, pattern)
    return value == pattern


def evaluate(action: str, resource: str, rules: list[dict]) -> dict:
    hit = None
    for rule in rules:
        if match(action, rule["action"]) and match(resource, rule["resource"]):
            hit = rule
    return hit or {"action": action, "resource": "*", "effect": DEFAULT_EFFECT}


def decide(action: str, resources: list[str], rules: list[dict]) -> str:
    effects = [evaluate(action, r, rules)["effect"] for r in resources]
    if "deny" in effects:
        return "deny"
    if "ask" in effects:
        return "ask"
    return "allow"


# ---------------------------------------------------------------- 真实配置
DEFAULT_RULES = [
    {"action": "*", "resource": "*", "effect": "allow"},
    {"action": "external_directory", "resource": "*", "effect": "ask"},
    {"action": "read", "resource": "*", "effect": "allow"},
]

CODE_REVIEWER = permissions({
    "edit": "deny",
    "task": "deny",
    "bash": {"*": "deny", "git status*": "allow", "git diff*": "allow"},
    "webfetch": "deny",
    "websearch": "deny",
    "external_directory": "deny",
})

ORCHESTRATOR = permissions({
    "edit": {"*": "deny", "reports/*.md": "allow"},
    "task": {"*": "deny", "implementer-add": "allow", "test-runner": "allow"},
    "bash": {"*": "ask", "python -m unittest*": "allow", "git status*": "allow"},
})

NO_PERMISSION = permissions(None)

CASES = [
    ("code-reviewer", "改综述稿正文", "edit", ["notes/文献综述_初稿_v1.md"], CODE_REVIEWER, "deny"),
    ("code-reviewer", "改自己的报告", "edit", ["notes/核验报告.md"], CODE_REVIEWER, "deny"),
    ("code-reviewer", "看 git 状态", "bash", ["git status --short"], CODE_REVIEWER, "allow"),
    ("code-reviewer", "看 git diff", "bash", ["git diff HEAD"], CODE_REVIEWER, "allow"),
    ("code-reviewer", "用 shell 重定向写文件", "bash", ["echo hacked > notes/稿.md"], CODE_REVIEWER, "deny"),
    ("code-reviewer", "跑 python 改文件", "bash", ["python -c open('x','w')"], CODE_REVIEWER, "deny"),
    ("orchestrator", "写运行报告", "edit", ["reports/phase2-run.md"], ORCHESTRATOR, "allow"),
    ("orchestrator", "改综述稿", "edit", ["notes/文献综述_初稿_v1.md"], ORCHESTRATOR, "deny"),
    ("orchestrator", "跑测试", "bash", ["python -m unittest discover"], ORCHESTRATOR, "allow"),
    ("orchestrator", "装包", "bash", ["pip install requests"], ORCHESTRATOR, "ask"),
    # 关键：不写 permission 不等于安全。内置 defaults 第一条是
    # {action:"*", resource:"*", effect:"allow"}，未命中任何自定义规则时就是放行。
    ("未配置权限", "改任意文件", "edit", ["notes/稿.md"], NO_PERMISSION, "allow"),
]


def main() -> int:
    print(f"{'角色':<14}{'场景':<24}{'动作':<7}{'判定':<7}{'预期':<7}结果")
    print("-" * 78)
    bad = 0
    for who, desc, action, resources, rules, want in CASES:
        got = decide(action, resources, DEFAULT_RULES + rules)
        ok = "OK" if got == want else "MISMATCH"
        if got != want:
            bad += 1
        print(f"{who:<14}{desc:<24}{action:<7}{got:<7}{want:<7}{ok}")
    print("-" * 78)
    print(f"{len(CASES) - bad}/{len(CASES)} 与预期一致")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
