# Manual DOCX Specification

## Rule

When generating the product manual `.docx`, follow this structure by default for Chinese software manuals unless the user explicitly provides a different template.

Prefer high-fidelity `.docx` generation with `python-docx` for final formatting. Use Pandoc as a draft conversion tool when helpful.

## Tooling

- Preferred final formatter: `python-docx`
- Pandoc path: `C:\Program Files\Pandoc\pandoc.exe`
- Use Pandoc to convert markdown drafts into a working `.docx` when that speeds up drafting, then apply final formatting fixes in Word structure or `python-docx`.

## Page setup

- Paper size target: A4
- Physical size target: 21cm * 29cm
- Margins:
  - top: 2.5cm
  - bottom: 2.5cm
  - left: 3cm
  - right: 3cm

## Header

- The cover page must not display a header.
- Every page after the cover page must display a header.
- Header typography: Chinese font 宋体, English font Times New Roman, 小五.
- Header content: left side `<system-name>V1.0`; right side page number in `X/Y` format.
- Use Word fields for page numbers: `PAGE/NUMPAGES`.

## Outline levels

- `修订记录` and the chapter headings `一、二、三、四、五` use outline level 1.
- Subheadings such as `4.1`、`4.2`、`4.3`、`5.1` to `5.X` use outline level 2.

## Required structure

### Cover page

- First page only.
- Main title: `{{SYSTEM_NAME}}[简称：{{SYSTEM_SHORT_NAME}}]V1.0`
- Subtitle on next line: `产品说明书`
- Typography target: 宋体、一号、居中、加粗
- Vertical layout target: title block starts after about 5 blank lines worth of top spacing
- Short name should be decided automatically from the system name when the user does not provide one.

### Page 2: 目录

- New page placed after the cover page and before `修订记录`.
- Title text: `目  录`
- Typography target: 宋体、二号、加粗、居中
- Keep two spaces between `目` and `录`.
- Directory content should include outline levels 1 and 2.

### Page 3: 修订记录

- New page.
- Heading: `修订记录`
- Typography target: 宋体、三号、加粗、左对齐
- After the heading, insert one 2-row 4-column table.
- Table font target: 宋体、小四、居中
- Column widths:
  - 版本号: 2cm
  - 生成日期: 3cm
  - 作者: 6.5cm
  - 修订内容: 3.5cm
- Row height: 0.9cm
- Header cells:
  - 版本号
  - 生成日期
  - 作者
  - 修订内容
- First data row:
  - 版本号: `V1.0`
  - 生成日期: `2026-6-15`
  - 作者: `孔祥鑫`
  - 修订内容: `初始版本`

### Page 4: 一、软件介绍

- New page.
- Heading: `一、软件介绍`
- Typography target: 宋体、三号、左对齐
- Body content uses 宋体、小四、首行缩进 2 字符
- Required lines:
  - 软件名称：`{{SYSTEM_NAME}}`
  - 简称：`{{SYSTEM_SHORT_NAME}}`
  - 版本号：`V1.0`
  - 软件类别：`应用软件`
  - 著作权人：`孔祥鑫`

### Page 5: 二、软件用途

- New page.
- Heading: `二、软件用途`
- Typography target: 宋体、三号、左对齐
- Follow with one natural paragraph within 200 Chinese characters describing the software purpose.
- Generate this paragraph from the final planned business modules instead of using one generic canned sentence.

### Page 6: 三、软件功能

- New page.
- Heading: `三、软件功能`
- Typography target: 宋体、三号、左对齐
- Follow with one natural paragraph within 200 Chinese characters describing the software functions.
- Generate this paragraph from the final planned business modules instead of using one generic canned sentence.

### Page 6+: 四、运行环境

- New page.
- Heading: `四、运行环境`
- Typography target: 宋体、三号、左对齐

#### 4.1 硬件要求

- Heading typography target: 宋体、三号、左对齐
- Insert one 2-row 2-column table
- Table font target: 宋体、小四、左对齐
- Column widths:
  - 类型: 2.8cm
  - 基本要求: 12.2cm
- Row height: 0.9cm
- Header cells:
  - 类型
  - 基本要求
- First data row:
  - 类型: `服务器端`
  - 基本要求: `CPU 8核1.60GHz，内存8G，硬盘剩余空间10G`

#### 4.2 软件环境

- Heading typography target: 宋体、三号、左对齐
- Insert one 5-row 2-column table
- Table font target: 宋体、小四、左对齐
- Column widths:
  - 名称: 2.8cm
  - 基本环境: 12.2cm
- Row height: 0.9cm
- Header cells:
  - 名称
  - 基本环境
- Data rows:
  - 操作系统 | `Windows 10 64位`
  - 数据库软件 | `PostgreSQL`
  - 开发软件 | `Opencode，Claude Code，Codex，IntelliJ IDEA，Navicat 16`
  - 开发语言 | 按全栈代码如实填写并带版本号，例如 `Python 3.10`

#### 4.3 软件开发环境

- New page.
- Heading typography target: 宋体、三号、左对齐
- Follow with one paragraph using this pattern and fill the actual frontend/backend languages:
  - `本软件分为前端页面和后端业务逻辑，其中前端页面使用XX语言进行开发，后端业务逻辑使用XX进行开发，数据库使用PostgreSQL，数据库管理采用Navicat 16，整个系统使用IntelliJ IDEA环境进行开发。开发界面如图4-1所示。`
- Leave a figure placeholder for the user to insert manually.
- Required caption below the figure:
  - `图4-1 软件开发界面`
- Caption typography target: 宋体、小四、居中

### Page group: 五、软件使用

- New page.
- Heading: `五、软件使用`
- Typography target: 宋体、三号、左对齐
- Use subsections `5.1` to `5.X` for screenshots from the demo frontend.
- Each screenshot subsection must start on a new page.
- For each subsection:
  - include the screenshot image
  - include one natural paragraph around 200 Chinese characters
  - the paragraph must cover image description, page purpose, core information, and main operations
  - place the caption below the image
  - caption typography target: 宋体、小四、居中

## Screenshot section rule

- Use only screenshots that actually exist in `<system-folder>/photos/`.
- If a screenshot corresponds to a broken or disconnected secondary page, omit that subsection.
- Prefer one screenshot per page for section 5.

## Consistency rule

- Keep `{{SYSTEM_NAME}}`, `{{SYSTEM_SHORT_NAME}}`, version, author, and stack wording consistent across the whole document.
- If the generated code stack conflicts with the default wording above, prefer real generated languages for language fields.
- Prefer deriving `{{SYSTEM_SHORT_NAME}}` automatically from the system name with a concise readable abbreviation.
