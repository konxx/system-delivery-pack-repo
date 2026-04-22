# Output Specification

## Required folders

Always keep these folders at the workspace root:

- `outputs/code/`
- `outputs/photos/`
- `outputs/docx/`
- `outputs/Template/`

Also create one runnable frontend folder directly under `outputs/`:

- `outputs/<system-folder>-frontend/`

## Deliverable mapping

### 1. Full-stack code pack

Write the non-validated full-stack source tree to:

- `outputs/code/<system-folder>/`

Recommended internal layout:

- `frontend/`
- `backend/`
- `database/`
- `docs/` or `README.md`

Treat this pack as a believable engineering handoff, not as a verified release.

### 2. Runnable frontend demo

Write the runnable demo to:

- `outputs/<system-folder>-frontend/`

Keep this deliverable independent from the full-stack code pack so it can be launched for screenshots without backend dependencies.

### 3. Screenshots

Write screenshots to:

- `outputs/photos/`

Prefer numbered filenames in business-flow order:

- `01-login.png`
- `02-dashboard.png`
- `03-list.png`
- `04-detail.png`
- `05-form.png`

Use only the screens relevant to the system. Do not fabricate pages the demo does not include.

### 4. Documents

Write final `.docx` files to:

- `outputs/docx/<system-name>-开发协议.docx`
- `outputs/docx/<system-name>-系统说明书.docx`

If the user prefers English filenames, keep the same folder and switch only the visible names.

### 5. Template working area

Use `outputs/Template/` for:

- copied user templates
- fallback seed templates
- manifest files
- screenshot-driven outlines
- draft markdown or note files used to generate the final `.docx`

Do not store the final `.docx` files in `outputs/Template/`.

