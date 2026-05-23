---
name: system-delivery-pack
description: Generate complete system delivery packs from prompts such as "生成仓储管理系统", "生成 CRM 系统", or "build an ERP system". Use when Codex needs to (1) plan 8-10 first-level system modules from the user's brief, (2) write non-validated full-stack source code with React, TypeScript, Python, and PostgreSQL under <system-name>/code based on those modules, (3) build a runnable frontend demo under <system-name>/demo by first choosing exactly one bundled design prompt from ui_prompt/ (30 styles) and mapping the same modules into the UI, (4) capture Playwright screenshots under <system-name>/photos, and (5) create the agreement and manual .docx files under <system-name>/docs while keeping working templates and outlines inside <system-name>/docs/Template.
---

# System Delivery Pack

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

1. Extract the system name, the primary user roles, and whether the user supplied an agreement template.
2. Read [references/module-planning.md](references/module-planning.md) and plan 8-10 first-level modules before writing any deliverable.
3. Run `scripts/prepare_output_tree.py --root <workspace> --system-name "<system name>"`.
4. Read [references/output-spec.md](references/output-spec.md) before writing files.
5. Read [references/ui-prompt-selection.md](references/ui-prompt-selection.md) before creating the pure-frontend deliverable.
6. Read [references/layout-archetypes.md](references/layout-archetypes.md) before deciding the frontend information architecture.
7. Read [references/manual-docx-spec.md](references/manual-docx-spec.md) before generating the product manual `.docx`.
8. Read [references/delivery-workflow.md](references/delivery-workflow.md) before creating screenshots or documents.

## Output contract

Write the deliverables to these locations:

- `<system-folder>/code/`: full-stack source tree. This code does not need to be proven runnable.
- `<system-folder>/demo/`: runnable pure-frontend demo app.
- `<system-folder>/photos/`: Playwright screenshots of the main screens and flows.
- `<system-folder>/docs/`: final agreement and manual `.docx` files.
- `<system-folder>/docs/Template/`: copied user templates, fallback seed templates, outlines, manifests, and other working files.

Do not move these deliverables to other top-level folders unless the user explicitly asks.

## Workflow

### 1. Normalize the brief and lock the module plan

- Infer reasonable defaults when the user gives only a short prompt like `生成进销存系统`.
- Match the user's language. For Chinese prompts, write the agreement and manual in Chinese.
- Keep a short assumptions list and report it after the work is complete.
- Plan 8-10 first-level modules before generating code, UI, screenshots, or documents.
- Do not plan fewer than 8 or more than 10 first-level modules unless the user explicitly asks for a different count.
- Make the module plan drive the frontend navigation, backend routers, service boundaries, database tables, screenshot targets, and document sections.
- Save a short working module list in `<system-folder>/docs/Template/` when helpful for traceability.

### 2. Prepare the output tree

- Run `scripts/prepare_output_tree.py` first so the folder contract is created consistently.
- Let the script copy fallback template seeds from `assets/` into `<system-folder>/docs/Template/`.
- If the user supplied a template file, copy that template into `<system-folder>/docs/Template/` before editing it. Do not modify the original in place.

### 3. Create the full-stack code pack

- Place the full-stack deliverable under `<system-folder>/code/`.
- Build the code structure from the planned 8-10 modules rather than from generic placeholder sections.
- Use a realistic structure with frontend, backend, API contracts, SQL or schema files, and setup notes.
- Do not spend time proving this code runs unless the user explicitly asks for that extra validation.
- Prefer breadth and coherence: routes, components, models, services, database schema, and representative pages should all exist for the planned modules.
- Use clear TODO comments only where integration details are intentionally omitted.

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
- Include the main screens implied by the 8-10 module plan: dashboard plus the module-specific list, detail, form, workflow, analytics, settings, or other screens as needed.
- When the demo includes secondary pages such as detail, edit, or drill-down views, keep their mock data linked to the primary list data through the same record IDs or keys.
- Prefer a single shared mock dataset per module so list pages, detail pages, and forms refer to the same entities instead of unrelated placeholders.
- Keep the UI visually intentional. Do not default to an unstyled placeholder interface.
- Run `scripts/validate_frontend_demo.py --root <workspace> --system-name "<system name>"` before any launch or screenshot step.
- Run `scripts/validate_frontend_build.py --root <workspace> --system-name "<system name>"` before using any build-first screenshot workflow.
- If the static validation fails, fix the frontend structure first. Do not continue to Playwright screenshots with a broken or incomplete demo.

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
- If runtime setup requires dependency installation or browser installation, request permission when needed and continue once approved.

### 6. Create the development agreement

- Put the final agreement `.docx` in `<system-folder>/docs/`.
- Work from the template copy in `<system-folder>/docs/Template/`.
- Change only two text locations tied to the system name unless the user explicitly points to a different pair of placeholders.
- Preserve the rest of the legal wording and layout.
- If no template was provided, start from `assets/agreement-template.md`, copy it into `<system-folder>/docs/Template/`, and convert the filled result into `.docx`.

### 7. Create the system manual

- Put the final manual `.docx` in `<system-folder>/docs/`.
- Base it on the actual screenshots in `<system-folder>/photos/` plus concise explanatory text.
- Read [references/manual-docx-spec.md](references/manual-docx-spec.md) first and follow it as the default Chinese manual structure.
- Use `C:\Program Files\Pandoc\pandoc.exe` as the default draft conversion path when Pandoc is needed.
- Run `scripts/build_manual_outline.py --root <workspace> --system-name "<system name>"` after screenshots are ready to scaffold the manual draft.
- Run `scripts/build_manual_docx.py --root <workspace> --system-name "<system name>"` to produce the final formatted manual `.docx`.
- Before running `build_manual_docx.py`, the current agent must directly fill the blank fields in `manual-content.json`.
- Fill natural Chinese copy for:
  - `short_name`
  - `purpose_text`
  - `function_text`
  - `development_environment_text`
  - each `screenshot_sections[].title`
  - each `screenshot_sections[].description_text`
- The language must be concise, natural, and specific to the system. Do not leave templated placeholders or generic canned text.
- Explain what each screen does, who uses it, what the key actions are, and which planned module it belongs to.
- In section `五、软件使用`, place one screenshot subsection per page with one natural-language paragraph around 200 Chinese characters.
- Keep the cover page, revision table, runtime tables, and figure captions consistent with the manual docx spec.
- If no user-provided manual template exists, start from `assets/manual-template.md`, copy it into `<system-folder>/docs/Template/`, and convert the filled result into `.docx`.

## Module planning rule

Treat module planning as a mandatory upstream step:

- Always plan 8-10 first-level modules from the user's system brief before generating any deliverable.
- Keep the modules at the same hierarchy level. Do not count subfeatures as separate first-level modules just to reach the target.
- Prefer a mix of domain modules and supporting modules so the system feels complete.
- Reuse the same module names across code folders, frontend navigation, screenshot labels, and document sections whenever practical.
- If the brief is too small, expand with reasonable supporting modules instead of dropping below 8.
- Mention the final module count in the completion summary.

## Agreement edit rule

Treat `只改两处文字` literally:

- Replace the title-level system name.
- Replace one body-level project-name reference.
- Do not rewrite clause wording, payment terms, liability, acceptance terms, or schedule text unless the user explicitly asks.

If the provided template already marks two named placeholders, use those placeholders instead of guessing.

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
- Make the runnable frontend believable enough for screenshots and demo review.
- Prefer screenshots from a built preview server rather than an unstable dev server.
- Keep mock data coherent across list, detail, edit, and drill-down pages.
- Keep manual copy natural and specific. Avoid obviously templated wording.
- Keep filenames stable and descriptive.
- Keep the full-stack code and the runnable frontend as separate deliverables.
- Keep every deliverable inside the user-named system folder.
- Leave the template copies and outline files in `<system-folder>/docs/Template/` for traceability.

## Resources

- Read [references/output-spec.md](references/output-spec.md) for the exact folder contract and deliverable naming rules.
- Read [references/module-planning.md](references/module-planning.md) for the mandatory 8-10 module planning workflow.
- Read [references/ui-prompt-selection.md](references/ui-prompt-selection.md) for the mandatory pure-frontend style-selection workflow.
- Read [references/layout-archetypes.md](references/layout-archetypes.md) for layout variety and shell selection guidance.
- Read [references/manual-docx-spec.md](references/manual-docx-spec.md) for the required Chinese product-manual structure.
- Read [references/delivery-workflow.md](references/delivery-workflow.md) for the end-to-end checklist and document rules.
- Run `scripts/prepare_output_tree.py` to create the folder tree and seed templates.
- Run `scripts/validate_frontend_demo.py` to statically verify the demo before launching it or taking screenshots.
- Run `scripts/validate_frontend_build.py` before building the frontend demo for screenshots.
- Run `scripts/validate_frontend_routes.py` against the preview server before Playwright capture.
- Run `scripts/build_manual_outline.py` to generate a screenshot-driven manual outline before writing the final `.docx`.
- Run `scripts/build_manual_docx.py` to generate the final formatted manual `.docx`.
- Use `assets/agreement-template.md` and `assets/manual-template.md` as fallback seeds when the user does not provide templates.
- Use `ui_prompt/manifest.json` to inspect the 30 available frontend design prompts and open only the chosen `ui_prompt/<slug>/prompt.xml`.
