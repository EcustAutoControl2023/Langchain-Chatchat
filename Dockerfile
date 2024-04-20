# Base Image
FROM python:3.11.8
# Labels
LABEL maintainer=chatchat
# Environment Variables
ENV HOME=/Langchain-Chatchat
# Commands
WORKDIR /
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    mkdir -p $HOME
# Copy the application files
COPY . $HOME
WORKDIR $HOME
# Install dependencies from requirements.txt
RUN pip3 install -r mamba.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    mv ./modifiedpkgs/encrypted_cookie_manager.py /usr/local/lib/python3.11/site-packages/streamlit_cookies_manager/encrypted_cookie_manager.py && \
    mv ./modifiedpkgs/messages.py /usr/local/lib/python3.11/site-packages/streamlit_chatbox/messages.py && \
    mv ./modifiedpkgs/widgets.py /usr/local/lib/python3.11/site-packages/streamlit_login_auth_ui/widgets.py

EXPOSE 22 7861 8501
ENTRYPOINT ["python", "startup.py", "-a"]
