<template>
    <!-- <div v-show="value" class="photo-form"> -->
    <div class="photo-form">
        <!-- <v-flex xs12 sm8 md4> -->
        <v-card class="elevation-12">
            <output id="position_base" class="form__output" v-if="preview">
                <img
                    class="image__preview"
                    :src="preview"
                    alt=""
                    >
                  <img
                    id="pointer_position"
                    class = "image__pointer__position"
                    src="../assets/ceter_position.png"
                    alt="中心">
            </output>
            <v-card-actions>
                <v-spacer></v-spacer>
            <v-btn
            color="primary"
            label="Select Image"
            @click="pickFile"
            v-model="imageName"
            prepend-icon="attach_file"
            >
            画像を選択
            <input
            type="file"
            style="display: none"
            ref="image"
            accept="image/*"
            @change="onFilePicked"
            />
            </v-btn>
            </v-card-actions>
            <div>焦点を合わせる位置を変えられます。</div>
            <v-card-actions>
              <v-row>
              <v-col>
              左
              <input
                type="range"
                min="0"
                max="100"
                v-model="selectedCenterX"
                @change="pointerPositionX"
              >右
              {{selectedCenterX}}
              </v-col>
              <v-col>
              上
              <input
                type="range"
                min="0"
                max="100"
                v-model="selectedCenterY"
                @change="pointerPositionY"
              >下
              {{selectedCenterY}}
              </v-col>
              </v-row>
            </v-card-actions>
            <v-card-actions>
              勢いの強さ：
            <input
              type="radio"
              name="blur"
              v-model="makeBlurVolume"
              value=0.95
            />弱い 
            <input
              type="radio"
              name="blur"
              v-model="makeBlurVolume"
              value=0.9
            />普通 
            <input
              type="radio"
              name="blur"
              v-model="makeBlurVolume"
              value=0.8
            />強い 
            <input
              type="radio"
              name="blur"
              v-model="makeBlurVolume"
              value=0.7
            />ゲキつよ
            </v-card-actions>
        </v-card>
      <v-btn
        class="amber darken-2 tweetgenerate__btn"
        dark
        @click.prevent="ConvertPhoto"
        :disabled="processing"
        :loading="processing"
        :block=true
        >Upload
      </v-btn>
      <photo-result
        :original_image_URL="original_image_storageURL"
        :converted_image_URL="converted_image_storageURL"
        :converted_video_URL="converted_video_storageURL"
      />
        <!-- </v-flex> -->
    </div>
</template>

<script>
import axios from "axios"
// import NotFound from "./pages/NotFound"
import CONSTANT from "./constans/index"
// import firebase from 'firebase'
// import firestore from '../plugins/firebase'
import PhotoResult from '../components/PhotoResult'
export default {
  name: 'PhotoUpload',
  // props: {
  //   value: {
  //     type: Boolean,
  //     required: true
  //   }
  // },
  components: {
    'photo-result': PhotoResult
  },
  data () {
    return {
      preview: null,
      photo: null,
      photo_url: null,
      dialog: false,
      imageName: '',
      imageURL: '',
      imageFile: null,
      processing: false,
      original_image_storageURL: null,
      converted_image_storageURL: null,
      converted_video_storageURL: null,
      makeBlurVolume: 0.9,
      selectedCenterX: 50,
      selectedCenterY: 50
    }
  },
  // mounted() {
  //   mitt().emit('original_image', this.imageFile)
  //   mitt().emit('converted_image', this.converted_image)
  // },
  methods: {
    pointerPositionX() {
      // console.log("横に動かすよ")
      // this.selectedCenterX = value
      // console.log(this.selectedCenterX)
      // pタグをゲット
      let pointer = document.getElementById("pointer_position")
      // console.log("pointer "+ pointer)
      // スライダーの位置によって●を動かす
      pointer.style.left = this.selectedCenterX + "%"
    },
    pointerPositionY() {
      // console.log("縦に動かすよ")
      // this.selectedCenterY = value
      // pタグをゲット
      let pointer = document.getElementById("pointer_position")
      // console.log("pointer "+ pointer)
      // スライダーの位置によって●を動かす
      pointer.style.top = this.selectedCenterY + "%"
    },
    pickFile () {
      this.$refs.image.click()
    },
    onFilePicked (event) {
      let vm = this
      this.preview = null
      console.log(event.target.files)
      // フォームでファイルが選択されたら実行される
      if (event.target.files.length === 0) {
        this.reset()
        return false
      }
      // ファイルが画像でなかったら処理中断
      if (!event.target.files[0].type.match('image/*')) {
        this.reset()
        return false
      }
    const THUMBNAIL_WIDTH = 600; // 画像リサイズ後の横の長さの最大値
    const THUMBNAIL_HEIGHT = 600; // 画像リサイズ後の縦の長さの最大値
    // 画像をリサイズする
    var image = new Image();
    var reader = new FileReader();
    this.imageURL = reader.result
    var file_info = event.target.files[0]
    // this.imageFile = event.target.files[0]
    this.imageName = event.target.files[0].name
    reader.onload = e => {
      console.log(e.target.files)
      image.src = e.target.result;
      image.onload = () => {
        console.log("イメージが読み込まれたよ")
        let width = image.width
        let height = image.height
        console.log(width)
        console.log(height)
        if(image.width > image.height){
          console.log("横長画像")
          // 横長の画像は横のサイズを指定値にあわせる
          // var ratio_w = image.height/image.width;
          var ratio_w = THUMBNAIL_WIDTH/width;
          width = THUMBNAIL_WIDTH;
          // height = THUMBNAIL_WIDTH * ratio_w;
          height = Math.round(height * ratio_w);
          console.log(width)
          console.log(height)
        } else {
          console.log("縦長画像")
          // 縦長の画像は縦のサイズを指定値にあわせる
          var ratio_h = THUMBNAIL_HEIGHT/height;
          // var ratio_h = image.width/image.height;
          // width = THUMBNAIL_HEIGHT * ratio_h;
          width = Math.round(width * ratio_h);
          height = THUMBNAIL_HEIGHT;
          console.log(width)
          console.log(height)
        }
        // width = THUMBNAIL_WIDTH;
        // height = THUMBNAIL_WIDTH;
        // サムネ描画用canvasのサイズを上で算出した値に変更
        var canvas = document.createElement('canvas');
        canvas.width = width
        canvas.height = height
        var ctx = canvas.getContext('2d');
        // // canvasに既に描画されている画像をクリア
        // ctx.clearRect(0,0,width,height);
        // // canvasにサムネイルを描画
        ctx.drawImage(image,0,0,width,height);
        // ctx.drawImage(image,0,0, image.width, image.height, 0, 0, width, height);
        var ctx_canvas = ctx.canvas
        console.log(event.target.files)
        console.log(event.target.files[0])
        console.log(file_info)
        // ファイルをリサイズする
        var resizeCanvasBlob = this.GetCanvasBlob(ctx_canvas, file_info)
        resizeCanvasBlob.then((blob) => {
          console.log(blob)
          // 外でも使えるようにする
          vm.imageFile = blob
          console.log(this.imageFile)
        }, function(err){
          console.log(err)
        })
      }
      console.log(this.imageFile)
      // previewに読み込み結果（データURL）を代入する
      // previewに値が入ると<output>につけたv-ifがtrueと判定される
      // また、<output>内部の<img>のsrc属性はpreviewの値を参照しているので、結果として画像が表示される
      this.preview = e.target.result
      // this.canvas = e.target.result
      // this.imageFile = event.target.files[0]
      this.imageName = event.target.files[0].name
      console.log(this.imageFile)
    }
    // ファイルを読み込む
    // 読み込まれたファイルはデータURL形式で受け取れる（上記onload参照）
    reader.readAsDataURL(event.target.files[0])
    },
    GetCanvasBlob(ctx_canvas, file_info) {
      return new Promise(function(resolve, reject) {
        console.log(ctx_canvas)
        ctx_canvas.toBlob((blob) => {
            var smallImage = new File([blob], file_info.name,
            {
              type: file_info.type,
              lastModified: Date.now()
            })
            console.log(smallImage)
            // this.imageFile = smallImage
            // this.imageFile.push(smallImage)
            // console.log(this.imageFile
            resolve(smallImage)
            console.log(resolve(smallImage))
            console.log(reject)
        }, file_info.type, 1)
      })
    },
    // TextToBlob(ctx_canvas, file_info, filename) {
    //   var vm = this
    //   var resizeCanvasBlob = vm.GetCanvasBlob(ctx_canvas, file_info)
    //   resizeCanvasBlob.then((blob) => {
    //     console.log(blob)
    //     // 外でも使えるようにする
    //     vm.filename = blob
    //     console.log(filename)
    //   }, function(err){
    //     console.log(err)
    //   })
    // },
    ConvertPhoto () {
      if (this.processing) return
      this.processing = true
      // this.uploadPhoto ()
      // const vm = new Vue();
      // this.mitt().emit('original_image', this.imageFile)
      let config = {
        headers: {
            'content-type': 'multipart/form-data; boundary=hogehoge',
            'X-Requested-With': 'XMLHttpRequest',
            'crossDomain': true
        }
      };
      // FormData を利用して File を POST する
      console.log(this.imageFile)
      // テキストをBlobにする
      const blur2Blob = new Blob([this.makeBlurVolume], {type: "text/plain"})
      const selected_xBlob = new Blob([this.selectedCenterX], {type: "text/plain"})
      const selected_yBlob = new Blob([this.selectedCenterY], {type: "text/plain"})
      // this.TextToBlob(this.makeBlurVolume, {"type": "text/plane", "name": "blur_volume"}, this.makeBlurVolume)
      // this.TextToBlob(this.selectedCenterX, {"type": "text/plane", "name": "selected_x"}, this.selectedCenterX)
      // this.TextToBlob(this.selectedCenterY, {"type": "text/plane", "name": "selected_y"}, this.selectedCenterY)
      let formData = new FormData();
      // formData.append('original_image', this.imageFile);
      // formData.append('blur_volume', this.makeBlurVolume);
      // formData.append('selected_x', this.selectedCenterX);
      // formData.append('selected_y', this.selectedCenterY);
      // formData.append('original_image[]', this.imageFile, "original_image");
      // // console.log(formData.getAll('original_image[]'))
      // formData.append('original_image[]', blur2Blob, "blur_volume");
      // // console.log(formData.getAll('original_image[]'))
      // formData.append('original_image[]', selected_xBlob, "selected_x");
      // // console.log(formData.getAll('original_image[]'))
      // formData.append('original_image[]', selected_yBlob, "selected_y");
      // console.log(formData.getAll('original_image[]'))
      formData.append('original_image', this.imageFile, "original_image");
      // formData.append('original_image', this.imageFile, this.imageFile);
      // console.log(formData.getAll('original_image[]'))
      formData.append('blur_volume', blur2Blob, "blur_volume");
      // console.log(formData.getAll('original_image[]'))
      formData.append('selected_x', selected_xBlob, "selected_x");
      // console.log(formData.getAll('original_image[]'))
      formData.append('selected_y', selected_yBlob, "selected_y");
      // POST送信する
      // axios.post(
      //   "/convert_img",
      //   {
      //     "original_image": this.imageFile
      //   },
      //   config
      // )
      axios.post(
        CONSTANT.API_URL+"/convert_img",
        // "/convert_img",
        formData,
        config
      )
      // 送信完了
        .then((res) => {
          console.log(res)
          console.log(res.data)
          // this.converted_image = res.data
          this.original_image_storageURL = res.data.original_img
          this.converted_image_storageURL = res.data.converted_img
          this.converted_video_storageURL = res.data.converted_video
          this.processing = false
          // this.mitt().emit('converted_image', this.converted_image)
          console.log("firestorageに入れたオリジナルイメージURL"+ this.original_image_storageURL)
          console.log("生成結果URL　"+ this.converted_image_storageURL)
          console.log("ビデオの生成結果URL　"+ this.converted_video_storageURL)
        })
        .catch(error => {
          console.log(error)
          this.processing = false
          this.generatedTweet = "ツイート生成に失敗しました。もう一度試してみてください"
          axios.post(
            CONSTANT.SLACK_SERVER_ERROR,
            JSON.stringify({
              text: this.generatedTweet + "\n" + error,
              username: this.screen_name
            }), {
              withCredentials: false,
              transformRequest: [(data, headers) => {
                delete headers.common.Authorization
                delete headers.post["Content-Type"]
                return data
              }]
              }).then(() => {
              // window.location.reload()
          }).catch(err => {
            console.log("error: ", err)
          })
        })
    }
  }
}
</script>
<style lang="scss" scoped>
.form__output {
  position: relative;
}
.form__output > .image__preview {
  max-width: 100%;
  // position: relative;
  // height: 200px;
}
.form__output > h3{
  position: absolute;
  top: 50%;
  left: 50%;
  // max-width: 100%;
  // height: 200px;
}
.form__output > .image__pointer__position {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 40%;
  height: 40%;
  transform: translate(-50%, -50%);
  // max-width: 100%;
  // height: 200px;
}
// .image__pointer__position {
//   position: absolute;
//   top: 50%;
//   left: 50%;
//   width: 10px;
//   height: 10px;
//   // max-width: 100%;
//   // height: 200px;
// }
</style>
