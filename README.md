注意：Deepseek API Key已删除，要加上自己的Key不然无法运行

Karpathy-Style KB: 一站式 AI 个人知识库系统
一个基于长上下文大模型（Long-context LLM）理念构建的极简知识库方案。不同于传统的 RAG（检索增强生成）碎片化模式，本项目通过全量编译原始资料，构建结构化的 Markdown 知识网格，实现更具全局逻辑的深度问答。

🌟 核心特性
全链路集成：从 PDF/TXT 原始资料上传、文本提取（Ingest）、到 AI 自动化编译（Compile）和 Web 问答，全部在一个界面完成。

长上下文架构：放弃复杂的向量数据库索引，利用现代 LLM 超长上下文能力，确保跨文档推理的连贯性。

沉浸式 UI：基于 Streamlit 构建，支持知识目录树浏览、Markdown 实时预览、流式对话。

工程化反馈：内置构建状态进度条与溯源标注，确保每一条回答都有据可查。

📂 项目结构
.
├── app.py               # Streamlit 网页端主程序
├── ingest.py            # 文本提取模块（PDF -> Text）
├── compiler.py          # 知识库编译模块（Text -> Markdown Wiki）
├── query_engine.py      # 专家级问答引擎
├── raw/                 # 原始资料存放处 (PDF, TXT)
├── wiki/                # AI 编译生成的结构化 Markdown 库
└── requirements.txt     # 项目依赖
🚀 快速开始
1. 克隆仓库
Bash
git clone https://github.com/你的用户名/你的项目名.git
cd 你的项目名
2. 安装依赖
建议使用 Python 3.10+ 环境：

Bash
pip install -r requirements.txt
3. 配置 API Key
在 query_engine.py 和 compiler.py 中填入你的 DeepSeek（或 OpenAI 兼容）API Key：

Python
client = OpenAI(api_key="YOUR_API_KEY", base_url="https://api.deepseek.com/v1")
4. 运行
Bash
streamlit run app.py
🛠️ 技术路线
Ingest (摄入)：使用 PyMuPDF 解析 raw/ 目录下的硬件手册或技术文档，清洗杂讯。

Compile (编译)：通过精心设计的 System Prompt，让 LLM 充当“图书管理员”，将文本重构为分类明确的 Markdown 节点。

Query (问答)：采用“专家顾问模式”，AI 会优先检索 wiki/ 下的内容进行回答，并标注来源文件。

📖 适用场景
电子竞赛备赛：整理芯片手册（Datasheet）、典型电路、算法笔记。

课程学习整理：将多门专业课的课件转化为互联的知识图谱。

论文/技术调研：快速扫描多篇论文并提取对比分析。

🤝 贡献与感谢
本项目灵感来源于 Andrej Karpathy 的 random_hallucinations 理念。感谢 DeepSeek 提供的强大推理能力支持。

💡 提示
建议在 compiler.py 中根据个人习惯修改 system_prompt，以获得最符合你个人审美的 Wiki 分类。

如果处理超长文档，请注意在 query_engine.py 中根据实际情况调整 timeout 参数。
