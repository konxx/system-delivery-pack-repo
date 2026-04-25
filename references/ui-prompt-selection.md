# UI Prompt Selection

## Rule

For every pure-frontend deliverable, select exactly one design prompt from `ui_prompt/` before writing UI code.

Do not start styling first and choose later. Do not blend multiple prompts unless the user explicitly asks for a hybrid direction.

## Required flow

1. Read `ui_prompt/manifest.json` to inspect the 30 available styles.
2. If the user names a style slug that exists, use it directly. Otherwise choose one slug randomly from the 30 bundled options.
3. Read only the selected `ui_prompt/<slug>/prompt.xml`.
4. Use that prompt as the primary visual brief for layout, typography, color, motion, and surface treatment.
5. Mention the chosen slug in the final assumptions or delivery summary.

## Default selection

When the user does not specify a style, do not map by industry or system type. Pick one style randomly from the 30 bundled prompts and proceed with that single style consistently.

## Guardrails

- Prefer one prompt with strong consistency over a mixed style.
- Use the prompt as direction, not as a reason to ignore usability.
- Do not apply hidden domain-based defaults when the user has not named a style.
- Only read extra `prompt.xml` files if the user explicitly asks for style comparison or alternatives.
