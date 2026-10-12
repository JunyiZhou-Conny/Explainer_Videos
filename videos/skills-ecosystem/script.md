# One Skill Library, Three Coding Agents

一套技能库，三个编程助手

Target: 300 seconds · 662 English words · English narration · Chinese and English subtitles · Swiss preset

## Production notes — not spoken

- This script does not claim successful installation, live discovery, or invocation in any application. Scene 8 describes the intended organization; scene 9 explains how to verify it.
- Before rendering, root must confirm the finished conny-explainer-video bundle uses all seven named presets and exactly the defaults in scene 11. Change the script if implementation differs.
- Show exact filesystem paths on screen, but use the natural spoken path names in the English lines for narration. Tilde means the current user home directory.
- Label scene 3 counts as the October 12 baseline before installation. Do not relabel 83 as the current count after adding skills.
- The style names are the requested preset catalog. Do not imply the presets reproduce a creator's footage exactly or that all seven styles have passed rendered-sample review.
- Scene 12 describes our reusable production workflow. It does not attribute those exact roles or steps to the uploader without separate viewing evidence.
- For science-fiction references, use Starfield / NASA-punk and Rhine Lab. Do not substitute Star Wars imagery or labels.
- The full local catalog belongs in companion links/credits, not a scrolling display of private project filenames. Use SOURCES.md and report.md.
- Target five minutes at approximately 130 English words per minute. Actual voice duration and caption readability require rendering checks; word count does not prove duration.

## s01: Save the preferences. Shorten the prompt. / 保存偏好，缩短提示词

**Visual:** A dense generic paragraph collapses into a short prompt card: 'Use conny-explainer-video. Explain my Cursor skills. Swiss, 5 minutes, bilingual subtitles.' Reveal a separate saved workflow card. Do not display any real chat history.

**EN:** Imagine asking for a video with one sentence: explain my Cursor skills, in Swiss style, five minutes, with bilingual subtitles.

**ZH:** 想象一下，只用一句话就能提出视频需求：用瑞士风格解释我的 Cursor 技能，五分钟，配中英双语字幕。

**EN:** You should not have to describe the fonts, pacing, structure, and export settings every time. A reusable skill stores those decisions, so your next request can focus on the topic.

**ZH:** 你不必每次都重新描述字体、节奏、结构和导出设置。可复用的技能会保存这些决定，让下一次请求专注于要讲的主题。

**Evidence:** User objective: reusable video styles/specifications; SOURCES.md

## s02: Recipe · Equipment · Cook / 食谱 · 厨具 · 厨师

**Visual:** Three aligned Swiss grid columns: SKILL / TOOL / AGENT. A recipe card, a renderer icon, and Cursor-Codex-Claude labels appear in narration order. Show 'instructions', 'capability', 'execution' underneath.

**EN:** A skill is a recipe: when to use a workflow, what steps to follow, and what a good result contains.

**ZH:** 技能就像食谱：它说明何时使用工作流、要按哪些步骤操作，以及合格的结果包含什么。

**EN:** Tools are equipment, such as a video renderer or image generator. Cursor, Codex, and Claude Code are the cooks. Sharing a recipe does not automatically give every cook the same equipment.

**ZH:** 工具是厨具，比如视频渲染器或图像生成器。Cursor、Codex 和 Claude Code 则是厨师。共享食谱，并不会自动让每位厨师拥有相同的厨具。

**Evidence:** SOURCES.md; SOURCES.md

## s03: Your actual folder map / 你电脑上的真实目录

**Visual:** Show exact paths ~/.agents/skills → 83; ~/.cursor/skills-cursor → 25; ~/.cursor/skills → absent. A persistent label reads '2026-10-12 baseline · before video-skill installation'. Group first two as shared personal and Cursor-managed.

**EN:** Your Mac already has a shared starting point. Before this installation, the audit found eighty-three skill folders under dot agents, then skills, in your home folder.

**ZH:** 你的 Mac 已经有一个共享起点。在安装这次的新技能之前，审计发现你的主目录下，点 agents 里的 skills 文件夹中有八十三个技能文件夹。

**EN:** Cursor separately maintained twenty-five skills under dot cursor, then skills cursor. The ordinary dot cursor skills folder did not exist. Similar names can describe very different locations and owners.

**ZH:** Cursor 还在点 cursor 里的 skills-cursor 目录中单独维护了二十五个技能。普通的点 cursor 下的 skills 文件夹当时并不存在。相近的名称，可能代表不同的位置和管理者。

**Evidence:** SOURCES.md roots; SOURCES.md

## s04: A folder is not always a skill / 并非每个文件夹都是技能

**Visual:** Expand ~/.cursor into extensions/, plugins/, projects/, skills-cursor/, mcp.json, hooks.json. Give each one a short bilingual label. Cached version cards stack behind one plugin; never light them all as active.

**EN:** Inside dot cursor, extensions add editor features. Plugins bundle agent capabilities. Projects stores working state, while the M C P configuration names tool connections and hooks can launch commands.

**ZH:** 在点 cursor 中，extensions 提供编辑器功能，plugins 打包助手能力，projects 保存工作状态。MCP 配置定义工具连接，而 hooks 可以触发命令。

**EN:** Plugin caches can keep several versions of one skill. A file's presence does not prove the application loads it. The companion catalog records all observed copies.

**ZH:** 插件缓存可能保留同一技能的多个版本。文件存在，不代表应用正在加载它。配套目录记录了所有观察到的副本。

**Evidence:** SOURCES.md; SOURCES.md

## s05: Open one skill / 打开一个技能看看

**Visual:** An original example folder conny-explainer-video/ unfolds into SKILL.md, references/, scripts/, assets/. Highlight frontmatter name/description, then numbered workflow, then optional resources. Avoid implying directory names alone execute anything.

**EN:** Inside a skill folder, find the skill markdown file. Its name and description identify when it applies. The main text supplies the procedure.

**ZH:** 在技能文件夹中，先找 SKILL.md。文件中的名称和描述说明何时使用它，正文则提供操作流程。

**EN:** References hold style guidance, scripts automate rendering steps, and assets supply templates. Together they turn a repeated conversation into a reusable package. Instructions still need tools capable of carrying them out.

**ZH:** references 保存风格指南，scripts 自动完成渲染步骤，assets 提供模板。它们一起把反复进行的对话变成可复用的包。但这些指令仍然需要相应工具才能执行。

**Evidence:** SOURCES.md; https://agentskills.io/specification

## s06: Who authored it? Who installed it? / 谁编写？谁安装？

**Visual:** Three distinct provenance rows: AUTHOR, FILE MANAGER, INSTALLER. Show Google Cloud Data Agent Kit → 26 identical SKILL.md files. Label content match as verified; installer identity as unknown. Use a short hash-equality graphic, not a full opaque digest.

**EN:** To trace origin, distinguish the author, the software managing the files, and whoever installed them.

**ZH:** 追溯来源时，要区分内容作者、管理文件的软件，以及执行安装的人或程序。

**EN:** For example, twenty-six shared skill files exactly match copies inside your Google Cloud Data Agent Kit extension. That proves matching content. It does not prove who copied them. Manifests and installer code provide evidence; timestamps alone cannot identify the installer.

**ZH:** 例如，你的二十六份共享技能文件与 Google Cloud Data Agent Kit 扩展中的副本完全一致。这证明内容相同，却不能证明是谁复制的。清单和安装代码可以提供证据；仅凭时间戳无法确定安装者。

**Evidence:** SOURCES.md; SOURCES.md identical_skill_md_elsewhere

## s07: Useful for which job? / 对哪项任务有用？

**Visual:** Three project cards: AWS / Python research / Explainer videos. Route amazon-bedrock, managing-python-dependencies, and conny-explainer-video to corresponding cards. Show a fourth small 'connector needed' marker beside image generation.

**EN:** Usefulness depends on the job. Bedrock and storage skills can help with your A W S projects. Python dependency and notebook skills support research workflows.

**ZH:** 是否有用，取决于具体任务。Bedrock 和存储技能能帮助你处理 AWS 项目，Python 依赖和 notebook 技能则支持研究工作流。

**EN:** For videos, prioritize evidence, explanations, visual design, narration, and rendering. Keep specialist skills for relevant topics. A large collection is not automatically wasteful. Installed instructions do not prove a connected service works.

**ZH:** 制作视频时，优先考虑依据、讲解、视觉设计、旁白和渲染。专业技能留给相关主题使用。技能多不等于浪费，装有指令也不代表连接的服务一定可用。

**Evidence:** SOURCES.md; SOURCES.md usefulness_for_this_goal

## s08: One editable home / 只维护一个来源

**Visual:** Show canonical ~/.agents/skills/conny-explainer-video/ as one physical folder. Cursor and Codex read from it. ~/.claude/skills/conny-explainer-video is a dashed symbolic-link arrow to the same folder. Add 'local Mac setup' label and no discovery checkmarks.

**EN:** For the new library, keep one editable source under your home folder's dot agents skills directory. Current Cursor and Codex documentation both recognize this location.

**ZH:** 新的技能库只保留一个可编辑来源，放在主目录的点 agents 下的 skills 中。当前的 Cursor 和 Codex 文档都支持这个位置。

**EN:** Claude Code gets a symbolic link from its own skills folder, pointing to the same files. Edit the source once. Keep application-managed skills and plugin caches in place.

**ZH:** Claude Code 则通过自己 skills 文件夹中的符号链接访问同一套文件，因此修改来源一次即可。由应用管理的技能和插件缓存仍保留在原位。

**Evidence:** SOURCES.md; https://cursor.com/docs/skills; https://learn.chatgpt.com/docs/build-skills; https://code.claude.com/docs/en/skills

## s09: Find it. Invoke it. Check it. / 找到、调用、验证

**Visual:** Three sequential verification cards: appears in picker → brief uses saved defaults → short render reviewed. Show plain examples '$conny-explainer-video' for Codex CLI, '/' picker for Cursor, '/conny-explainer-video' for Claude. Label interfaces explicitly.

**EN:** After installation, check each application's skill picker. Select Conny Explainer Video and first ask for a production brief. Confirm that it uses the intended preset and defaults.

**ZH:** 安装后，检查每个应用的技能选择器。选中 Conny Explainer Video，先让它生成制作简报，确认它采用了预期的风格预设和默认设置。

**EN:** Then test an override and a short render. Can the app find the skill, follow its instructions, and produce the result? Remote computers need their own setup.

**ZH:** 接着测试参数覆盖和短片渲染：应用能否找到技能、遵循指令，并产出结果？远程电脑需要单独配置。

**Evidence:** SOURCES.md; SOURCES.md

## s10: Choose a preset by name / 用名称选择风格

**Visual:** Seven original compact preset cards: swiss, cassette-futurism, de-stijl, bauhaus, nasa-punk, rhine-lab, pixel-studio. Starfield/NASA-punk and Rhine Lab are separate cards. Use abstract palettes and typography, no copied logos or game screenshots.

**EN:** The preset menu gives your preferences short names: Swiss, cassette futurism, De Stijl, Bauhaus, NASA punk, Rhine Lab, and pixel studio.

**ZH:** 预设菜单把你的偏好变成简短名称：瑞士风格、盒式未来主义、风格派、包豪斯、NASA 朋克、莱茵生命，以及像素工作室。

**EN:** Your science-fiction references include Starfield, NASA punk, and Rhine Lab. Each preset should specify palette, typography, composition, and motion. A style name selects a design brief; the rendered sample shows how well it works.

**ZH:** 你的科幻参考包括《星空》、NASA 朋克和莱茵生命。每个预设都应定义配色、字体、构图和运动方式。风格名称会选中设计规范，实际样片才能展示效果。

**Evidence:** User clarification: Starfield / NASA-punk / Rhine Lab; Requested conny-explainer-video preset catalog; root must validate final bundle

## s11: Defaults do the repetitive work / 把重复选择交给默认设置

**Visual:** A specification panel resolves: swiss; 300 seconds; 1920×1080; 30 fps; English narration; Chinese + English captions. An explicit override '2 minutes' changes only duration. Keep captions in a reserved lower region.

**EN:** For this workflow, the default brief is Swiss design, five minutes, ten eighty p, thirty frames per second, English narration, and Chinese plus English subtitles.

**ZH:** 这个工作流的默认简报是：瑞士风格、五分钟、1080p、每秒三十帧、英语旁白，以及中英双语字幕。

**EN:** You only need to state changes. Asking for two minutes overrides the duration. The saved workflow should carry your usual choices forward while keeping your current request in control.

**ZH:** 你只需说明要改的地方。要求两分钟，就会覆盖默认时长。保存的工作流延续你惯用的选择，同时以你本次的要求为准。

**Evidence:** Requested defaults for conny-explainer-video; root must verify finished bundle; SOURCES.md

## s12: From one request to a reviewed video / 从一句请求到经过检查的视频

**Visual:** Prompt 'Use conny-explainer-video. Explain my Cursor skills. Swiss, 5 minutes, bilingual subtitles.' flows through DIRECTOR / DESIGNER / ENGINEER, then an actual sample preview if available. End with a companion-catalog link card, without an unverified completed-install badge.

**EN:** For your next video, say: use Conny Explainer Video to explain my Cursor skills, Swiss style, five minutes, bilingual subtitles.

**ZH:** 下次制作时，你可以说：使用 Conny Explainer Video，用瑞士风格解释我的 Cursor 技能，五分钟，中英双语字幕。

**EN:** Our workflow separates three roles. The director checks the facts and teaching sequence. The designer turns those ideas into frames. The engineer builds timing, narration, captions, and the final render.

**ZH:** 我们的工作流分成三个角色：导演核实事实并安排讲解顺序，设计师把这些想法变成画面，工程实现则负责时间安排、旁白、字幕和最终渲染。

**EN:** Review a sample, adjust the saved preferences, and reuse the improved recipe next time.

**ZH:** 检查样片，调整保存的偏好，下次就能复用这份改进后的食谱。

**Evidence:** User objective: short future request and reusable workflow; Proposed production workflow; no uploader attribution; SOURCES.md
