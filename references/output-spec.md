# Output Specification

## Required folders

Always create one top-level folder named after the user input system name:

- `<system-folder>/`
- `<system-folder>/code/`
- `<system-folder>/demo/`
- `<system-folder>/photos/`
- `<system-folder>/docs/`
- `<system-folder>/docs/Template/`

## Deliverable mapping

### 1. Full-stack code pack

Write the non-validated full-stack source tree to:

- `<system-folder>/code/`

Recommended internal layout:

- `frontend/`
- `backend/`
- `database/`
- `docs/` or `README.md`

Treat this pack as a believable engineering handoff, not as a verified release.

Hard minimums:

- Include `frontend/`, `backend/`, and `database/`; none may be omitted.
- `frontend/` must be a React + TypeScript source tree with `package.json`, `src/`, an entry file, and module-specific pages/components.
- `backend/` must include Python/FastAPI-style app code with module routers and representative service/model logic.
- `database/` must include schema and seed/sample SQL.
- The pack must pass `scripts/validate_fullstack_code.py` before any demo, screenshot, document, or code-source DOCX step.

### 2. Runnable frontend demo

Write the runnable demo to:

- `<system-folder>/demo/`

Keep this deliverable independent from the full-stack code pack so it can be launched for screenshots without backend dependencies.

### 3. Screenshots

Write screenshots to:

- `<system-folder>/photos/`

Prefer numbered filenames in business-flow order:

- `01-login.png`
- `02-dashboard.png`
- `03-list.png`
- `04-detail.png`
- `05-form.png`

Use only the screens relevant to the system. Do not fabricate pages the demo does not include.

### 4. Documents

Write final `.docx` files to:

- `<system-folder>/docs/<system-name>合作开发协议.docx`
- `<system-folder>/docs/<system-name>-系统说明书.docx`
- `<system-folder>/docs/<system-name>代码源程序V1.0.docx`

If the user prefers English filenames, keep the same folder and switch only the visible names.

### 5. Template working area

Use `<system-folder>/docs/Template/` for:

- copied user templates
- fallback seed templates
- manifest files
- screenshot-driven outlines
- draft markdown or note files used to generate the final `.docx`
- manual draft files intended for Pandoc or `python-docx` based conversion

Keep the final `.docx` files in `<system-folder>/docs/`, not in `<system-folder>/docs/Template/`.
