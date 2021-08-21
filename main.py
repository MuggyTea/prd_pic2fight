#!/usr/bin/env python
# -*- coding: utf-8 -*
from flask import Flask, render_template, request, make_response, send_file
from flask_cors import CORS, cross_origin
from backend.app.settings.logging_prd import logging_setting
from backend.app.settings.firebase import db, timestamp
from backend.app.func.connect_firestorage import upload_bucket_file, download_bucket_file
import traceback
from backend.app.models import img_blur, pic2mp4
from PIL import Image as im
import cv2
import os
import io
import time
import numpy as np
import uuid
import json
import argparse
import ffmpeg

app = Flask(__name__, static_folder='dist/static', template_folder='dist')
CORS(app, support_credentials=True)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
logger = logging_setting('/tmp')
original_local_image_file = '/tmp/org0.jpg'
original_local_image_file_variable = '/tmp/org'
converted_local_image_file = '/tmp/upload0.jpg'
converted_local_image_file_variable = '/tmp/upload'
converted_local_mp4_file = '/tmp/upload_video.mp4'
content_type_jpg = 'image/jpeg'
content_type_mp4 = 'video/mov'
db_images = db.collection("UploadImages")

def allow_file(file_name):
    return '.' in file_name and \
        file_name.rsplit('.', 1)[1].lower() in ['png', 'jpeg', 'gif', 'jpg']


# @app.route("/")
# @app.route('/index')
# def index():
#     return render_template('index.html')

@app.route("/")
@app.route('/index')
def index():
    return "hello world"


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
    r.headers.add('Access-Control-Allow-Headers', 'Crossdomain, Authorization,X-Requested-With, Origin, X-Csrftoken, Content-Type, Accept')
    r.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return r


# 画像to放射ブラー画像
@app.route('/convert_img', methods=['POST'])
@cross_origin(support_credential=True)
def output_photo():
    try:
        # uuid発行。firestoreのidと同じにする
        img_uuid = uuid.uuid4()
        # img_uuid = "sample"
        # firestorageに保存するファイル名
        original_img_url = 'OriginalImage/' +str(img_uuid)+'.jpg'
        converted_img_url = 'ConvertedImage/' +str(img_uuid)+'.jpg'
        converted_video_url = 'ConvertedVideo/' +str(img_uuid)+'.mp4'
        # 動画作成用に生成した画像を入れておくリスト
        img_list = []
        # ファイルを受け取る
        img_file = request.files['original_image']
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
        # オリジナル画像２つ作り、ローカルに保存
        for i in range(2):
            # ローカルに保存
            cv2.imwrite(original_local_image_file_variable+str(i)+".jpg", input_data_img)
            # リストに格納
            img_list.append(original_local_image_file_variable+str(i)+".jpg")
        # 一枚ストレージにあげる
        original_local_image_file = original_local_image_file_variable + str(i) + ".jpg"
        # firestorageにアップロード
        original_storage_URL = upload_bucket_file(original_local_image_file, original_img_url, content_type_jpg, logger)
        logger.info('original image upload for firestorage URL: {0}, filename: {1}'.format(original_storage_URL, original_local_image_file))
        # 放射ブラーした画像を返す。引数は元画像・ぼかしの中心座標(x, y)から何px動かすか
        output_img, image_h, image_w = img_blur(f, [0, 0],logger, iterations=10)
        # ファイルをローカルに保存
        cv2.imwrite(converted_local_image_file, output_img)
        logger.info('blur output image: {0}, type {1}'.format(output_img, type(output_img)))
        # firestorageにアップロード
        converted_img_storage_URL = upload_bucket_file(converted_local_image_file, converted_img_url, content_type_jpg, logger)
        logger.info('converted image upload for firestorage URL: {0}, filename: {1}'.format(converted_img_storage_URL, converted_local_image_file))
        # 動画を作るために10枚のブラー画像を作る
        for i in range(10):
            # logger.info("ready to convert image {}, {} ".format(i, converted_local_image_file_variable + str(i) + ".jpg"))
            # ファイルの読み込み
            file = converted_local_image_file_variable + str(i) + ".jpg"
            output_file = converted_local_image_file_variable + str(i+1) + ".jpg"
            f = cv2.imread(file)
            # logger.info("read image {0}, type {1}".format(f, type(f)))
            # 等倍にブラーをかけた画像を10枚作る
            output_img, image_h, image_w = img_blur(f, [0, 0],logger, iterations=10)
            # ファイルをローカルに保存
            cv2.imwrite(output_file, output_img)
            # リストに格納
            img_list.append(output_file)
        # 動画を作る
        pic2mp4(pic_list=img_list, video_name=converted_local_mp4_file, logger=logger, img_size_y=image_h, img_size_x=image_w)
        # firestorageにアップロード
        converted_video_storage_URL = upload_bucket_file(converted_local_mp4_file, converted_video_url, content_type_mp4, logger)
        logger.info('converted video upload for firestorage URL: {0}, filename: {1}'.format(converted_video_storage_URL, converted_local_mp4_file))
        # データベースに登録
        db_images.document(str(img_uuid)).set(
            {
                "id": str(img_uuid),
                "original_image_URL": original_storage_URL,
                "converted_image_URL": converted_img_storage_URL,
                "converted_video_URL": converted_video_storage_URL,
                "created_at": str(time.strftime('%Y/%m/%d %H:%M:%S')),
                "timestamp": timestamp
            }
        )
        converted_img_dic = {"original_img": original_storage_URL, "converted_img": converted_img_storage_URL, "converted_video": converted_video_storage_URL,"URI": str(img_uuid)}
        logger.info('done: {}'.format(json.dumps(converted_img_dic, ensure_ascii=False)))
        # 画像を返す
        return json.dumps(converted_img_dic, ensure_ascii=False)
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
