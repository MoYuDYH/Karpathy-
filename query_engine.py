import os
from openai import OpenAI

# 1. 初始化客户端（建议和 compiler.py 保持一致）
client = OpenAI(
    api_key="sk-c22ba9da38b04376b4b7861d94fb8a98", 
    base_url="https://api.deepseek.com/v1",
    timeout=600.0, # 这里单位是秒，给它 10 分钟思考时间
)

def load_full_wiki(wiki_dir):
    """把整个 wiki 目录下的 md 文件合成一个超长字符串"""
    full_content = ""
    for root, dirs, files in os.walk(wiki_dir):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    # 加上文件名作为标识，方便 AI 溯源
                    full_content += f"\n\n--- 文件名: {file} ---\n"
                    full_content += f.read()
    return full_content

def ask_question(question):
    # 加载全部编译好的知识
    wiki_context = load_full_wiki("./wiki")
    
    print("🤔 AI 正在检索整个知识库...")

    # 构建长上下文 Prompt
    system_prompt = f"""
    你是一个基于个人知识库的“专家级助理”。
    你的大脑现在由两部分组成：1. 用户提供的专属知识库（核心）；2. 你作为大语言模型的通用专业知识。

    --- 以下是用户的完整知识库内容 ---
    {wiki_context}
    --- 知识库内容结束 ---

    请遵循以下原则回答用户问题：
    
    1. 【核心依据】：首选知识库中的内容进行回答。如果知识库提到了相关技术细节，必须优先使用，并在句末标注 [来源: 文件名.md]。
    
    2. 【补充增强】：如果知识库的内容比较简略，你可以调用你的通用知识库进行“扩充”和“解释”。
       - 例如：知识库只提到“STM32H7”，你可以补充其高频性能、双精度浮点运算等背景知识，帮助用户理解，但请注明这些是补充背景。
    
    3. 【逻辑推理】：允许你跨文档进行对比和推理。
       - 例如：如果 A 文档讲 ADC，B 文档讲 DMA，用户问如何高效采样，你应该结合两者的知识给出“DMA+ADC”的综合建议。
    
    4. 【诚实原则】：如果用户问的问题与知识库完全无关，且你也无法给出准确的技术建议，请直说“知识库中未记录，根据通用知识建议如下...”。

    回答要求：专业、严谨、逻辑清晰。对于代码示例，请优先给出符合知识库描述的代码风格。
    """

    response = client.chat.completions.create(
        model="deepseek-chat", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    while True:
        user_query = input("\n请输入你的问题（输入 'exit' 退出）: ")
        if user_query.lower() == 'exit':
            break
        
        answer = ask_question(user_query)
        print("\n✨ AI 的回答：\n")
        print(answer)
        print("\n" + "="*50)