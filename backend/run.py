#!/usr/bin/env python
# -*- coding: utf-8 -*
from flask import Flask, render_template, request, make_response, send_file
from app.settings.logging_prd import logging_setting
import traceback
from app.models import img_blur
from PIL import Image as im
import cv2
import os
import io
import time
import numpy as np

app = Flask(__name__, static_folder='../dist/static', template_folder='../dist')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
logger = logging_setting('pic2fight_test')


def allow_file(file_name):
    return '.' in file_name and \
        file_name.rsplit('.', 1)[1].lower() in ['png', 'jpeg', 'gif', 'jpg']


@app.route("/")
@app.route('/index')
def index():
    return render_template('index.html')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# 画像to放射ブラー画像
@app.route('/convert_img', methods=['POST'])
def output_photo():
    try:
        # ファイルを受け取る
        img_file = request.files['file']
        logger.info('file data: {}'.format(img_file))
        # 画像ファイル以外は弾く
        if not allow_file(img_file.filename):
            logger.error('error file data: {}'.format(img_file))
            return 'file not allowed, only allow png, jpg, gif, jpeg'
        # ファイルの読み込み
        f = img_file.read()
        # BytesIOで読み込んでOpenCVで扱える型にする
        # f = img_file.stream.read()
        bin_data = io.BytesIO(f)
        file_bytes = np.asarray(bytearray(bin_data.read()), dtype=np.uint8)
        input_data_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        # BGRをRGBに変換
        # dst_img = cv2.cvtColor(img_file, cv2.COLOR_BGR2RGB)
        # ファイルをローカルに保存
        cv2.imwrite('static/images/orig.jpg', input_data_img)
        # 放射ブラーした画像を返す。引数は元画像・ぼかしの中心座標(x, y)
        output_img = img_blur(f, [0, 0], logger)
        # ファイルをローカルに保存
        logger.info('blur output image: {0}, type {1}'.format(output_img, type(output_img)))
        # logger.info('blur output arr: {0}, type {1}'.format(output_arr, type(output_arr)))
        # output_img.save('static/images/upload.jpg')
        # レスポンスデータを作る
        # res_img = make_response()
        res_img = make_response()
        # 放射ブラーした画像
        # res_img.data = output_img
        # ヘッダー情報追加
        # res_img.headers.set('Content-Disposition', 'attachment', filename='static/images/upload.jpg')
        # res_img.headers['Contet-Type'] = 'Image'
        logger.info('done')
        # 画像を返す
        return render_template('index.html', raw_img_url='static/images/orig.jpg', blur_img_url='static/images/upload.jpg')
    except Exception as e:
        logger.error(traceback.format_exc())
        return str(e)


# 画像to放射ブラー動画
@app.route('/convert_mp4', methods=['POST'])
def output_mp4():
    try:
        # ファイルを受け取る
        img_file = request.files['file']
        logger.info('file data: {}'.format(img_file))
        # 画像ファイル以外は弾く
        if not allow_file(img_file.filename):
            logger.error('error file data: {}'.format(img_file))
            return 'file not allowed, only allow png, jpg, gif, jpeg'
        # ファイルの読み込み
        input_data_img = img_file.read()
        # 放射ブラーした画像を返す
        output_img = img_blur(input_data_img, [0, 0])
        # # 放射ブラーした画像12枚を繋げたmp4動画を返す
        # output_mp4 = mp4_blur(input_data_img)
        # # レスポンスデータを作る
        # res_mp4 = make_response()
        # # 放射ブラーした動画
        # res_mp4.data = output_mp4
        # # ヘッダー情報追加
        # res_img.headers['Content-Disposition'] = 'inline'
        # res_img.headers['Contet-Type'] = 'video/mp4'
        # # 動画を返す
        # return res_mp4
    except Exception as e:
        logger.error(traceback.format_exc())
        return str(e)


if __name__ == '__main__':
    app.run()
