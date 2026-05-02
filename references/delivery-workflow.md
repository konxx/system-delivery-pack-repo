# Delivery Workflow

## Checklist

1. Extract the system name and user roles from the brief.
2. Plan 8-10 first-level modules and keep that module map stable.
3. Create the output tree with `scripts/prepare_output_tree.py`.
4. Build the full-stack code pack under `<system-folder>/code/` from the module map.
5. Build the runnable frontend demo under `<system-folder>/demo/` from the same module map.
6. Run `scripts/validate_frontend_demo.py` and fix the demo if the static validation fails.
7. Launch the demo and capture Playwright screenshots into `<system-folder>/photos/`.
8. Copy the agreement template into `<system-folder>/docs/Template/` and edit only two system-name text slots.
9. Generate the manual outline with `scripts/build_manual_outline.py`.
10. Turn the agreement and manual into final `.docx` files in `<system-folder>/docs/`.
11. Report assumptions, selected ui prompt, final module count, saved paths, and any missing validations.

## Full-stack code pack rules

- Let the planned 8-10 modules shape the routers, services, entities, and frontend pages inside the code pack.
- Prefer coherent structure over execution proof.
- Include representative database tables, API endpoints, service layers, and screens.
- Leave integration seams as TODO comments only when necessary.
- Do not spend the majority of the task on dependency fixes, environment debugging, or tests.

## Runnable frontend rules

- Reflect the planned 8-10 modules in the navigation and page map.
- Make this deliverable actually startable when feasible.
- Prefer mocked data over incomplete backend coupling.
- Include navigation and the main business loop needed for screenshots.
- Keep the visuals intentional enough for a handoff screenshot pack.
- Ensure the demo passes `scripts/validate_frontend_demo.py` before treating it as ready for launch.

## Screenshot rules

- Never start Playwright screenshots if the static frontend validation fails.
- Use Playwright, not manual screenshots.
- Wait for the page to settle before capturing.
- Favor full-page screenshots only when it helps readability; otherwise use viewport captures with consistent dimensions.
- Capture the highest-value pages first: login or landing, dashboard, the most important module pages, record detail, create or edit flow, analytics or settings if present.

## Agreement rules

- Preserve the original template wording.
- Change only the title-level system name and one body-level project-name reference.
- If the template includes explicit placeholders, replace those exact placeholders and nothing else.
- Keep the working copy in `<system-folder>/docs/Template/` and place the final `.docx` in `<system-folder>/docs/`.

## Manual rules

- Base the manual on the actual screenshots, not on imagined pages.
- Describe each page in terms of user goal, main information, primary actions, and the module it belongs to.
- Explain major workflows in business order.
- Mention demo assumptions such as mock data, omitted integrations, or simplified permissions.
