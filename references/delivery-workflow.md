# Delivery Workflow

## Checklist

1. Extract the system name and user roles from the brief.
2. Plan 8-10 first-level modules and keep that module map stable.
3. Create the output tree with `scripts/prepare_output_tree.py`.
4. Save the module list to `<system-folder>/docs/Template/module-plan.md`.
5. Build the full-stack code pack under `<system-folder>/code/` from the module map.
6. Run `scripts/validate_fullstack_code.py` and fix the code pack if validation fails.
7. Choose one layout archetype from the 10 fixed options, then build the runnable frontend demo under `<system-folder>/demo/` from the same module map.
8. Run `scripts/validate_frontend_demo.py` and fix the demo if the static validation fails.
9. Run `scripts/validate_frontend_build.py`, then build the demo.
10. Start a preview or static server from the built output and run `scripts/validate_frontend_routes.py`.
11. Capture Playwright screenshots from the validated preview into `<system-folder>/photos/`.
12. Generate `<system-name>合作开发协议.docx` with `scripts/build_agreement_docx.py`, using the user-supplied party count or 3 parties by default.
13. Read `references/manual-docx-spec.md` and generate the manual outline with `scripts/build_manual_outline.py`.
14. Have the current agent fill `manual-content.json` directly with natural Chinese content for 用途、功能 and every screenshot description.
15. Run `scripts/build_manual_docx.py` to convert the manual draft into the final formatted `.docx` in `<system-folder>/docs/`.
16. Run `scripts/build_code_docx.py` to invoke the installed `codeclean` CLI and generate `<system-name>代码源程序V1.0.docx` in `<system-folder>/docs/`.
17. Report assumptions, selected ui prompt, selected layout archetype, final module count, saved paths, and any missing validations.

## Full-stack code pack rules

- Let the planned 8-10 modules shape the routers, services, entities, and frontend pages inside the code pack.
- Prefer coherent structure over execution proof.
- Include representative database tables, API endpoints, service layers, and screens.
- Do not skip `code/frontend`; it must contain a React + TypeScript source tree with module-specific pages or components.
- Do not generate a small placeholder code pack. The pack must include frontend, backend, and database files with enough breadth for a handoff.
- `code/frontend/src/modules`, `code/backend/app/routers`, and SQL `CREATE TABLE` statements must cover every planned first-level module.
- Minimum validation thresholds are enforced by `scripts/validate_fullstack_code.py`: at least 45 counted source files, 1300 nonblank source lines, 18 frontend source files, 18 backend Python files, 2 SQL files, and module coverage across frontend/backend/database.
- Treat a failed full-stack code validation as blocking. Do not create the demo, screenshots, documents, or code-source `.docx` until it passes.
- Leave integration seams as TODO comments only when necessary.
- Do not spend the majority of the task on dependency fixes, environment debugging, or tests.

## Runnable frontend rules

- Reflect the planned 8-10 modules in the navigation and page map.
- Make this deliverable actually startable when feasible.
- Prefer mocked data over incomplete backend coupling.
- Include navigation and the main business loop needed for screenshots.
- Keep the visuals intentional enough for a handoff screenshot pack.
- Choose a layout archetype from the 10 fixed options before implementation and let it materially change the shell.
- Do not default to the same left-sidebar workspace across unrelated prompts and systems.
- Ensure the demo passes `scripts/validate_frontend_demo.py` before treating it as ready for launch.
- Ensure the demo passes `scripts/validate_frontend_build.py` before trying to use a build-first screenshot workflow.
- Keep mock records consistent between primary pages and their secondary pages such as detail, edit, and drill-down views.
- Prefer a shared source of mock truth per module so the same entity appears coherently in list and detail states.

## Screenshot rules

- Never start Playwright screenshots if the static frontend validation fails.
- Prefer screenshots from a built preview or static server instead of a dev server.
- Run route smoke checks before opening Playwright on the target pages.
- Use Playwright, not manual screenshots.
- Wait for the page to settle before capturing.
- Favor full-page screenshots only when it helps readability; otherwise use viewport captures with consistent dimensions.
- Capture the highest-value pages first: login or landing, dashboard, the most important module pages, record detail, create or edit flow, analytics or settings if present.
- If a secondary page is not backed by a real record from the related primary page, skip that screenshot instead of capturing a disconnected view.
- Prefer a smaller but consistent screenshot set over a larger set with fake or broken detail pages.

## Agreement rules

- Prefer `scripts/build_agreement_docx.py` for the cooperation development agreement.
- Default to 3 parties when the user does not say how many people participate.
- Party labels follow the count: 3 uses 甲、乙、丙; 4 uses 甲、乙、丙、丁.
- The first party is fixed as `甲方：孔祥鑫` and `身份证号：140522200002262315`; subsequent party fields stay blank unless supplied by the user.
- The final filename is `<system-name>合作开发协议.docx` in `<system-folder>/docs/`.
- The title must be `合作开发协议`, 宋体 一号, centered. Body must be 宋体 小四, first-line indent 2 characters, single line spacing.
- Use `<system-name>平台软件` as the project software name unless the system name already ends with `平台软件`, `系统软件`, or `软件`.
- Convert all party-count wording consistently, including `甲、乙、丙三方` and `一式 n+1 份`.
- If the user does not provide an agreement date, use the current date minus one calendar month, for example 2026 年 5 月 24 日 becomes `2026 年 4 月 24 日`.

## Manual rules

- Base the manual on the actual screenshots, not on imagined pages.
- Follow `references/manual-docx-spec.md` as the default page structure for Chinese manuals.
- Describe each page in terms of user goal, main information, primary actions, and the module it belongs to.
- Use one screenshot subsection per page in section `五、软件使用`.
- Keep figure captions below images and center them.
- Use real generated languages with version numbers when filling the development-language fields.
- Prefer `scripts/build_manual_docx.py` as the default final manual generator.
- The current agent must fill the final copy before DOCX generation; do not rely on canned fallback paragraphs for 用途、功能 or screenshot descriptions.
- Explain major workflows in business order.
- Mention demo assumptions such as mock data, omitted integrations, or simplified permissions.
- After the manual `.docx` is complete, run the code-cleaning CLI to produce the cleaned code-source `.docx` and place it in `<system-folder>/docs/`.
