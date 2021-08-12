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
            @change="onFilePicked"
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
        :original_image_obj="imageURL"
        :original_image="imageFile"
        :converted_image="converted_image"
      />
        <!-- </v-flex> -->
    </div>
</template>

<script>
import axios from "axios"
// import NotFound from "./pages/NotFound"
import CONSTANT from "./constans/index"
import firebase from 'firebase'
import firestore from '../plugins/firebase'
import PhotoResult from '../components/PhotoResult'
// import mitt from "mitt"
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
      converted_image: null
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
    onFilePicked (event) {
      // フォームでファイルが選択されたら実行される
      console.log(event.target.files)
      if (event.target.files.length === 0) {
        console.log(event.target.files.length)
        return false
      }
      // ファイルが画像でなかったら処理中断
      if (!event.target.files[0].type.match('image/*')) {
        console.log(event.target.files[0].type)
        return false
      }
      // ファイルリーダーを立ち上げる
      const reader = new FileReader()
      reader.readAsDataURL(event.target.files[0])
      reader.addEventListener('load', () => {
        this.imageURL = reader.result
        this.imageFile = event.target.files[0]
        this.imageName = event.target.files[0].name
        console.log(this.preview)
        // this.uploadPhoto()
      })
      // 画像が読み込まれたタイミングで実行される
      reader.onload = e => {
        // previewに読み込み結果（データURL）を代入する
        // previewに値が入ると<output>につけたv-ifがtrueと判定される
        // また、<output>内部の<img>のsrc属性はpreviewの値を参照しているので、結果として画像が表示される
        this.preview = e.target.result
        console.log(this.preview)
      }
      // ファイルを読み込む
      // 読み込まれたファイルはデータURL形式で受け取れる（上記onload参照）
      reader.readAsDataURL(event.target.files[0])
    },
    // 画像アップロード処理
    uploadPhoto () {
      // ストレージオブジェクト作成
      const storageRef = firebase.storage().ref()
      // ファイルパス設定
      // eslint-disable-next-line no-template-curly-in-string
      const mountainRef = storageRef.child('originalImage/' + this.imageFile.name)
      // ファイルを適用してファイルアップロード
      mountainRef.put(this.imageFile).then(snapshot => {
        snapshot.ref.getDownloadURL().then(downloadURL => {
          this.imageURL = downloadURL
          console.log(this.imageURL)
          firestore.collection('Images').add({
            'originalPhotoURL': downloadURL
          })
        })
      })
    },
    ConvertPhoto () {
      if (this.processing) return
      this.processing = true
      this.uploadPhoto ()
      // const vm = new Vue();
      // this.mitt().emit('original_image', this.imageFile)
      // POST送信する
      // axios.post(
      //   "/convert_img",
      //   {
      //     "original_image": this.imageFile
      //   }
      // )
      axios.post(
        "/convert_img",
        
        this.imageFile
        
      )
      // 送信完了
        .then((res) => {
          this.converted_image = res.data
          this.processing = false
          // this.mitt().emit('converted_image', this.converted_image)
          console.log(this.converted_image)
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
              window.location.reload()
          }).catch(err => {
            console.log("error: ", err)
          })
        })
    }
  }
}
</script>
