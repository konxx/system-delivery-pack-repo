# Manual Humanize Style

Use this guide after `manual-content.json` is filled and before building the final manual DOCX.

## Rule

Polish the Chinese manual copy locally. Do not call OpenAI, Opencode, Claude, or any external AI/API service. The workflow borrows the two-pass editing idea from `poleHansen/baibaiAIGC`: first make the copy concrete and natural, then do a cleanup pass for boilerplate and repetition.

## Pass 1: Natural Rewrite

- Preserve factual content: system name, module names, roles, screenshots, actions, version, dates, author, tech stack, and figure order must not change.
- Write like a product handoff note, not a marketing page.
- Prefer concrete screen/action words: `查看`, `筛选`, `新增`, `编辑`, `审核`, `导出`, `统计`, `配置`, `查看详情`.
- Give each screenshot paragraph a concrete page purpose and one or two key visible items or actions. Mention its module or user role only when that context is useful.
- Keep `二、软件用途` and `三、软件功能` within about 200 Chinese characters each.
- Keep each `五、软件使用` screenshot paragraph within 80-120 Chinese characters. Prefer two or three plain sentences; do not use a one-line caption or pad the paragraph with generic background.

## Pass 2: Cleanup

- Remove or rewrite generic AI-style phrases such as `本系统旨在`, `赋能`, `一站式`, `智能化`, `数字化转型`, `全面提升`, `显著提升`, `高效便捷`, `全方位`, `多维度`, `闭环管理`, `极大地`, `从而实现`.
- Avoid repeated sentence frames such as `通过...实现...`, `系统提供了...功能`, `用户可以方便地...`.
- Replace broad claims with observable behavior. For example, write what the page lets the user check or operate instead of saying it “全面提升管理效率”.
- Use short and medium sentences together. Do not make every sentence start with `系统` or `页面`.
- Keep technical stack wording consistent with the generated code. The default database is PostgreSQL.

## Required Check

Run:

```powershell
python scripts/polish_manual_content.py --root <workspace> --system-name "<system name>"
```

If the script reports errors, revise `manual-content.json` and rerun it before `scripts/build_manual_docx.py`.
