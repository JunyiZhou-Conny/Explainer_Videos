# 中文字幕说明

视频 *AC215 · Lecture 18 — APIs and frontend: a FastAPI service, a simple page and a React app (follow-along: cheese-app-v1 + cheese-app-v2)*
（**AC215 · 第 18 讲：API 与前端——FastAPI 服务、简单网页和 React 应用（跟练：cheese-app-v1 + cheese-app-v2）**）是英文旁白，
配中文字幕和中英双语字幕，没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 18 讲“APIs”和“Frontend”两份课件的跟练视频，对照课件逐页讲解，
并照着教程仓库 [dlops-io/cheese-app-v1](https://github.com/dlops-io/cheese-app-v1) 和
[dlops-io/cheese-app-v2](https://github.com/dlops-io/cheese-app-v2) 的 README 一步一步做（版本见 [`ASSETS.md`](../../ASSETS.md)
“Which commit”：cheese-app-v1 的 `main` @ `ce03a10`；cheese-app-v2 的 `main` @ `447b5c3`，即 2026-11-05 学生 clone 到的版本，当天上午
`main` 动了两次；“Production images” 一节取自 `e98fa55` 的 README；教程 24“Simple Frontend App”在 `main` 上已被删掉，所以取自 `2025`
分支 = `14f2a14`，和考前精讲版 [`ac215-l16-exam`](../../../ac215-l16-exam/) 引用的是同一个 commit），分两部分：

- **第一部分（S01–S09，API）**：从一个问题开始：发往 port 3000 的请求，为什么是 API 的 uvicorn 应答的？然后是课上的蓝图和目录规则、
  clone 两个 repo、自己建好 `secrets` 和 `persistent-folder`；cheese-app-v1 里在容器中用 uvicorn 跑起 FastAPI（服务器和应用的分工、
  `api.service:app`、`--host 0.0.0.0`、`--reload`、发布的 port），把一个 Python 函数变成 URL（查询字符串、422、307、`/docs`），
  再用 `http-server` 提供静态页面；cheese-app-v2 里四个容器、一个 Docker 网络，把奶酪书的 14,356 个 chunk 载入 Chroma，启动 API，
  分清 `/healthz`（存活）和 `/readyz`（就绪），看懂 `/api` 下的 router 和 `/api/docs`，聊天怎样靠 session ID 存成文件，最后 `pytest`。
- **第二部分（S10–S16，前端）**：为什么需要框架，用 Vite 跑 React 开发服务器；Vite 代理怎样让浏览器只和同一个源（origin）打交道，
  所以 API 不需要 CORS；两阶段构建的 nginx 生产镜像取代 Vite（331 MB 对大约 95 MB）；`docker compose up --build` 一条命令启动整个应用，
  再完整清理；切到 `2025` 分支跑课上讲的简单前端，亲眼看浏览器的 CORS 预检请求和一次 307 重定向；最后是清理清单、回到课上的蓝图，
  留五道自测题。

画面上的终端输出、代码面板、README 引文、示意的浏览器窗口和各种标签（`your turn`、`extra`、`recorded`、`illustration`、金色的计费标签、
`Lecture 18 · slides …`）都是英文原样，方便你对照着敲。授课老师的名字从不出现在画面、字幕、标题、章节名和简介里。

## 怎么录制的

终端输出全部来自真实运行（`assets/terminal/`，录于 2026-11-05，详见 [`ASSETS.md`](../../ASSETS.md)），没有手打的输出。这一讲整个
跑在笔记本的 Docker 里，所以几乎每一步都是实录：两个 repo 的 clone、每个 `docker-shell.sh` 的构建和运行、uvicorn / FastAPI 的应答、
加上演示路由后的自动重载、`/api/docs`、`pytest`（26 passed）、向量数据库的加载、CNN 识别奶酪照片、3000 上的 Vite 开发服务器和它的
`/api` 代理、`npm run check`、8080 上的 nginx 生产镜像、`docker compose up --build`，以及 `2025` 分支的简单前端带着 CORS 调用去年的 API。
README 里没有、但有助于理解的检查（`curl`、`docker ps`、目录列表、`git log`、`git stash`、把 API 从网络上断开的实验）在画面上标着 `extra`。

录制机器**没有 Google 账号，也没有 GCP 项目**，录制用的密钥文件格式正确，但不属于任何账号。所以每个 Gemini 和 embedding 调用都录到它的
第一个如实的报错为止（`invalid_grant: account not found`，在 Ask 模式里是一个 500），视频不显示任何 Gemini 的回答，只说明有了你自己的
密钥之后回答出现在哪里。课件和 README、README 和实际运行不一致的地方（README 里漏了 `src` 的路径、写成 900 的 port、旧的整段 `<body>`
片段，课件把 container 内部标成 localhost:9000），以录到的为准，视频会温和地指出来。本讲不创建任何计费的云资源；只有聊天和 embedding
调用会向你自己的 Vertex AI 项目计费（金色标签标出）。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l18-apis-frontend.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本，也是上传 Bilibili 的版本 |
| `output/ac215-l18-apis-frontend.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l18-apis-frontend_part1.*`、`_part2.*` | 上下两部分（S01–S09：API；S10–S16：前端），每部分有自己的视频和字幕文件 |
| `output/ac215-l18-apis-frontend.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l18-apis-frontend.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l18-apis-frontend.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴（章节名的中文版在 `meta.yaml`） |
| `output/transcript.md` | 按章节排列的旁白全文 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文：`g1` 是第一部分（S01–S09），`g2` 是第二部分（S10–S16）；`en_display:` 是英文字幕行的显示形式 |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则（两份内容相同） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

视频和字幕要等渲染完成后才会出现在 `output/` 里。视频文件（`.mp4`）不放进 Git：剧集合并后作为 GitHub Release 的附件发布，
下载链接见 [`catalog/videos.json`](../../../../catalog/videos.json) 和 [`docs/VIDEOS.md`](../../../../docs/VIDEOS.md)；
字幕、章节和旁白全文留在 `output/` 里。练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令和中文速览在学习指南
[MLOps_Learning · guides/L18-apis-frontend.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L18-apis-frontend.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l18-apis-frontend --lang zh               # 中文译文和英文是否逐句对齐、能否通过显示检查
python -m explainer.build videos/ac215-l18-apis-frontend --render-only --jobs 3       # 渲染各场景（英文旁白）
python -m explainer.build videos/ac215-l18-apis-frontend --no-render --crf 27 --burn  # 拼接 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l18-apis-frontend --subs-only                  # 只重写字幕（改了译文之后）
```

`script.md` 里的每一行 SAY 在 `narration/*.yaml` 里对应一个条目（159 段：第一部分 89 段，第二部分 70 段），`en` 和 SAY 逐字相同；
`zh` 按 `explainer.voice.split_sentences` 切出的英文句子一句对一句（共 349 句：197 + 152），不合并、不拆分。字幕按英文旁白录下的时间显示：
双语字幕带在中文句子切开的地方，把英文句子也切在对应的位置，所以中文尽量保持英文的语序（条件、目的和时间从句留在英文放的位置）；
纯中文字幕每行最多 22 个单位、每条最多两行。SAY 为了让语音读对，把实物念成了单词（api dot service colon app、host 0.0.0.0、
square root、x equals 2 and y equals 10、slash api、healthz、node modules、Control C、access control allow origin, star……）；
这些条目（73 段：41 + 32）在 `en_display:` 里给出屏幕上的写法（`api.service:app`、`--host 0.0.0.0`、`square_root`、`x=2&y=10`、`/api`、
`/healthz`、`node_modules`、`Ctrl+C`、`access-control-allow-origin: *`……），双语字幕的英文行显示的就是它。

## 译文风格

按中国 MLOps 助教带实验课的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名和路径、URL、container / 网络 / image / volume 的名字、
README 的小节名、应用的标签页和聊天模式、状态码）一字不改，比如 `sh docker-shell.sh`、`npm run dev`、`localhost:3000`、`/api/docs`、
`cheese-app-api-service`、Backend APIs、Review the app、Docker Cleanup、Ask、Identify、Cheese books、Recent。旁白引用的日志和报错按屏幕原文照抄
（Application startup complete、CNN model is loading、Invalid grant: account not found、Internal Server Error、host not found in upstream、
26 passed），观众要在终端里找它们。

实验课上本来就说英文的词保留英文：前几讲的 repo、clone、commit、container、image、tag、port、volume、shell、registry、bucket、pipeline、
chunk、embedding、session、stash、lint，加上这一讲的 router、origin、session ID、outlet、div、CORS、JSX；其余用中文标准术语（MDN 中文版
和 Kubernetes 中文文档的译名）：前端、后端、服务器、请求、响应、状态码、请求头、路由、中间件、装饰器、类型提示、查询字符串、重定向、
静态文件、强制刷新、单页应用、组件、框架、开发服务器、构建工具、代理、预检请求、探针、存活、就绪、集群、挂载、构建缓存。几组容易混的词
始终分开：route 是“路由”，router 照说（“路由器”是网络硬件）；origin 照说，不写“源”或“域”（origin 包含协议、主机和 port）；
服务器（uvicorn、nginx、http-server）≠ 应用（FastAPI 的 app、React 应用）。视频里的比喻一个比喻一个词：许可条（CORS 的
access-control-allow-origin）、信使（第 3.5 步：转发 /api 的 Vite 或 nginx）、电话簿（Docker DNS，同第 4、10 讲）、一趟（课上的一趟）、
蓝图（课上的技术架构图）、这棵树的叶子（25 个操作）、窗口（outlet）、外壳（应用的外壳）、第 0 步（预检）。

字幕检查不允许中文行里出现下划线名字、等号、和号、加号和括号，所以几样实物在中文行里按旁白的说法写，英文行照常显示原样：`square_root` →
square root，`api_server` → API server，`uvicorn_server` → uvicorn server，`node_modules` → node modules，`x=2&y=10` → x 等于 2，y 等于 10，
`Ctrl+C` → Ctrl-C，`access-control-allow-origin: *` → access-control-allow-origin，星号。小写的实物不放在句首（“是 nginx。”“命令 git switch 2025……”）。
标题、章节名和简介用书面语体（容器、镜像、仓库、端口、源（origin）、预检请求）。双语字幕的英文原句就在中文下方，所以中文行不加英文括注。
完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 字幕里的说法 | 书面写法 / 常见的其他译法 |
| --- | --- | --- |
| server / app (uvicorn / FastAPI) | 服务器 / 应用 | 同左 |
| route / router / prefix | 路由 / router / 前缀 | 路由 / 路由器（APIRouter） / 同左 |
| query string / type hint / decorator | 查询字符串 / 类型提示 / 装饰器 | 同左 |
| trailing slash / redirect (307) | 结尾的斜杠 / 307 | 尾部斜杠 / 重定向 |
| static files / hard refresh | 静态文件 / 强制刷新 | 同左 |
| liveness / readiness probe | 存活 / 就绪探针 | 存活探针 / 就绪探针 |
| session ID | session ID | 会话 ID |
| single-page app / component / framework | 单页应用 / 组件 / 框架 | 单页应用（SPA） / 同左 |
| dev server / build tool / production build | 开发服务器 / 构建工具 / 生产构建 | 同左 |
| outlet | outlet（窗口） | 出口（React Router） |
| proxy / the courier | 代理 / 信使 | 反向代理 |
| origin | origin | 源（origin） |
| CORS / permission slip | CORS / 许可条 | 跨域资源共享 |
| preflight (step zero) | 预检（第 0 步） | 预检请求 |
| multi-stage build | 两阶段构建 | 多阶段构建 |
| phone book (Docker DNS) | 电话簿 | 容器名解析 |
