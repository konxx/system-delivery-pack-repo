# Delivery Workflow

## Checklist

1. Extract the system name and user roles, then ask once for document dates, technical style, and technical highlights unless already supplied.
2. If the user does not answer and later asks to continue, use the documented defaults without asking again. Plan 8-10 first-level modules and keep that module map stable.
3. Create the output tree with `scripts/prepare_output_tree.py` and record the resolved intake preferences in `delivery-manifest.json`.
4. Save the module list to `<system-folder>/docs/Template/module-plan.md`.
5. Build the full-stack code pack under `<system-folder>/code/` from the module map.
6. Run `scripts/validate_fullstack_code.py` and fix the code pack if validation fails.
7. Choose one layout archetype from the 10 fixed options, then build the runnable frontend demo under `<system-folder>/demo/` from the same module map.
8. Run `scripts/validate_frontend_demo.py` and fix the demo if the static validation fails.
9. If dependencies are missing, install packages only with domestic mirrors, then run `scripts/validate_frontend_build.py` and build the demo.
10. Start a preview or static server from the built output and run `scripts/validate_frontend_routes.py`.
11. Capture Playwright screenshots from the validated preview into `<system-folder>/photos/`.
12. Generate `<system-name>合作开发协议.docx` with `scripts/build_agreement_docx.py`; the agreement is fixed to 甲乙双方.
13. Read `references/manual-docx-spec.md` and generate the manual outline with `scripts/build_manual_outline.py`.
14. Read `references/manual-humanize-style.md`.
15. Have the current agent fill `manual-content.json` directly with natural Chinese content for 用途、功能 and every screenshot description.
16. Run `scripts/polish_manual_content.py --root <workspace> --system-name "<system name>"`; if it reports errors, revise `manual-content.json` and rerun it.
17. Run `scripts/build_manual_docx.py` to convert the manual draft into the final formatted `.docx` in `<system-folder>/docs/`.
18. Run `scripts/build_code_docx.py` to invoke the installed `codeclean` CLI and generate `<system-name>代码源程序V1.0.docx` in `<system-folder>/docs/`.
19. Confirm `<system-folder>/docs/` has been cleaned and contains only the cooperation agreement, system manual, and code-source DOCX.
20. Report assumptions, selected ui prompt, selected layout archetype, final module count, saved paths, and any missing validations.

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
- Never use the agreement party or manual author in source, comments, tests, SQL seeds, configuration, filenames, or mock data. Generate fictional identities instead.
- Treat protected-identity findings from `scripts/validate_fullstack_code.py` as blocking errors.

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
- Use only fictional people in mock data; do not reuse any identity from the agreement or manual.
- Treat protected-identity findings from `scripts/validate_frontend_demo.py` as blocking errors.
- When installing frontend packages, use `npm install --registry=https://registry.npmmirror.com`, `npm ci --registry=https://registry.npmmirror.com`, or `pnpm install --registry=https://registry.npmmirror.com`.
- When running package-backed tooling through npx, use `npx --registry=https://registry.npmmirror.com ...`.

## Screenshot rules

- Never start Playwright screenshots if the static frontend validation fails.
- Prefer screenshots from a built preview or static server instead of a dev server.
- Run route smoke checks before opening Playwright on the target pages.
- Use Playwright, not manual screenshots.
- Wait for the page to settle before capturing.
- Run `python scripts/verify_local_playwright.py` before screenshots.
- Capture routes with `python scripts/capture_screenshots.py`; use the machine-level Python Playwright and cached Chromium.
- Do not install or update Playwright packages or browsers during a delivery run. If local verification fails, stop the screenshot stage and report the missing machine prerequisite.
- Favor full-page screenshots only when it helps readability; otherwise use viewport captures with consistent dimensions.
- Capture the highest-value pages first: login or landing, dashboard, the most important module pages, record detail, create or edit flow, analytics or settings if present.
- If a secondary page is not backed by a real record from the related primary page, skip that screenshot instead of capturing a disconnected view.
- Prefer a smaller but consistent screenshot set over a larger set with fake or broken detail pages.

## Agreement rules

- Prefer `scripts/build_agreement_docx.py` for the cooperation development agreement.
- The cooperation agreement is fixed to two parties: 甲方 and 乙方.
- Do not generate 丙方 or any larger party count unless the user explicitly asks to redesign the agreement template.
- Load the fixed 甲方 name and ID only from `assets/agreement-template.md`; subsequent party fields stay blank unless supplied by the user.
- The final filename is `<system-name>合作开发协议.docx` in `<system-folder>/docs/`.
- The title must be `合作开发协议`, 宋体 一号, centered. Body must be 宋体 小四, first-line indent 2 characters, single line spacing.
- Use the system name directly as the project software name. Do not append `平台软件`.
- Use two-party wording throughout: `甲乙双方`, `对方`, `另一方`, and `双方`.
- Use the intake date recorded in `delivery-manifest.json`; default to `2026年4月15日` when no date was supplied.

## Manual rules

- Base the manual on the actual screenshots, not on imagined pages.
- Follow `references/manual-docx-spec.md` as the default page structure for Chinese manuals.
- Describe each page in terms of user goal, main information, primary actions, and the module it belongs to.
- Use one screenshot subsection per page in section `五、软件使用`.
- Keep figure captions below images and center them.
- Use real generated languages with version numbers when filling the development-language fields.
- Prefer `scripts/build_manual_docx.py` as the default final manual generator.
- The current agent must fill the final copy before DOCX generation; do not rely on canned fallback paragraphs for 用途、功能 or screenshot descriptions.
- Before building the DOCX, read `references/manual-humanize-style.md` and run `scripts/polish_manual_content.py`. Do not use an external AI/API to polish manual copy.
- Treat errors from `polish_manual_content.py` as blocking. Revise `manual-content.json` until the report has no errors.
- The manual must have no header on the cover page. Every page after the cover page must have a header with `<system-name>V1.0` on the left and `PAGE/NUMPAGES` page numbering shown as `X/Y` on the right, using 宋体 for Chinese text, Times New Roman for English text, and 小五 font size.
- Explain major workflows in business order.
- Mention demo assumptions such as mock data, omitted integrations, or simplified permissions.
- After the manual `.docx` is complete, run the code-cleaning CLI to produce the cleaned code-source `.docx` and place it in `<system-folder>/docs/`.
- After the code-source `.docx` is complete, remove `<system-folder>/docs/Template/` and any other non-final working files from `<system-folder>/docs/`. Final `docs` must contain only `<system-name>合作开发协议.docx`, `<system-name>-系统说明书.docx`, and `<system-name>代码源程序V1.0.docx`.
