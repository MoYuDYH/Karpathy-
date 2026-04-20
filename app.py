import streamlit as st

import os

import shutil

import time

from ingest import process_all_files  # 确保函数名一致

from compiler import compile_knowledge_base # 确保函数名一致

from query_engine import ask_question



# ================= 1. 页面配置 =================

st.set_page_config(

    page_title="Karpathy 一站式知识库",

    page_icon="🚀",

    layout="wide"

)



# 定义路径

RAW_DIR = "./raw"

WIKI_DIR = "./wiki"

os.makedirs(RAW_DIR, exist_ok=True)



# ================= 2. 侧边栏：上传 + 浏览器 =================

with st.sidebar:

    st.subheader("📄 已上传原始文件")

   

    if os.path.exists(RAW_DIR):

        raw_files = [f for f in os.listdir(RAW_DIR) if os.path.isfile(os.path.join(RAW_DIR, f))]

       

        if raw_files:

            # 使用 st.data_editor 或简单的列表显示

            for i, f_name in enumerate(raw_files):

                col1, col2 = st.columns([0.8, 0.2])

                col1.caption(f"{i+1}. {f_name}")

               

                # 可选：加一个删除按钮，防止传错文件

                if col2.button("🗑️", key=f"del_{f_name}"):

                    os.remove(os.path.join(RAW_DIR, f_name))

                    st.toast(f"已删除 {f_name}")

                    time.sleep(1)

                    st.rerun()

        else:

            st.info("暂无原始文件")

    st.title("⚙️ 知识管理中心")

   

    with st.expander("⬆️ 上传并构建", expanded=True):

        uploaded_files = st.file_uploader("放入 PDF/TXT", accept_multiple_files=True)

       

        if st.button("🏗️ 开始自动化构建", use_container_width=True):

            if uploaded_files:

                # 建立一个状态容器，让用户看到每一步在干嘛

                with st.status("🚀 正在启动自动化构建管道...", expanded=True) as status:

                   

                    # 步骤 1: 保存文件

                    st.write("📥 正在将文件写入磁盘...")

                    for f in uploaded_files:

                        with open(os.path.join(RAW_DIR, f.name), "wb") as file:

                            file.write(f.getbuffer())

                    st.toast(f"成功接收 {len(uploaded_files)} 个文件", icon="📁")



                    # 步骤 2: 提取文本

                    st.write("🔍 正在扫描并提取文本（Ingest）...")

                    start_time = time.time()

                    all_text = process_all_files(RAW_DIR)

                    with open("all_raw_data.txt", "w", encoding="utf-8") as f:

                        f.write(all_text)

                    st.write(f"✅ 文本提取完成，共 {len(all_text)} 字符")



                    # 步骤 3: LLM 编译

                    st.write("🤖 正在通过 LLM 编译知识网络（Compile）...")

                    st.warning("这一步涉及大模型长文本处理，请耐心等待约 30-60 秒...")

                   

                    # 调用你改过解析逻辑的编译函数

                    compile_knowledge_base()

                   

                    duration = round(time.time() - start_time, 1)

                    status.update(label=f"🎉 构建成功！耗时 {duration}s", state="complete", expanded=False)

               

                # 构建后的即时反馈面板

                st.balloons() # 撒花庆祝

                st.success(f"知识库已于 {time.strftime('%H:%M:%S')} 完成更新！")

               

                # 提示用户接下来可以干嘛

                st.info("💡 现在你可以点击下方的‘目录树’预览内容，或者直接在右侧提问。")

               

                # 延迟 2 秒自动刷新界面，更新目录树

                time.sleep(2)

                st.rerun()

            else:

                st.error("❌ 错误：请先选择要上传的文件！")



    # --- 第二部分：知识库浏览器 ---

    st.subheader("📚 已有知识储备")

    if os.path.exists(WIKI_DIR):

        # 统计

        all_md = []

        for root, dirs, files in os.walk(WIKI_DIR):

            for f in files:

                if f.endswith(".md"):

                    all_md.append(os.path.join(root, f))

        st.caption(f"当前共有 {len(all_md)} 个知识节点")



        # 目录树

        sub_dirs = [d for d in os.listdir(WIKI_DIR) if os.path.isdir(os.path.join(WIKI_DIR, d))]

        for d in sub_dirs:

            with st.expander(f"📁 {d}"):

                d_path = os.path.join(WIKI_DIR, d)

                files = [f for f in os.listdir(d_path) if f.endswith(".md")]

                for f in files:

                    if st.button(f"📄 {f}", key=f"btn_{d}_{f}", use_container_width=True):

                        st.session_state.preview_content = open(os.path.join(d_path, f), "r", encoding="utf-8").read()

                        st.session_state.preview_name = f

    else:

        st.info("知识库空空如也")



# ================= 3. 主界面：预览 & 对话 =================

st.header("🧠 智能知识库对话")



# 文件预览区

if "preview_content" in st.session_state and st.session_state.preview_content:

    with st.container(border=True):

        c1, c2 = st.columns([0.9, 0.1])

        c1.subheader(f"预览: {st.session_state.preview_name}")

        if c2.button("关闭"):

            st.session_state.preview_content = None

            st.rerun()

        st.markdown(st.session_state.preview_content)

    st.divider()



# 对话显示

if "messages" not in st.session_state:

    st.session_state.messages = []



for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])



# 用户提问

if prompt := st.chat_input("基于您的知识库提问..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):

        st.markdown(prompt)



    with st.chat_message("assistant"):

        with st.spinner("AI 正在深度思考并溯源..."):

            answer = ask_question(prompt)

            st.markdown(answer)

            st.session_state.messages.append({"role": "assistant", "content": answer})