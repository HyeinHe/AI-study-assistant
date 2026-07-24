import streamlit as st
import requests

API_KEY = st.secrets["API_KEY"]

st.title("AI 学习总结助手")
st.write("每天记录学习内容，AI 帮你写总结")

# 输入框
history = st.text_area("粘贴你今天的学习记录", 
    placeholder="例如：\nPython 2小时\nAI工具 1小时\n英语 0.5小时",
    height=150)

# 按钮
if st.button("生成总结"):
    if not history:
        st.warning("请先输入学习记录")
    else:
        with st.spinner("AI 正在总结..."):
            prompt = "我是一名大一学生，今天的学习记录如下：\n" + history
            prompt += "\n\n请严格基于上面的记录进行总结，不要添加任何没有记录的内容。"
            prompt += "\n输出格式：\n1. 总结\n2. 鼓励的话\n3. 改进建议"

            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": "Bearer " + API_KEY,
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}]
            }

                        response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            # 调试：把 API 返回的结果显示出来
            st.write("API 返回状态码：", response.status_code)
            st.write("API 返回完整内容：")
            st.json(result)
            
            if "choices" not in result:
                st.error("API 返回错误，检查 Key 或网络")
                st.stop()
                
            reply = result["choices"][0]["message"]["content"]
            st.success("总结完成！")
            st.markdown(reply)
