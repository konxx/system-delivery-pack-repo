# UI Prompt Selection

## Rule

For every pure-frontend deliverable, select exactly one design prompt from `ui_prompt/` before writing UI code.

Do not start styling first and choose later. Do not blend multiple prompts unless the user explicitly asks for a hybrid direction.

## Required flow

1. Read `ui_prompt/manifest.json` to inspect the 30 available styles.
2. Choose one slug that fits the user's domain, audience, and tone.
3. Read only the selected `ui_prompt/<slug>/prompt.xml`.
4. Use that prompt as the primary visual brief for layout, typography, color, motion, and surface treatment.
5. Mention the chosen slug in the final assumptions or delivery summary.

## Default matching

- Education, campus, student, teacher, training, library: `academia`
- Generic management backend, ERP, CRM, OA, MIS: `enterprise`
- Serious admin console, policy-heavy dashboards, data-dense tools: `professional` or `swiss-minimalist`
- Modern SaaS product, productized dashboard, startup platform: `saas`
- Youthful or friendly product: `playful-geometric`, `sketch`, or `claymorphism`
- Industrial or manufacturing context: `industrial`
- Premium, editorial, luxury, brand-heavy: `luxury`, `monochrome`, or `art-deco`
- Futuristic, AI, hacker, security, neon: `modern-dark`, `cyberpunk`, `terminal`, or `vaporwave`

If multiple styles could fit, choose the one that best supports the user's domain first and novelty second.

## Guardrails

- Prefer one prompt with strong consistency over a mixed style.
- Use the prompt as direction, not as a reason to ignore usability.
- For education systems, default to `academia` unless the user requests a more software-product look.
- For backoffice business systems without a strong brand signal, default to `enterprise`.
- Only read extra `prompt.xml` files if the user explicitly asks for style comparison or alternatives.
