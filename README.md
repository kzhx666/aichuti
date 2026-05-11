<h1 align="center">AI 出题中心 (AI Exam Generator) V2.5</h1>

<p align="center">
  🚀 专为中职教育打造的工业级 AI 试卷生成系统。基于双大模型驱动，独创无尘沙箱质检机制，解决长文本截断与排版难题。
</p>

<p align="center">
  <a href="https://github.com/kzhx666/aichuti/stargazers">
    <img src="https://img.shields.io/github/stars/kzhx666/aichuti?style=flat-square&color=yellow" alt="Stars">
  </a>
  <a href="https://github.com/kzhx666/aichuti/network/members">
    <img src="https://img.shields.io/github/forks/kzhx666/aichuti?style=flat-square&color=blue" alt="Forks">
  </a>
  <a href="https://github.com/kzhx666/aichuti/issues">
    <img src="https://img.shields.io/github/issues/kzhx666/aichuti?style=flat-square&color=red" alt="Issues">
  </a>
  ![Docker](https://img.shields.io/badge/Docker-Supported-2496ED?style=flat-square&logo=docker)
  ![AI](https://img.shields.io/badge/Model-DeepSeek/Kimi-67C23A?style=flat-square)
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-success?style=flat-square" alt="License">
  </a>
</p>

---

## 📑 目录 (Table of Contents)

- [✨ 功能特性](#-功能特性-features)
- [🛡️ 核心黑科技](#️-核心黑科技-core-technologies)
- [🖥️ 系统支持](#-系统支持-os-support)
- [🧠 项目架构](#-项目架构-architecture)
- [🚀 快速安装](#-快速安装-installation)
- [📂 项目结构](#-项目结构-structure)
- [❓ 常见问题](#-常见问题-faq)

---

## ✨ 功能特性 (Features)

- **🤖 双擎驱动架构**：采用“资料提取官 (如 Kimi)”与“专家命题官 (如 DeepSeek)”协作模式，先脱水提纯资料，再深度逻辑命题。
- **📝 Markdown 极速生成**：直接从上传的 Word/PDF 资料中提取知识点，一键生成符合 Markdown 标准语法的交互式试卷。
- **📄 工业级 Word 导出**：支持 LaTeX 数学公式无损转换，完美排版 ρ、θ、Δ 等符号，支持 K_软 等中文下标。
- **🔍 智能 OCR 引擎**：内置图文扫描识别功能，支持扫描件资料出题（需配置相关 API）。
- **📁 资料分类管理**：支持文件夹级别的资料归档，支持物理删除与多分类切换。

---

## 🛡️ 核心黑科技 (Core Technologies)

### 1. 🛡️ 无尘质检沙箱 (Buffer & Validate)
彻底解决大模型在生成长文本时的“断肢”问题。系统会在后端建立隐形沙箱，逐题校验 HTML 结构（`<details>` 闭合性），只有质检通过的题目才会输出到前端，确保排版 100% 纯净。

### 💓 2. 全时段防断流强心针 (Heartbeat)
针对 DeepSeek-R1 等模型长达数分钟的“深度思考”阶段，系统会自动向前端发射高频率、带载荷的心跳包，骗过 Nginx/Cloudflare 的超时踢人机制，保障生成过程永不断线。

### 🧠 3. 无限续写与记忆钢印
针对 1 号模型处理超长文档时的“怠工”问题，引入强制 KPI 考核逻辑。若输出过短，系统会自动触发“鞭策”指令，直至榨干数千字干货笔记。

---

## 🧠 项目架构 (Architecture)

````mermaid
graph TD
    A[👨‍🏫 教师控制台] -->|POST| B(FastAPI 后端引擎)
    B --> C{无尘沙箱中心}
    C -->|任务 1| D[1号 AI: 考点脱水提取]
    C -->|任务 2| E[2号 AI: 专家逻辑命题]
    C -->|任务 3| F[正则质检员: 格式修剪]
    F -->|格式校验通过| G[前端输出区]
    F -->|格式残缺| C
    G --> H[Word 排版引擎: LaTeX 转换]
    H --> I[试卷.docx 下载]
````

---

## 🚀 快速安装 (Installation)

### 📦 1. 环境准备
确保已安装 `Docker` 和 `Docker-compose`。

### ⚡ 2. 一键拉取与运行

````bash
git clone [https://github.com/kzhx666/aichuti.git](https://github.com/kzhx666/aichuti.git)
cd aichuti
docker-compose up -d --build
````

### 🎯 3. 初始化配置

* 访问：`http://您的IP:3003`
* 初始密码：`123456`
* 进入 **API 配置** 页面，填写您的 Kimi/DeepSeek API Key。

---

## 🖥️ 系统支持 (OS Support)

| 操作系统 (OS) | 架构 | 状态 | 备注 |
| :--- | :---: | :---: | :--- |
| **Debian / Ubuntu** | AMD64/ARM64 | ✅ | 强烈推荐 |
| **CentOS / RHEL** | AMD64 | ✅ | 需关闭防火墙或开放 3003 端口 |
| **Windows / macOS** | x86/ARM | ✅ | 需安装 Docker Desktop |

---

## 📂 项目结构 (Structure)

````text
aichuti/
├── backend/
│   ├── main.py             # 核心逻辑 (沙箱、质检、防断流)
│   └── ...
├── frontend/
│   ├── index.html          # 前端交互 (全净渲染引擎)
│   └── assets/             # Vue/Element-Plus 等静态资源
├── uploads/                # 资料存放物理目录
├── docker-compose.yml      # 容器编排
└── README.md               # 项目说明
````

---

## ❓ 常见问题 (FAQ)

<details>
<summary><b>Q: 为什么生成过程中屏幕会有很久不跳字？</b></summary>

这是正常现象。系统启用了 **无尘质检沙箱**。后端正在后台全速生成并实时校验题目格式。只有等一道题完整生成并修复了潜在的截断错误后，才会整题展示在屏幕上。
</details>

<details>
<summary><b>Q: 下载的 Word 里的公式还是乱码怎么办？</b></summary>

请确保您使用的是最新版本的后端代码。系统内置了强大的正则翻译官，如果发现新符号无法识别，可提交 Issue，我们会快速扩充翻译字典。
</details>

---

<p align="center">
  中职老师专属的 AI 出题神器 | 基于 FastAPI 与 Docker 构建 | MIT License
</p>
