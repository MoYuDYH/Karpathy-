import os
import pdfplumber

def read_text_file(file_path):
    """读取普通的纯文本文件 (txt, md)"""
    # 这里的 encoding='utf-8' 很重要，防止中文乱码
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_pdf_file(file_path):
    """读取 PDF 文件并提取文字"""
    text_content = ""
    # 使用刚刚安装的 pdfplumber 打开 PDF
    with pdfplumber.open(file_path) as pdf:
        # 遍历 PDF 的每一页
        for page in pdf.pages:
            # 提取当前页的文字并拼接到总内容里
            page_text = page.extract_text()
            if page_text:
                text_content += page_text + "\n"
    return text_content

def process_all_files(raw_dir):
    """遍历文件夹，把所有文件内容合并成一个大字符串"""
    print(f"📁 开始扫描目录: {raw_dir} ...\n")
    
    all_knowledge = "" # 用来装所有文件内容的“大桶”
    
    # os.listdir 会列出该文件夹下所有的文件名
    for filename in os.listdir(raw_dir):
        file_path = os.path.join(raw_dir, filename)
        
        # 排除掉文件夹，只处理文件
        if os.path.isfile(file_path):
            print(f"⏳ 正在处理: {filename}")
            
            try:
                # 如果是 txt 或 md 结尾的
                if filename.endswith('.txt') or filename.endswith('.md'):
                    content = read_text_file(file_path)
                    all_knowledge += f"\n\n[来源文件: {filename}]\n{content}"
                    
                # 如果是 pdf 结尾的
                elif filename.endswith('.pdf'):
                    content = read_pdf_file(file_path)
                    all_knowledge += f"\n\n[来源文件: {filename}]\n{content}"
                    
                else:
                    print(f"⚠️ 跳过不支持的格式: {filename}")
            except Exception as e:
                print(f"❌ 处理 {filename} 时报错: {e}")

    print("\n✅ 所有文件处理完毕！")
    return all_knowledge

# ================= 程序的真正入口 =================
if __name__ == "__main__":
    raw_folder_path = "./raw" 
    
    # 1. 提取所有文本
    final_text = process_all_files(raw_folder_path)
    
    # 2. 将提取到的“生肉”存入一个文件，给后面的 Compile 阶段用
    # 如果没有这个文件，就创建一个
    with open("all_raw_data.txt", "w", encoding="utf-8") as f:
        f.write(final_text)
    
    print("-" * 40)
    print(f"✅ 提取完成！总字符数: {len(final_text)}")
    print("💾 原始内容已保存至: all_raw_data.txt")