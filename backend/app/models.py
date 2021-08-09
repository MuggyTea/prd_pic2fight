#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
モデル(関数、クラス、フィールド、メソッドなど)を定義する。
"""
import numpy as np
import cv2
import random
from PIL import Image as im
import os
import io
import time


def img_blur(src, pos, logger, ratio=0.9, iterations=20, margin=1.3):
    """
    放射ブラー効果をつけた画像を生成する関数
    """
    # バイナリデータをnumpyの形に変形する
    nparr = np.fromstring(src, np.uint8)
    src = cv2.imdecode(nparr, cv2.IMREAD_COLOR).astype(np.float32)
    del nparr
    h, w = src.shape[0:2]
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
    c_x = pos[0] * m
    c_y = pos[1] * m

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
    # ファイルをローカルに保存
    cv2.imwrite('static/images/upload.jpg', dst)
    return dst
