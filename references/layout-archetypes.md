# Layout Archetypes

## Rule

Before building the runnable frontend demo, choose exactly one primary layout archetype from the 10 fixed options below.

Do not treat the chosen `ui_prompt` as color-only guidance. The layout shell must also change.

## Selection rule

- If the user explicitly names one of the 10 layout archetypes, use it directly.
- If the user does not name a layout archetype, randomly choose one from the 10 fixed options.
- Use one archetype only. Do not blend multiple layout shells unless the user explicitly asks for a hybrid layout.

## Guardrail

Do not default to `3. 左侧导航栏，右侧内容`.

Use that layout only when it is the selected archetype. Do not silently fall back to it for convenience.

## 10 Fixed Layout Archetypes

### 1. 移动端风格，底部 tab 栏

- Use a mobile-app shell with bottom tab navigation, top title bar, and stacked card content.
- Good for lightweight operational systems, field workflows, campus micro-apps, and touch-first demos.

### 2. 顶部导航栏，内容区域卡片式布局

- Use a top navigation bar, horizontal module switching, and modular card sections in the content area.
- Good for modern SaaS, polished admin products, and systems that need a clean dashboard-first structure.

### 3. 左侧导航栏，右侧内容

- Use a classic persistent left navigation with a right-side workspace.
- Good for dense management backends, multi-module operations platforms, and tools with constant navigation depth.

### 4. 单页面滚动式，全宽无侧边栏

- Use a full-width scrolling canvas with anchored sections, no sidebar, and strong narrative rhythm.
- Good for overview-heavy systems, exhibition-style dashboards, academic or editorial experiences, and showcase demos.

### 5. 双栏工作台，左侧筛选/摘要，右侧主内容

- Use a two-column shell with filters, summaries, or entity lists on the left and the active workspace on the right.
- Good for review, approval, inspection, and detail-heavy operational workflows.

### 6. Bento 宫格式总览，模块卡片入口

- Use a bento-grid overview where modules appear as large entry cards, metric tiles, and drill-in panels.
- Good for analytics-heavy systems, operations centers, and reporting-focused management products.

### 7. 顶部标签栏 + 二级面板切换

- Use a top tab strip for primary modules and secondary inline panels or segmented controls inside each page.
- Good for business systems that need dense controls without relying on a permanent sidebar.

### 8. 卡片画廊 + 详情聚焦区

- Use a gallery or grid of entities with a strong spotlight area for detail, preview, or editing.
- Good for products, assets, courses, students, media, and catalog-like systems.

### 9. 时间线 / 流程步骤式布局

- Use sequential stages, step rails, or timeline-driven content as the main organizing model.
- Good for approvals, onboarding, scheduling, service handling, logistics, and lifecycle tracking.

### 10. 浮动导航 + 抽屉/弹层工作区

- Use floating nav controls with drawers, sheets, popovers, or layered panels for deeper interaction.
- Good for experimental, futuristic, playful, or high-interaction demos where the shell should feel less traditional.

## How To Use The Archetype

- Let the chosen archetype control navigation placement, filter placement, page rhythm, list/detail transitions, and dashboard structure.
- Do not keep the same page skeleton while only swapping color tokens from a different `ui_prompt`.
- Keep dashboard, list, detail, and workflow pages structurally related to the same archetype.

## Final check

Before finalizing the demo, ask:

- Is this clearly one of the 10 layout archetypes above?
- Would this still be structurally distinct if I swapped the colors?
- Did I avoid defaulting to `3. 左侧导航栏，右侧内容` unless that exact archetype was chosen?

If the answer is no, redesign the shell before proceeding.
