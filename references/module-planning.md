# Module Planning

## Rule

For every system request, plan 8-10 first-level modules before generating code, UI, screenshots, or documents.

Do not plan fewer than 8 or more than 10 first-level modules unless the user explicitly requests a different count.

## Required flow

1. Extract the system name, roles, and domain clues from the user's brief.
2. Draft 8-10 first-level modules.
3. Balance the list so it includes both domain-specific modules and supporting modules.
4. Reuse the module list as the structural backbone for:
   - full-stack code folders and APIs
   - pure frontend navigation and pages
   - screenshot targets
   - agreement/manual wording when relevant
5. Mention the final module count and selected module names in the final summary.

## Module composition guidance

Prefer this shape:

- 5-7 domain-specific modules
- 2-3 supporting modules such as dashboard, reports, notifications, workflow, settings, permissions, or logs

Avoid padding with weak duplicates. Each first-level module should represent a real navigation group or business area.

## Common support modules

Use these when the brief is short and you need to reach 8-10 modules naturally:

- 仪表盘
- 基础资料
- 核心业务管理
- 流程审批
- 统计报表
- 消息通知
- 系统配置
- 权限与角色
- 日志审计

## Example planning pattern

For a student information system, a solid 8-module plan could be:

1. 仪表盘
2. 学生档案
3. 班级管理
4. 课程管理
5. 成绩管理
6. 考勤管理
7. 统计报表
8. 系统设置

For a larger brief, extend to 9 or 10 modules by adding items such as 家校沟通, 预警中心, 权限角色, or 日志审计.

## Guardrails

- Keep module names stable after planning them.
- Do not let the frontend use one module map while the backend uses another.
- Do not collapse everything into generic pages like list/detail/settings if the module plan is richer than that.
- If the user names required modules, preserve them and fill the remaining slots up to 8-10 with reasonable supporting modules.
