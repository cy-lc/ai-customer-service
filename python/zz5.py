# import streamlit as st
# s=st.title("My First App")
# name=st.text_input("请输入姓名：")
# st.write(f"你输入的姓名为：{name}")
# sex=st.radio("请选择性别：",["男","女"])
# st.write(f"你选择的性别为：{sex}")
# password=st.text_input("请输入密码：",type="password")
#
# st.write(f"你输入的密码为：{password}")
#
#
#
# #
# # data={
# #     "姓名":["陈尧","张德忠"],
# #     "学号":["001","002"],
# #     "班级":["1班","2班"]
# # }
# # st.table(data)
# import streamlit as st
#
# st.set_page_config(
#     page_title="陈尧 设计",
#     page_icon="🧊",
#     layout="wide",
#     initial_sidebar_state="expanded",
#     menu_items={
#         'Get Help': 'https://www.extremelycoolapp.com/help',
#         'Report a bug': "https://www.extremelycoolapp.com/bug",
#         'About': "# This is a header. This is an *extremely* cool app!"
#     }
# )
import streamlit as st
import os
st.set_page_config(
    page_title="陈尧 设计",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.title("ai智能伴侣")
p=st.chat_input("请输入你要问的问题：")
if p:
 st.chat_message("assistant").write(p)
 print("**************************",p)