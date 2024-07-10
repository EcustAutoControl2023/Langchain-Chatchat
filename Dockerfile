# Base Image
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04
# Labels
LABEL maintainer=chatchat
# Environment Variables
ENV HOME=/Langchain-Chatchat
# Commands
WORKDIR /
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3.11 python3-pip curl libgl1 libglib2.0-0 jq && \
    apt-get install ffmpeg libsm6 libxext6  -y --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f /usr/bin/python3 && \
    ln -s /usr/bin/python3.11 /usr/bin/python3 && \
    mkdir -p $HOME
# Copy the application files
COPY . $HOME
WORKDIR $HOME
# Install dependencies from requirements.txt
RUN pip3 install -r mamba.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir
RUN pip3 install -r mamba-acc.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir

RUN mv ./modifiedpkgs/encrypted_cookie_manager.py /usr/local/lib/python3.11/dist-packages/streamlit_cookies_manager/encrypted_cookie_manager.py && \
    mv ./modifiedpkgs/messages.py /usr/local/lib/python3.11/dist-packages/streamlit_chatbox/messages.py && \
    mv ./modifiedpkgs/widgets.py /usr/local/lib/python3.11/dist-packages/streamlit_login_auth_ui/widgets.py

EXPOSE 22 7861 8501
ENTRYPOINT ["python3", "startup.py", "-a"]
