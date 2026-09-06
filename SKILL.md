---
name: ruanzhu
description: Generate complete system delivery packs from prompts such as "生成仓储管理系统", "生成 CRM 系统", or "build an ERP system". Use when Codex needs to (1) plan 8-10 first-level system modules from the user's brief, (2) write non-validated full-stack source code with React, TypeScript, Python, and PostgreSQL under the system folder code directory based on those modules, (3) build a runnable frontend demo under the system folder demo directory by first choosing exactly one bundled design prompt from ui_prompt/ (30 styles) and mapping the same modules into the UI, (4) capture Playwright screenshots under the system folder photos directory, (5) create the cooperation development agreement and manual .docx files under the system folder docs directory while using docs/Template only as a temporary working area, and (6) generate a cleaned code-source .docx from the system folder code directory with the installed `codeclean` CLI after the manual is delivered, then clean docs so only the three final DOCX files remain.
---

# Ruanzhu

## Overview

Generate a fixed set of project deliverables for a named system. Favor completeness, stable paths, and believable artifacts over production hardening.

## Default stack

- Use React + TypeScript for frontend code.
- Use Python for backend code. Prefer FastAPI unless the user asks for something else.
- Use PostgreSQL for schema design and sample SQL.
- Use a runnable Vite + React + TypeScript app for the pure-frontend deliverable.
- Use Playwright for screenshots.
- Use DOCX for the agreement and the manual.

## Quick start

1. Extract the system name and primary user roles, then complete the required intake question for dates, technical style, and technical highlights. The cooperation agreement is fixed to two parties: 甲方 and 乙方.
2. Read [references/module-planning.md](references/module-planning.md) and plan 8-10 first-level modules before writing any deliverable.
3. Run `scripts/prepare_output_tree.py --root <workspace> --system-name "<system name>"` with the resolved intake preferences.
4. Read [references/output-spec.md](references/output-spec.md) before writing files.
5. Read [references/ui-prompt-selection.md](references/ui-prompt-selection.md) before creating the pure-frontend deliverable.
6. Read [references/layout-archetypes.md](references/layout-archetypes.md) before deciding the frontend information architecture.
7. Read [references/manual-docx-spec.md](references/manual-docx-spec.md) before generating the product manual `.docx`.
8. Read [references/manual-humanize-style.md](references/manual-humanize-style.md) before filling manual copy.
9. Read [references/delivery-workflow.md](references/delivery-workflow.md) before creating screenshots or documents.

## Output contract

Write the deliverables to these locations:

- `<system-folder>/code/`: full-stack source tree. This code does not need to be proven runnable.
- `<system-folder>/demo/`: runnable pure-frontend demo app.
- `<system-folder>/photos/`: Playwright screenshots of the main screens and flows.
- `<system-folder>/docs/`: final agreement, manual, and code-source `.docx` files.
- `<system-folder>/docs/Template/`: temporary working area for copied templates, fallback seed templates, outlines, manifests, and draft files. This folder must be removed before final delivery.

Do not move these deliverables to other top-level folders unless the user explicitly asks.

## Required intake gate

Before generating files, ask one concise grouped question for the following information unless the user already supplied it:

- Document dates: allow one shared date or separate agreement and manual revision dates.
- Technical style: stack, architecture, interaction, or visual direction the user prefers.
- Technical highlights: the capabilities or engineering strengths that should be emphasized.

Use a direct prompt such as: `请补充本次交付的日期（可分别指定协议和说明书日期）、技术风格、技术亮点；不回复时我将按默认配置继续。`

Ask once. If the user does not answer and later says to continue, proceed without asking again. Use these defaults when no answer is available:

- Agreement date: `2026年4月15日`.
- Manual revision date: `2026-6-15`.
- Technical style: React + TypeScript, FastAPI, PostgreSQL, plus one bundled UI prompt and one layout archetype.
- Technical highlights: choose three domain-appropriate highlights; the generic fallback is modular full-stack architecture, role-based access with audit trails, and visual business analytics.

If the user supplies one date only, apply it to both the agreement and manual. Record the resolved values by passing `--document-date`, `--agreement-date`, `--manual-date`, `--technical-style`, and repeated `--technical-highlight` options to `scripts/prepare_output_tree.py`. Treat `delivery-manifest.json` as the downstream source of truth.

## Domestic package mirror rule

Use domestic mirrors for every package installation or temporary package execution step.

- For Python packages, run `python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple <packages>`.
- For Node package installation with npm, run `npm install --registry=https://registry.npmmirror.com` or `npm ci --registry=https://registry.npmmirror.com`.
- For temporary package execution, run `npx --registry=https://registry.npmmirror.com <package> ...`.
- For Node package installation with pnpm, run `pnpm install --registry=https://registry.npmmirror.com`.
- Playwright is a machine-level prerequisite and must not be installed or updated during a delivery run.
- Do not run package install or package-execution commands without an explicit domestic mirror unless the workspace already has an equivalent local registry configuration.

## Local Playwright rule

- Run `python scripts/verify_local_playwright.py` before starting the preview server or screenshots.
- Use `python scripts/capture_screenshots.py` for route screenshots. This script calls the machine-level Python Playwright and cached Chromium directly.
- Do not add Playwright to the demo's `package.json`, run `npm install playwright`, use `npx playwright`, or run `playwright install` as part of a delivery.
- If verification fails, stop the screenshot stage and report that the machine-level prerequisite needs repair outside the current delivery. Do not silently download a replacement.

## Workflow

### 1. Normalize the brief and lock the module plan

- Complete the required intake gate before creating files. Reuse answers already present in the conversation instead of asking duplicate questions.
- Infer reasonable defaults when the user gives only a short prompt like `生成进销存系统`.
- Match the user's language. For Chinese prompts, write the agreement and manual in Chinese.
- Keep a short assumptions list and report it after the work is complete.
- Plan 8-10 first-level modules before generating code, UI, screenshots, or documents.
- Do not plan fewer than 8 or more than 10 first-level modules unless the user explicitly asks for a different count.
- Make the module plan drive the frontend navigation, backend routers, service boundaries, database tables, screenshot targets, and document sections.
- Save the module list to `<system-folder>/docs/Template/module-plan.md`; downstream validation treats this file as required.

### 2. Prepare the output tree

- Run `scripts/prepare_output_tree.py` first so the folder contract is created consistently.
- Pass the resolved intake preferences so `delivery-manifest.json` records both document dates, technical style, and technical highlights.
- Let the script copy fallback template seeds from `assets/` into `<system-folder>/docs/Template/`.
- If the user supplied a template file, copy that template into `<system-folder>/docs/Template/` before editing it. Do not modify the original in place.

### 3. Create the full-stack code pack

- Place the full-stack deliverable under `<system-folder>/code/`.
- Build the code structure from the planned 8-10 modules rather than from generic placeholder sections.
- Use a realistic structure with frontend, backend, API contracts, SQL or schema files, and setup notes.
- Do not skip the full-stack frontend. `<system-folder>/code/frontend/` must contain a React + TypeScript source tree with `package.json`, `src/`, an entry file, and module-specific pages/components.
- Do not create a token placeholder code pack. `<system-folder>/code/backend/` must contain FastAPI-style app code with module routers, services or models, and representative API behavior.
- `<system-folder>/code/database/` must contain SQL schema and seed/sample data files.
- The full-stack code pack must cover every planned first-level module in frontend module folders, backend routers, and database tables.
- Minimum code-pack breadth before validation: at least 45 counted source files, 1300 nonblank source lines, 18 frontend source files, 18 backend Python files, 2 SQL files, and at least one frontend module directory, backend router, and `CREATE TABLE` statement for each planned module.
- Run `scripts/validate_fullstack_code.py --root <workspace> --system-name "<system name>"` immediately after writing `<system-folder>/code/`.
- If full-stack validation fails, fix the code pack before creating the demo, screenshots, agreement, manual, or code-source `.docx`.
- Do not spend time proving this code runs unless the user explicitly asks for that extra validation.
- Prefer breadth and coherence: routes, components, models, services, database schema, and representative pages should all exist for the planned modules.
- Use clear TODO comments only where integration details are intentionally omitted.
- Never place the fixed agreement/manual identity in full-stack source, comments, sample configuration, SQL seeds, tests, filenames, or mock data. Invent fictional people for all examples.
- Treat identity findings from `scripts/validate_fullstack_code.py` as blocking errors.

### 4. Create the runnable frontend demo

- Place the runnable demo under `<system-folder>/demo/`.
- Before writing UI code, inspect `ui_prompt/manifest.json` and choose exactly one style prompt from the 30 bundled options.
- If the user does not explicitly name a style, choose one prompt randomly from the 30 bundled options.
- After choosing the style, read only the selected `ui_prompt/<slug>/prompt.xml` and use it as the primary visual direction for the pure frontend deliverable.
- Before writing page structure, choose exactly one primary layout archetype from the 10 fixed options in [references/layout-archetypes.md](references/layout-archetypes.md).
- If the user does not explicitly name a layout archetype, randomly choose one from the 10 fixed options.
- Do not mix multiple ui prompts unless the user explicitly asks for a hybrid style.
- Map the planned 8-10 modules into the navigation, page structure, cards, tables, forms, and charts of the runnable frontend demo.
- Do not default to the same `left sidebar + right content` admin shell for every system.
- Use left-sidebar navigation only when the chosen layout archetype is explicitly `3. 左侧导航栏，右侧内容`.
- Let the chosen layout archetype affect navigation placement, module entry points, detail-page composition, and dashboard structure instead of changing only colors.
- Make this deliverable runnable with a normal React + TypeScript frontend toolchain. Prefer a Vite layout.
- Use mocked data, local state, or static JSON when backend integration would slow delivery.
- Invent fictional mock identities. Never reuse the cooperation-agreement party or manual author in demo code, UI labels, screenshots, comments, or data files.
- Include the main screens implied by the 8-10 module plan: dashboard plus the module-specific list, detail, form, workflow, analytics, settings, or other screens as needed.
- When the demo includes secondary pages such as detail, edit, or drill-down views, keep their mock data linked to the primary list data through the same record IDs or keys.
- Prefer a single shared mock dataset per module so list pages, detail pages, and forms refer to the same entities instead of unrelated placeholders.
- Keep the UI visually intentional. Do not default to an unstyled placeholder interface.
- Run `scripts/validate_frontend_demo.py --root <workspace> --system-name "<system name>"` before any launch or screenshot step.
- Run `scripts/validate_frontend_build.py --root <workspace> --system-name "<system name>"` before using any build-first screenshot workflow.
- If the static validation fails, fix the frontend structure first. Do not continue to Playwright screenshots with a broken or incomplete demo.
- Treat identity findings from `scripts/validate_frontend_demo.py` as blocking errors.

### 5. Capture Playwright screenshots

- Do not launch Playwright until `scripts/validate_frontend_demo.py` passes for the demo folder.
- Prefer a build-first screenshot workflow: install dependencies, run the frontend build, start a preview or static server from the built output, validate routes, then use Playwright as the final capture tool.
- Run `scripts/validate_frontend_build.py` before building, and run `scripts/validate_frontend_routes.py` against the preview server before taking screenshots.
- Prefer screenshotting the built preview over screenshotting the dev server whenever feasible.
- Launch the validated preview and use Playwright to capture the major screens.
- Capture only screens that actually exist in the demo and prioritize the highest-value pages from the module plan.
- If a secondary page such as a product detail page, student detail page, or order drill-down does not have data that matches an actual record from the primary page, do not screenshot that secondary page.
- Prefer skipping an inconsistent secondary page over capturing a broken or disconnected detail view.
- Prefer a stable naming pattern such as `01-login.png`, `02-dashboard.png`, `03-list.png`, `04-detail.png`, `05-form.png`.
- Save all screenshots to `<system-folder>/photos/`.
- Run `python scripts/verify_local_playwright.py`, then call `python scripts/capture_screenshots.py --base-url <preview-url> --output-dir <system-folder>/photos --page <filename>=<route> ...`.
- Never install a Playwright package or browser during this stage. If the local verification fails, report the missing machine prerequisite and stop this stage.

### 6. Create the cooperation development agreement

- Put the final agreement `.docx` in `<system-folder>/docs/` as `<system-name>合作开发协议.docx`.
- The agreement is fixed to two parties: 甲方 and 乙方. Do not generate 丙方 or any multi-party wording.
- Generate the agreement with `scripts/build_agreement_docx.py --root <workspace> --system-name "<system name>"`.
- Use the agreement date recorded in `delivery-manifest.json`; default to `2026年4月15日` only when the user gave no date.
- Use the system name directly as the project software name. Do not append `平台软件`.
- The generated DOCX must use title `合作开发协议`, 宋体 一号, centered. Body text must use 宋体 小四, first-line indent 2 characters, single line spacing.
- Load the fixed 甲方 name and ID only from `assets/agreement-template.md`; do not duplicate that identity in source code or mock data. 乙方 name and ID remain blank unless the user provides them.
- Keep the working draft in `<system-folder>/docs/Template/` during generation and the final `.docx` in `<system-folder>/docs/`. The Template folder is temporary and must not remain in the delivered `docs` folder.

### 7. Create the system manual

- Put the final manual `.docx` in `<system-folder>/docs/`.
- Base it on the actual screenshots in `<system-folder>/photos/` plus concise explanatory text.
- Read [references/manual-docx-spec.md](references/manual-docx-spec.md) first and follow it as the default Chinese manual structure.
- Use `C:\Program Files\Pandoc\pandoc.exe` as the default draft conversion path when Pandoc is needed.
- Run `scripts/build_manual_outline.py --root <workspace> --system-name "<system name>"` after screenshots are ready to scaffold the manual draft.
- Run `scripts/build_manual_docx.py --root <workspace> --system-name "<system name>"` to produce the final formatted manual `.docx`.
- Use the manual revision date recorded in `delivery-manifest.json`; default to `2026-6-15` only when the user gave no date.
- Before running `build_manual_docx.py`, the current agent must directly fill the blank fields in `manual-content.json`.
- Fill natural Chinese copy for:
  - `short_name`
  - `purpose_text`
  - `function_text`
  - `development_environment_text`
  - each `screenshot_sections[].title`
  - each `screenshot_sections[].description_text`
- The language must be concise, natural, and specific to the system. Do not leave templated placeholders or generic canned text.
- Focus each screenshot note on the page purpose and one or two salient actions or visible items. Mention the user role or module only when it makes the description clearer.
- In section `五、软件使用`, place one screenshot subsection per page with a short, natural paragraph of 80-120 Chinese characters. Use two or three sentences; do not pad the text with repeated context or generic claims.
- Before writing final manual copy, read [references/manual-humanize-style.md](references/manual-humanize-style.md). Use the local two-pass workflow to remove generic AI-style wording while preserving facts, modules, screenshots, and stack details.
- Run `scripts/polish_manual_content.py --root <workspace> --system-name "<system name>"` after filling `manual-content.json`. If it reports errors, revise the JSON and rerun the script before `build_manual_docx.py`.
- Do not use any external AI/API service to polish or generate manual copy.
- Keep the cover page, revision table, runtime tables, and figure captions consistent with the manual docx spec.
- The manual must have no header on the cover page. Every page after the cover page must have a header with `<system-name>V1.0` on the left and `PAGE/NUMPAGES` page numbering shown as `X/Y` on the right, using 宋体 for Chinese text, Times New Roman for English text, and 小五 font size.
- If no user-provided manual template exists, start from `assets/manual-template.md`, copy it into `<system-folder>/docs/Template/`, and convert the filled result into `.docx`.

### 8. Create the code source document

- After the system manual `.docx` is finished, run `scripts/build_code_docx.py --root <workspace> --system-name "<system name>"` to invoke the installed `codeclean` CLI on `<system-folder>/code/`.
- Save the final cleaned code-source document in `<system-folder>/docs/` as `<system-name>代码源程序V1.0.docx`.
- Keep the output in `<system-folder>/docs/`, not in `<system-folder>/docs/Template/`.
- `scripts/build_code_docx.py` cleans `<system-folder>/docs/` after successful code-source generation. Final delivery must contain only these three files:
  - `<system-name>合作开发协议.docx`
  - `<system-name>-系统说明书.docx`
  - `<system-name>代码源程序V1.0.docx`

## Module planning rule

Treat module planning as a mandatory upstream step:

- Always plan 8-10 first-level modules from the user's system brief before generating any deliverable.
- Keep the modules at the same hierarchy level. Do not count subfeatures as separate first-level modules just to reach the target.
- Prefer a mix of domain modules and supporting modules so the system feels complete.
- Reuse the same module names across code folders, frontend navigation, screenshot labels, and document sections whenever practical.
- If the brief is too small, expand with reasonable supporting modules instead of dropping below 8.
- Mention the final module count in the completion summary.

## Cooperation agreement rule

- Use `scripts/build_agreement_docx.py` as the default agreement generator; do not hand-build the agreement unless the script is unavailable.
- The agreement template is fixed to 甲乙双方. Reject or ignore requests to generate 丙方 or any larger party count unless the user explicitly asks to redesign the template.
- Use two-party wording throughout: `甲乙双方`, `对方`, `另一方`, and `双方`. Do not leave `各方`, `三方`, `多方`, `其余各方`, or `全体合作方` wording in the final agreement.
- Use the system name directly as the project software name. Do not append `平台软件`.
- Prefer the agreement date recorded during intake; use `2026年4月15日` only as the no-answer default.
- Preserve the fixed clause wording from `assets/agreement-template.md`; only the intake date, system name, and user-supplied 乙方 details should vary.

## UI prompt rule

Treat the bundled `ui_prompt/` directory as mandatory input for any pure-frontend design task:

- Select one and only one prompt for the runnable frontend demo.
- Start from `ui_prompt/manifest.json`, then select one style prompt.
- If the user names a style, use that style directly when it exists in `ui_prompt/`.
- If the user does not name a style, randomly choose one prompt from the 30 bundled options.
- Do not infer a default style from domain type such as education, campus, ERP, CRM, or generic admin backend.
- After selecting the slug, read only the chosen `ui_prompt/<slug>/prompt.xml`.
- Preserve the chosen prompt's typography, color direction, composition, and motion language throughout the frontend demo.
- Mention the selected ui prompt slug in the final assumptions or summary.

## Layout rule

Treat layout composition as a separate design decision from color and typography:

- Choose exactly one primary layout archetype from the 10 fixed options before implementing the demo.
- If the user names one of the 10 layout archetypes, use it directly.
- If the user does not name a layout archetype, randomly choose one from the 10 fixed options.
- Do not reuse the same page skeleton for every system just because the style prompt changed.
- Do not default to `left sidebar + right content` unless the chosen layout archetype is exactly that option.
- Reuse the chosen archetype consistently across dashboard, list, detail, and workflow pages.
- Mention the selected layout archetype in the final assumptions or summary.

## Quality bar

- Optimize for package completeness, not production readiness.
- Treat missing or thin full-stack code as a blocking failure, not a warning.
- Do not proceed past the code-pack step unless `scripts/validate_fullstack_code.py` passes.
- Make the runnable frontend believable enough for screenshots and demo review.
- Prefer screenshots from a built preview server rather than an unstable dev server.
- Keep mock data coherent across list, detail, edit, and drill-down pages.
- Block delivery if the fixed document identity appears anywhere under `<system-folder>/code/` or `<system-folder>/demo/`; use fictional mock identities instead.
- Keep manual copy natural and specific. Avoid obviously templated wording, marketing claims, and generic AI-style phrases.
- Keep filenames stable and descriptive.
- Keep the full-stack code and the runnable frontend as separate deliverables.
- Keep every deliverable inside the user-named system folder.
- Do not leave working files in the final `docs` folder. Final `docs` must contain only the cooperation agreement, system manual, and code-source DOCX.

## Resources

- Read [references/output-spec.md](references/output-spec.md) for the exact folder contract and deliverable naming rules.
- Read [references/module-planning.md](references/module-planning.md) for the mandatory 8-10 module planning workflow.
- Read [references/ui-prompt-selection.md](references/ui-prompt-selection.md) for the mandatory pure-frontend style-selection workflow.
- Read [references/layout-archetypes.md](references/layout-archetypes.md) for layout variety and shell selection guidance.
- Read [references/manual-docx-spec.md](references/manual-docx-spec.md) for the required Chinese product-manual structure.
- Read [references/manual-humanize-style.md](references/manual-humanize-style.md) before filling and polishing manual copy.
- Read [references/delivery-workflow.md](references/delivery-workflow.md) for the end-to-end checklist and document rules.
- Read `D:\Projects\code_clean\CLI.md` before generating the cleaned code-source `.docx`.
- Run `scripts/prepare_output_tree.py` to create the folder tree and seed templates.
- Run `scripts/validate_fullstack_code.py` after writing the full-stack code pack and before creating downstream deliverables.
- Run `scripts/validate_frontend_demo.py` to statically verify the demo before launching it or taking screenshots.
- Run `scripts/validate_frontend_build.py` before building the frontend demo for screenshots.
- Run `scripts/validate_frontend_routes.py` against the preview server before Playwright capture.
- Run `scripts/verify_local_playwright.py` to validate the machine-level screenshot runtime.
- Run `scripts/capture_screenshots.py` to capture routes without installing Playwright in the generated project.
- Run `scripts/build_manual_outline.py` to generate a screenshot-driven manual outline before writing the final `.docx`.
- Run `scripts/polish_manual_content.py` after filling `manual-content.json` and before generating the final manual `.docx`.
- Run `scripts/build_manual_docx.py` to generate the final formatted manual `.docx`.
- Run `scripts/build_code_docx.py` after the manual to generate the cleaned code-source `.docx`.
- Use `assets/agreement-template.md` and `assets/manual-template.md` as fallback seeds when the user does not provide templates.
- Use `ui_prompt/manifest.json` to inspect the 30 available frontend design prompts and open only the chosen `ui_prompt/<slug>/prompt.xml`.
