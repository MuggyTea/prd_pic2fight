# See here for image contents: https://github.com/microsoft/vscode-dev-containers/blob/v0.202.3/containers/python-3/.devcontainer/base.Dockerfile
# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
# ARG VARIANT=3-bullseye
# FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# # [Optional] Allow the vscode user to pip install globally w/o sudo
# ENV PIP_TARGET=/usr/local/pip-global
# ENV PYTHONPATH=${PIP_TARGET}:${PYTHONPATH}
# ENV PATH=${PIP_TARGET}/bin:${PATH}
# RUN if ! cat /etc/group | grep -e "^pip-global:" > /dev/null 2>&1; then groupadd -r pip-global; fi \
#     && usermod -a -G pip-global vscode \
#     && umask 0002 && mkdir -p ${PIP_TARGET} \
#     && chown :pip-global ${PIP_TARGET} \
#     && ( [ ! -f "/etc/profile.d/00-restore-env.sh" ] || sed -i -e "s/export PATH=/export PATH=\/usr\/local\/pip-global:/" /etc/profile.d/00-restore-env.sh )

# # [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
# ARG NODE_VERSION="none"
# RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1

# ##### ビルド環境 #####
# FROM node:16.7.0-alpine as build-stage
# WORKDIR /prd_pic2fight/frontend
# # vue.jsのProjectをコピーする
# COPY . .
# RUN npm install
# # npm run build で distファイルが生成されるscriptがpackage.jsonにある前提
# RUN npm run build

##### Python環境
FROM python:3.9 as build-stage
# FROM ubuntu:20.04 as ubuntu_2004
USER root

#ARG project_dir=/prd_pic2fight
EXPOSE 8080:8080
#ENV APP_HOME /main.py

WORKDIR /prd_pic2fight

COPY . ./
RUN apt-get update && apt-get upgrade -y

# ENV OPENCV_VERSION="4.5.1"

RUN apt-get -qq update \
    && apt-get -qq install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libopenjp2-7-dev \
        libavformat-dev \
        libpq-dev libgl1-mesa-glx ffmpeg libsm6 libxrender1 libxext6 x264 x265
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN cd ~/ &&\
    git clone https://github.com/opencv/opencv.git &&\
    git clone https://github.com/opencv/opencv_contrib.git &&\
    cd opencv && mkdir build && cd build &&\
    cmake \
        -D BUILD_TIFF=ON \
        -D BUILD_opencv_java=OFF \
        -D WITH_CUDA=OFF \
        -D WITH_OPENGL=ON \
        -D WITH_OPENCL=ON \
        # -D WITH_IPP=ON \
        -D WITH_TBB=OFF \
        -D WITH_EIGEN=ON \
        -D WITH_V4L=ON \
        -D BUILD_TESTS=OFF \
        -D BUILD_PERF_TESTS=OFF \
        -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=$(python3.9 -c "import sys; print(sys.prefix)") \
        -D PYTHON3_EXECUTABLE=$(which python3.9) \
        -D PYTHON_INCLUDE_DIR=$(python3.9 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
        -D PYTHON_PACKAGES_PATH=$(python3.9 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
        -D PYTHON3_LIBRARY=$(find / -name libpython3.9.so) \
        # -D CMAKE_INSTALL_PREFIX=/usr/local \
        # -D PYTHON3_EXECUTABLE=/usr/local/bin/python3.9 \
        # -D PYTHON_PACKAGES_PATH=/usr/local/lib/python3.9/site-packages \
        # -D PYTHON_INCLUDE_DIR=/usr/local/include/python3.9 \
        # -D PYTHON_INCLUDE_DIR2=/usr/include/x86_64-linux-gnu/python3.9 \
        # -D PYTHON3_LIBRARY=/usr/local/lib/libpython3.9.so \
        ..\
    && make -j$(nproc) \
    && make install

# COPY . ./

CMD gunicorn --bind :PORT --workers 1 --threads 8 --timeout 0 main:app --reload

# ##### 本番環境 #####
# FROM nginx:1.13.12-alpine as nginx

# # contentsを配置するディレクトリを作成する
# WORKDIR /prd_pic2fight
# COPY --from=build-stage /prd_pic2fight/nginx ./
# RUN mkdir -p /var/log/nginx/log\
#     && mkdir /home/www\
#     && mkdir /home/www/contents

# # ビルド環境で構築されたdistディレクトリをnignxの該当のディレクトリに配置する
# COPY --from=build-stage /prd_pic2fight/dist ./

# # nginx.confファイルを配置する
# RUN rm -f /etc/nginx/conf.d/*.conf\
#     && rm -f /etc/nginx/nginx.conf\
#     && cp -i *.conf /etc/nginx

# # RUN cp -i /prd_pic2fight/*.conf /etc/nginx

# EXPOSE 80 443 8080
# CMD ["nginx", "-g", "daemon off;","-c","/etc/nginx/nginx.conf"]
