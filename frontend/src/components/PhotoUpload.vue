<template>
    <!-- <div v-show="value" class="photo-form"> -->
    <div class="photo-form">
        <!-- <v-flex xs12 sm8 md4> -->
        <v-card class="elevation-12">
            <output class="form__output" v-if="preview">
                <img
                    :src="preview"
                    alt=""
                    max-width="200px"
                    height="200px"
                    >
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
            multiple @change="onFilePicked"
            />
            </v-btn>
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
      converted_video_storageURL: null
    }
  },
  // mounted() {
  //   mitt().emit('original_image', this.imageFile)
  //   mitt().emit('converted_image', this.converted_image)
  // },
  methods: {
    pickFile () {
      this.$refs.image.click()
    },
    onFilePicked (e) {
      const THUMBNAIL_WIDTH = 500; // 画像リサイズ後の横の長さの最大値
      const THUMBNAIL_HEIGHT = 500; // 画像リサイズ後の縦の長さの最大値
      // フォームでファイルが選択されたら実行される
      console.log(e.target.files)
      if (e.target.files.length === 0) {
        console.log(e.target.files.length)
        return false
      }
      // ファイルが画像でなかったら処理中断
      if (!e.target.files[0].type.match('image/*')) {
        console.log(e.target.files[0].type)
        return false
      }
      // ファイルリーダーを立ち上げる
      var reader = new FileReader()
      var image = new Image()
      reader.readAsDataURL(e.target.files[0])
      reader.addEventListener('load', () => {
        this.imageURL = reader.result
        this.imageFile = e.target.files[0]
        this.imageName = e.target.files[0].name
        console.log(this.preview)
        // this.uploadPhoto()
      })
      // 画像が読み込まれたタイミングで実行される
      reader.onload = (e) => {
        // previewに読み込み結果（データURL）を代入する
        // previewに値が入ると<output>につけたv-ifがtrueと判定される
        // また、<output>内部の<img>のsrc属性はpreviewの値を参照しているので、結果として画像が表示される
        this.preview = e.target.result
        console.log(this.preview)
        console.log("イメージ"+image)
        this.$refs.image.onload = () => {
          console.log("イメージだよ"+image)
          var width, height, ratio
          // 横長画像だったら横長に合わせる
          if(image.width > image.height) {
            // 縦横比を計算
            ratio = image.height/image.width
            // 縦横を決める
            width = THUMBNAIL_WIDTH
            height = THUMBNAIL_HEIGHT * ratio
          } else {
            ratio = image.width/image.height
            width = THUMBNAIL_WIDTH * ratio
            height = THUMBNAIL_HEIGHT
          }
          // サムネ描画用canvasのサイズを算出した値に変更
          let canvas = document.createElement('canvas')
          canvas.width = width
          canvas.height = height
          let ctx = canvas.getContext('2d')
          ctx.drawImage(image, 0, 0, width. height)
          // 縮小した画像を送信
          ctx.canvas.toBlob((blob) => {
            this.imageFile = new File([blob], e.target.files[0].name,
            {
              type: e.target.files[0].type,
              lastModified: Date.now()
            })
          }, e.target.files[0].type, 1)
        }
      }
      // ファイルを読み込む
      // 読み込まれたファイルはデータURL形式で受け取れる（上記onload参照）
      // reader.readAsDataURL(event.target.files[0])
    },
    // 画像アップロード処理
    // uploadPhoto () {
    //   // ストレージオブジェクト作成
    //   const storageRef = firebase.storage().ref()
    //   // ファイルパス設定
    //   // eslint-disable-next-line no-template-curly-in-string
    //   const mountainRef = storageRef.child('originalImage/' + this.imageFile.name)
    //   // ファイルを適用してファイルアップロード
    //   mountainRef.put(this.imageFile).then(snapshot => {
    //     snapshot.ref.getDownloadURL().then(downloadURL => {
    //       this.imageURL = downloadURL
    //       console.log(this.imageURL)
    //       firestore.collection('Images').add({
    //         'originalPhotoURL': downloadURL
    //       })
    //     })
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
            'content-type': 'multipart/form-data'
        }
      };
      // FormData を利用して File を POST する
      let formData = new FormData();
      formData.append('original_image', this.imageFile);
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
          this.processing = false
          // this.mitt().emit('converted_image', this.converted_image)
          console.log("firestorageに入れたオリジナルイメージURL"+ this.original_image_storageURL)
          console.log("生成結果URL"+ this.converted_image_storageURL)
        })
        .catch(error => {
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
