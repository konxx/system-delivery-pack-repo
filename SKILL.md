---
name: system-delivery-pack
description: Generate complete system delivery packs from prompts such as "生成仓储管理系统", "生成 CRM 系统", or "build an ERP system". Use when Codex needs to (1) plan 8-10 first-level system modules from the user's brief, (2) write non-validated full-stack source code with React, TypeScript, Python, and PostgreSQL under outputs/code based on those modules, (3) build a runnable frontend demo under outputs/ by first choosing exactly one bundled design prompt from ui_prompt/ (30 styles) and mapping the same modules into the UI, (4) capture Playwright screenshots under outputs/photos, and (5) create the agreement and manual .docx files while keeping template files in outputs/Template.
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
6. Read [references/delivery-workflow.md](references/delivery-workflow.md) before creating screenshots or documents.

## Output contract

Write the deliverables to these locations:

- `outputs/code/<system-folder>/`: full-stack source tree. This code does not need to be proven runnable.
- `outputs/<system-folder>-frontend/`: runnable pure-frontend demo app.
- `outputs/photos/`: Playwright screenshots of the main screens and flows.
- `outputs/docx/`: final agreement and manual `.docx` files.
- `outputs/Template/`: copied user templates, fallback seed templates, outlines, manifests, and other working files.

Do not move these deliverables to other top-level folders unless the user explicitly asks.

## Workflow

### 1. Normalize the brief and lock the module plan

- Infer reasonable defaults when the user gives only a short prompt like `生成进销存系统`.
- Match the user's language. For Chinese prompts, write the agreement and manual in Chinese.
- Keep a short assumptions list and report it after the work is complete.
- Plan 8-10 first-level modules before generating code, UI, screenshots, or documents.
- Do not plan fewer than 8 or more than 10 first-level modules unless the user explicitly asks for a different count.
- Make the module plan drive the frontend navigation, backend routers, service boundaries, database tables, screenshot targets, and document sections.
- Save a short working module list in `outputs/Template/` when helpful for traceability.

### 2. Prepare the output tree

- Run `scripts/prepare_output_tree.py` first so the folder contract is created consistently.
- Let the script copy fallback template seeds from `assets/` into `outputs/Template/`.
- If the user supplied a template file, copy that template into `outputs/Template/` before editing it. Do not modify the original in place.

### 3. Create the full-stack code pack

- Place the full-stack deliverable under `outputs/code/<system-folder>/`.
- Build the code structure from the planned 8-10 modules rather than from generic placeholder sections.
- Use a realistic structure with frontend, backend, API contracts, SQL or schema files, and setup notes.
- Do not spend time proving this code runs unless the user explicitly asks for that extra validation.
- Prefer breadth and coherence: routes, components, models, services, database schema, and representative pages should all exist for the planned modules.
- Use clear TODO comments only where integration details are intentionally omitted.

### 4. Create the runnable frontend demo

- Place the runnable demo under `outputs/<system-folder>-frontend/`.
- Before writing UI code, inspect `ui_prompt/manifest.json` and choose exactly one style prompt from the 30 bundled options.
- After choosing the style, read only the selected `ui_prompt/<slug>/prompt.xml` and use it as the primary visual direction for the pure frontend deliverable.
- Do not mix multiple ui prompts unless the user explicitly asks for a hybrid style.
- Map the planned 8-10 modules into the navigation, page structure, cards, tables, forms, and charts of the runnable frontend demo.
- Make this deliverable runnable with a normal React + TypeScript frontend toolchain. Prefer a Vite layout.
- Use mocked data, local state, or static JSON when backend integration would slow delivery.
- Include the main screens implied by the 8-10 module plan: dashboard plus the module-specific list, detail, form, workflow, analytics, settings, or other screens as needed.
- Keep the UI visually intentional. Do not default to an unstyled placeholder interface.

### 5. Capture Playwright screenshots

- Launch the runnable frontend deliverable and use Playwright to capture the major screens.
- Capture only screens that actually exist in the demo and prioritize the highest-value pages from the module plan.
- Prefer a stable naming pattern such as `01-login.png`, `02-dashboard.png`, `03-list.png`, `04-detail.png`, `05-form.png`.
- Save all screenshots to `outputs/photos/`.
- If runtime setup requires dependency installation or browser installation, request permission when needed and continue once approved.

### 6. Create the development agreement

- Put the final agreement `.docx` in `outputs/docx/`.
- Work from the template copy in `outputs/Template/`.
- Change only two text locations tied to the system name unless the user explicitly points to a different pair of placeholders.
- Preserve the rest of the legal wording and layout.
- If no template was provided, start from `assets/agreement-template.md`, copy it into `outputs/Template/`, and convert the filled result into `.docx`.

### 7. Create the system manual

- Put the final manual `.docx` in `outputs/docx/`.
- Base it on the actual screenshots in `outputs/photos/` plus concise explanatory text.
- Run `scripts/build_manual_outline.py --root <workspace> --system-name "<system name>"` after screenshots are ready to scaffold the manual outline.
- Explain what each screen does, who uses it, what the key actions are, and which planned module it belongs to.
- If no user-provided manual template exists, start from `assets/manual-template.md`, copy it into `outputs/Template/`, and convert the filled result into `.docx`.

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
- Start from `ui_prompt/manifest.json` to shortlist styles, then read the chosen `ui_prompt/<slug>/prompt.xml`.
- If the user names a style, use that style directly when it exists in `ui_prompt/`.
- If the brief is education- or campus-related, prefer `academia` unless the user asks for a different mood.
- If the brief is a generic management backend, prefer `enterprise`, `professional`, or `swiss-minimalist`.
- Preserve the chosen prompt's typography, color direction, composition, and motion language throughout the frontend demo.
- Mention the selected ui prompt slug in the final assumptions or summary.

## Quality bar

- Optimize for package completeness, not production readiness.
- Make the runnable frontend believable enough for screenshots and demo review.
- Keep filenames stable and descriptive.
- Keep the full-stack code and the runnable frontend as separate deliverables.
- Leave the template copies and outline files in `outputs/Template/` for traceability.

## Resources

- Read [references/output-spec.md](references/output-spec.md) for the exact folder contract and deliverable naming rules.
- Read [references/module-planning.md](references/module-planning.md) for the mandatory 8-10 module planning workflow.
- Read [references/ui-prompt-selection.md](references/ui-prompt-selection.md) for the mandatory pure-frontend style-selection workflow.
- Read [references/delivery-workflow.md](references/delivery-workflow.md) for the end-to-end checklist and document rules.
- Run `scripts/prepare_output_tree.py` to create the folder tree and seed templates.
- Run `scripts/build_manual_outline.py` to generate a screenshot-driven manual outline before writing the final `.docx`.
- Use `assets/agreement-template.md` and `assets/manual-template.md` as fallback seeds when the user does not provide templates.
- Use `ui_prompt/manifest.json` to inspect the 30 available frontend design prompts and open only the chosen `ui_prompt/<slug>/prompt.xml`.
