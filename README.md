# 🛠️ 建筑材料 AI 命题中心 (AI Exam Generator)

> 一款专为中职院校《建筑材料》与土木工程专业打造的“工业级” AI 自动化出题系统。基于大语言模型（LLM），支持全量图文文档解析、智能防崩溃处理、以及纯净 Word 试卷一键生成。

## ✨ 核心特性 (Key Features)

* 🤖 **AI 智能精准命题**
    * 内置极致调优的专业教师 Prompt（提示词），强制控制单选、多选、判断题比例。
    * 深入解析每一个错误选项，提供极具教学价值的结构化答案。
* 📂 **多端绝对同步机制 (真·物理挂载)**
    * 彻底摒弃容易产生数据孤岛的前端 `LocalStorage` 存储。
    * 所有分类文件夹实时穿透到服务器物理硬盘，无论通过 IP 还是域名访问，下拉列表毫秒级无缝同步。
* 📄 **全维度文档解析 & OCR 引擎**
    * 支持大体积 `.docx` 和 `.pdf` 文档解析。
    * 可选开启原生 OCR（Tesseract）图文扫描，精准提取教材扫描件和复杂图片中的知识点。
* 🛡️ **工业级防崩溃与防断流守护**
    * **前端防线：** 核心超长提示词采用 HTML `<script type="text/plain">` 物理隔离，彻底免疫终端工具（如 Xshell 等）粘贴代码时的折行截断引发的白屏死机。
    * **后端防线：** 加入“零宽字符”(`\u200B`) 心跳包机制，在 AI 长时间深度思考时，每 5 秒向浏览器发送一次存活信号，完美穿透 Nginx/Cloudflare 的网络闲置超时（504 Gateway Timeout）限制。
    * **终极清道夫：** 前端内置无视大小写的跨行正则清洗引擎，彻底斩断大模型偶尔抽风带来的多余代码块包裹和 `list index out of range` 报错残余。
* 📥 **双版本试卷一键导出**
    * 前端实时 KaTeX 数学公式渲染。
    * 一键导出纯净排版的 Word 文档，支持“学生留白版”和带有红色高亮解析的“教师标准版”。

## 🛠️ 技术栈 (Tech Stack)

* **前端 (Frontend):** Vue 3 (CDN), Element Plus, Axios, Marked.js, KaTeX
* **后端 (Backend):** Python 3.10, FastAPI, OpenAI SDK, python-docx, pdfplumber, pytesseract
* **部署环境 (Deployment):** Docker, Docker Compose, Nginx

## 🚀 极速部署 (Quick Start)

本项目采用容器化部署，几步即可在任何 Linux 服务器（如 Ubuntu/Debian）上运行。

### 1. 克隆项目
```bash
git clone [https://github.com/kzhx666/aichuti.git](https://github.com/kzhx666/aichuti.git)
cd aichuti
```

### 2. 构建并启动服务
系统将自动拉取环境、安装 OCR 依赖并穿透挂载持久化目录。
```bash
docker-compose up -d --build
```

### 3. 访问系统
在浏览器中打开：
```text
http://你的服务器IP:3003
```
*初始安全密码为：123456（请在代码中自行修改）*

## 📖 使用指南 (Usage Guide)

1.  **API 配置：** 进入【⚙️ API 配置】面板，填写兼容 OpenAI 接口的 API URL、Key 以及模型名称（如 `glm-4`、`gpt-4o` 等），点击保存。
2.  **资料管理：** 在【📚 资料管理】中创建分类，并拖拽上传课程教材或考点总结（支持 Word/PDF）。
3.  **一键出题：** 回到主控台，选择指定资料库，点击【🚀 一键生成】，等待右侧屏幕滚动输出完美试卷！

## ⚠️ 注意事项 (Notes)

* 本项目核心依赖于服务器的 Docker 环境，请确保服务器硬盘已留出足够空间用于存储上传的 PDF/Word 资料。
* 由于 Nginx 已关闭缓冲以支持流式输出，如果使用反向代理（如 Nginx Proxy Manager），请务必在代理设置中同样关闭 `Cache` 和 `Block Exploits` 功能。

## 📄 开源协议
MIT License