#!/usr/bin/env python
# -*- coding: utf-8 -*
from flask import Flask, render_template, request, make_response, send_file
from backend.app.settings.logging_prd import logging_setting
from backend.app.settings.firebase import db, timestamp
from backend.app.func.connect_firestorage import upload_bucket_file, download_bucket_file
import traceback
from backend.app.models import img_blur
from PIL import Image as im
import cv2
import os
import io
import time
import numpy as np
import uuid

app = Flask(__name__, static_folder='dist/static', template_folder='dist')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
logger = logging_setting('/tmp')
original_local_image_file = '/tmp/org.jpeg'
converted_local_image_file = '/tmp/upload.jpeg'
content_type_jpg = 'image/jpeg'
content_type_mp4 = 'video/mp4'
db_images = db.collection("UploadImages")

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
        # uuid発行。firestoreのidと同じにする
        img_uuid = uuid.uuid4()
        # img_uuid = "sample"
        # firestorageに保存するファイル名
        original_img_url = 'OriginalImage/'+str(img_uuid)+'.jpg'
        converted_img_url = 'ConvertedImage/'+str(img_uuid)+'.jpg'
        converted_video_url = 'ConvertedVideo/'+str(img_uuid)+'.mp4'
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
        # BGRをRGBに変換
        # dst_img = cv2.cvtColor(img_file, cv2.COLOR_BGR2RGB)
        # ファイルをローカルに保存
        # オブジェクト名をディレクトリ名とし、実行ディレクトリと同じ階層にログファイル保存ディレクトリを作成
        # if os.path.exists(str("static/images/")) is not True:
        #     os.mkdir(str("static/images/"))
        # オリジナル画像をローカルに保存
        cv2.imwrite(original_local_image_file, input_data_img)
        # firestorageにアップロード
        original_storage_URL = upload_bucket_file(original_local_image_file, original_img_url, content_type_jpg, logger)
        logger.info('original image upload for firestorage URL: {0}, filename: {1}'.format(original_storage_URL, original_local_image_file))
        # cv2.imwrite('orig.jpg', input_data_img)
        # 放射ブラーした画像を返す。引数は元画像・ぼかしの中心座標(x, y)
        output_img = img_blur(f, [0, 0], logger)
        # ファイルをローカルに保存
        cv2.imwrite(converted_local_image_file, output_img)
        logger.info('blur output image: {0}, type {1}'.format(output_img, type(output_img)))
        # firestorageにアップロード
        converted_img_storage_URL = upload_bucket_file(converted_local_image_file, converted_img_url, content_type_jpg, logger)
        logger.info('converted image upload for firestorage URL: {0}, filename: {1}'.format(converted_img_storage_URL, converted_local_image_file))
        converted_video_storage_URL = ""
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
        converted_img_dic = {"original_img": original_storage_URL, "converted_img": converted_img_storage_URL, "URI": img_uuid}
        # 画像を返す
        return converted_img_dic
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
