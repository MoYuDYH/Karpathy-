import os
from openai import OpenAI

# 1. 初始化 AI 客户端 (这里以 DeepSeek 为例，如果你用别的，改 base_url 和 key)
client = OpenAI(
    api_key="", 
    base_url="https://api.deepseek.com/v1"
)

def compile_knowledge_base():
    # 读取你刚刚生成的“生肉”文本
    with open("all_raw_data.txt", "r", encoding="utf-8") as f:
        raw_data = f.read()

    print("🚀 正在把知识发送给 AI 编译，请稍候（根据文本长度可能需要 1-3 分钟）...")

    # 2. 编写 Prompt (这是作业 25 分的核心！)
    system_prompt = """
    你是一个知识库编译器。请阅读用户提供的原始资料，完成以下任务：
    1. 识别核心技术概念、关键人物、重要日期。
    2. 为每个核心概念撰写一个简洁的 Markdown 页面。
    3. 页面内部必须包含 [[双向链接]] 关联其他概念。
    4. 必须输出特定的格式，每个页面用 ---FILENAME: 路径--- 隔开。
    你是一个严格的知识库编译器。
    【绝对禁令】：严禁输出任何开场白、结束语或解释性文字。
    【输出要求】：你的输出必须直接以 "---FILENAME: " 开头。
    
    输出示例：
    ---FILENAME: concepts/Transformer.md---
    # Transformer
    这是一种基于 [[注意力机制]] 的模型...
    ---FILENAME: people/Karpathy.md---
    # Andrej Karpathy
    OpenAI 联合创始人，提出了 [[LLM Knowledge Base]] 范式...
    """

    # 3. 调用大模型
    response = client.chat.completions.create(
        model="deepseek-chat",  # 确保你的模型支持长文本
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"这是原始资料：\n\n{raw_data}"}
        ],
        temperature=0.5 # 调低随机性，让输出更稳定
    )

    full_output = response.choices[0].message.content

    # 4. 解析 AI 的回复并自动创建文件
    os.makedirs("wiki/concepts", exist_ok=True)
    os.makedirs("wiki/people", exist_ok=True)

    # 改进的分割逻辑
    parts = full_output.split("---FILENAME: ")
    for part in parts:
        # 如果这一段不包含分隔符 ---，说明它是 AI 说的废话，直接跳过
        if "---" not in part:
            continue
            
        try:
            # 尝试分割文件名和内容
            header, content = part.split("---", 1)
            file_path = f"wiki/{header.strip()}"
            
            # 再次检查 file_path 是否合法（防止 AI 乱写路径）
            # 如果文件名过长（超过 100 字符），通常就是解析错了，跳过
            if len(header.strip()) > 100 or "\n" in header:
                continue

            # 自动创建子目录
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content.strip())
            print(f"📄 已生成页面: {file_path}")
            
        except Exception as e:
            print(f"⚠️ 跳过无效段落: {e}")
