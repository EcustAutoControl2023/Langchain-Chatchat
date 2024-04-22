import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages import *
from webui_pages.dialogue.dialogue import dialogue_page, chat_box, dialogue_page_user
from webui_pages.knowledge_base.knowledge_base import knowledge_base_page
import os
import sys
from configs import VERSION
from server.utils import api_address

st.set_page_config( "损伤失效智能分析系统", os.path.join("img", "chatchat_icon_blue_square_v2.png"), initial_sidebar_state="expanded", menu_items={ 'Get Help': 'https://github.com/chatchat-space/Langchain-Chatchat', 'Report a bug': "https://github.com/chatchat-space/Langchain-Chatchat/issues", 'About': f"""欢迎使用 Langchain-Chatchat WebUI {VERSION}！""" })

# TODO: 登陆实现
from streamlit_login_auth_ui.widgets import __login__

def nav_sidebar(self):
    """
    Creates the side navigaton bar
    """
    main_page_sidebar = st.sidebar.empty()
    with main_page_sidebar:
        selected_option = option_menu(
            menu_title = '损伤失效智能分析系统',
            # menu_icon = 'list-columns-reverse',
            icons = ['box-arrow-in-right', 'person-plus', 'x-circle','arrow-counterclockwise'],
            # options = ['Login', 'Create Account', 'Forgot Password?', 'Reset Password'],
            options = ['登录', '创建账户', '忘记密码', '重置密码'],
            styles = {
                "container": {"padding": "5px"},
                "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px"}} )
    return main_page_sidebar, selected_option

def build_login_ui(self):
    """
    Brings everything together, calls important functions.
    """
    if 'LOGGED_IN' not in st.session_state:
        st.session_state['LOGGED_IN'] = False

    if 'LOGOUT_BUTTON_HIT' not in st.session_state:
        st.session_state['LOGOUT_BUTTON_HIT'] = False

    auth_json_exists_bool = self.check_auth_json_file_exists('_secret_auth_.json')

    if auth_json_exists_bool == False:
        with open("_secret_auth_.json", "w") as auth_json:
            json.dump([], auth_json)

    main_page_sidebar, selected_option = self.nav_sidebar()

    # if selected_option == 'Login':
    if selected_option == '登录':
        c1, c2 = st.columns([7,3])
        with c1:
            self.login_widget()
        with c2:
            if st.session_state['LOGGED_IN'] == False:
                self.animation()
    
    # if selected_option == 'Create Account':
    if selected_option == '创建账户':
        self.sign_up_widget()

    # if selected_option == 'Forgot Password?':
    if selected_option == '忘记密码':
        self.forgot_password()

    # if selected_option == 'Reset Password':
    if selected_option == '重置密码':
        self.reset_password()
    
    self.logout_widget()

    if st.session_state['LOGGED_IN'] == True:
        main_page_sidebar.empty()
    
    if self.hide_menu_bool == True:
        self.hide_menu()
    
    if self.hide_footer_bool == True:
        self.hide_footer()
    
    return st.session_state['LOGGED_IN']

__login__.nav_sidebar = nav_sidebar
__login__.build_login_ui = build_login_ui

__login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()

api = ApiRequest(base_url=api_address())

def set_background():
    # 设置背景图片的CSS样式
    page_bg_img = '''
    <style>
    body {
        background-image: url("back.jpg");
        background-size: cover;

    }
     .home-text {
        font-size: 20px;  /* 调整首页文本的字体大小 */
    }
    </style>
    '''
    st.markdown(page_bg_img,unsafe_allow_html=True)

# 定义开始页面
def start_page(api: ApiRequest,is_lite):
    # 调用设置背景图片的函数
    set_background()

    st.title("欢迎使用 ChatGLM WebUI")
    st.title("你的智能伙伴")
    st.title("-START-")
    # st.title("[-START-]()")
    image_path = "back.jpg"
    st.image(image_path, caption='Your Image Caption', use_column_width=True)



if __name__ == "__main__":
    is_lite = "lite" in sys.argv
    if LOGGED_IN == True:
        username= __login__obj.cookies['__streamlit_login_signup_ui_username__'] 
        st.session_state['user_id'] = username
        print(username)

        # 定义其他页面，如对话页面和知识库管理页面
        pages = {
            # "开始": {
            #     "icon": "play",
            #     "func": start_page,
            # },
            "对话": {
                "icon": "chat",
                "func": dialogue_page,
            },
        }
        if username == "admin":
            pages["知识库管理"] = {
                "icon": "hdd-stack",
                "func": knowledge_base_page,
            }

        with st.sidebar:
            st.image(
                os.path.join(
                    "img",
                    "newlogo.png"
                ),
                use_column_width=True
            )
            # TODO: 侧边栏区分用户，显示不同的功能。普通用户显示历史记录，管理员用户显示知识库管理
            selected_page = "对话"
            if username == "admin":
                st.caption(
                    f"""<p align="right">当前用户：{username}（管理员）</p>""",
                    unsafe_allow_html=True,
                )
                options = list(pages)
                icons = [x["icon"] for x in pages.values()]

                default_index = 0
                selected_page = option_menu(
                    "",
                    options=options,
                    icons=icons,
                    default_index=default_index,
                )
            else:
                st.caption(
                    f"""<p align="right">当前用户：{username}</p>""",
                    unsafe_allow_html=True,
                )
                pages["对话"] = {
                    "icon": "chat",
                    "func": dialogue_page_user,
                }

        # 在点击 "开始" 后处理页面跳转
        if selected_page in pages:
            pages[selected_page]["func"](api=api,is_lite=is_lite)

