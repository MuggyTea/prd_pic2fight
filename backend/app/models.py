#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
モデル(関数、クラス、フィールド、メソッドなど)を定義する。
"""
from typing import Sized
import numpy as np
import cv2
import random
from PIL import Image as im
import os
import io
import time


def img_blur(src, selected_x_per, selected_y_per, logger, ratio=0.9, iterations=20, margin=1):
    """
    放射ブラー効果をつけた画像を生成する関数
    """
    # logger.info("start to blur: {}".format(src))
    if (type(src) == bytes):
        logger.info("src file type may be byte {} ".format(type(src)))
        # バイナリデータをnumpyの形に変形する
        nparr = np.fromstring(src, np.uint8)
        src = cv2.imdecode(nparr, cv2.IMREAD_COLOR).astype(np.float32)
        del nparr
    else:
        logger.info("src file type may be numpy.ndarray {} ".format(type(src)))
    # logger.info("blur src to narray: {}".format(nparr))
    # src = cv2.imdecode(nparr, cv2.IMREAD_COLOR).astype(np.float32)
    # del nparr
    # h, w = src.shape[0:2]
    h, w , _= src.shape
    n = iterations
    m = margin

    # 背景を作成する．お好みで255を0にすると黒背景にできる．
    bg = np.ones(src.shape, dtype=np.uint8) * 255
    bg = cv2.resize(bg, (int(m * w), int(m * h)))

    # 背景の中心に元画像を配置
    bg[int((m - 1) * h / 2):int((m - 1) * h / 2) + h, int((m - 1) * w / 2):int((m - 1) * w / 2) + w] = src

    image_list = []
    h *= m
    w *= m
    # c_x = pos[0] * m
    # c_y = pos[1] * m
    # c_x = w/2
    # c_y = h/2
    # 焦点の位置を決める
    c_x = w * float(selected_x_per) * 0.01
    c_y = h * float(selected_y_per) * 0.01

    # 縮小画像の作成
    for i in range(n):
        r = ratio + (1 - ratio) * (i + 1) / n
        shrunk = cv2.resize(src, (int(r * w), int(r * h)))
        left = int((1 - r) * c_x)
        right = left + shrunk.shape[1]
        top = int((1 - r) * c_y)
        bottom = top + shrunk.shape[0]
        bg[top:bottom, left:right] = shrunk
        image_list.append(bg.astype(np.int32))

    # 最終的な出力画像の作成
    dst = sum(image_list) / n
    dst = dst.astype(np.uint8)

    r = (1 + ratio) / 2
    dst = dst[int((1 - r) * c_y):int(((1 - r) * c_y + h) * r), int((1 - r) * c_x):int(((1 - r) * c_x + w) * r)]
    dst = cv2.resize(dst, (int(w / m), int(h / m)))
    # imageに変換
    # BytesIOで読み込んでOpenCVで扱える型にする
    # f = img_file.stream.read()
    # bin_data = io.BytesIO(dst)
    #BGRをRGBに変換.
    # file_bytes = np.asarray(bytearray(bin_data.read()), dtype=np.uint8)
    # dst_img = cv2.imdecode(dst, cv2.IMREAD_COLOR)
    #BGRをRGBに変換.
    # dst_img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    # cv2.imwrite('upload.jpg', dst)
    return dst, h, w


def pic2mp4(pic_list, video_name, logger, img_size_y=256, img_size_x=256):
    """
    複数枚の画像から動画を作成する関数
    """
    # 動画作成の準備
    logger.info("frame size x {0}, y {1}".format(img_size_x, img_size_y))
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
    video = cv2.VideoWriter(video_name, fourcc, 6.0, (int(img_size_x), int(img_size_y)))

    # 画像のリストを一枚ずつ読み込む
    for i, pic in enumerate(pic_list):
        # logger.info("{} 枚目".format(i))
        # logger.info("画像パス {}".format(pic))
        img = cv2.imread(pic)
        # logger.info("画像を変換 {}".format(img))
        # 動画に書き込む
        video.write(img)
    # 出力
    video.release()
    return video
