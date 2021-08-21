<template>
     <!-- <v-card
     class="mx-auto"
     color="#FFFFFF"
     width="100%"
     > -->
     <!-- <v-card-title
     class="amber darken-2 title__displayname"
     dark
     >
       <span class="font-weight">
         {{ screen_name }} bot のツイート
       </span>
     </v-card-title>
     <v-card-text class="headline font-weight-bold text__description">
        {{ generatedTweet }}
     </v-card-text>
     <v-card-actions>
       <v-list-item class="grow">
         <v-list-item-avatar color="grey darken-3">
         <v-img
         v-if="userinfo"
         class="elevation-6"
         :src="userinfo.photoURL"
         ></v-img>
         </v-list-item-avatar>
         <v-row
         align="center"
         justify="end"
         >
         <v-btn
         class="light-blue darken-1 text-center white--text"
         @click.prevent="PostingTweet"
         :disabled="processing"
         :loading="processing"
         >
           <font-awesome-icon :icon="['fab', 'twitter']"></font-awesome-icon>
           TwitterにShare
         </v-btn>
         </v-row> -->
       <!-- </v-list-item>
     </v-card-actions>
     </v-card> -->
      <!-- <v-btn
        class="amber darken-2 tweetgenerate__btn"
        dark
        @click.prevent="TweetGenerate"
        :disabled="processing"
        :loading="processing"
        :block=true
        >Upload
      </v-btn> -->
      <!-- <v-row v-if="converted_image" justify="center"> -->
    <v-container v-if="converted_image_URL" class="grey lighten-5">
      <v-row justify="center">
      <v-col md="10">
        <h1>生成結果！</h1>
      </v-col>
      </v-row>
      <v-row justify="center">
      <v-col md="10">
        <v-card class="pa-2" outlined tile>
            <img
            :src="original_image_URL"
            class="grey darken-4 setting__image"
          >
          <v-card-title>
            Before
          </v-card-title>
        </v-card>
      </v-col>
      </v-row>
      <v-row justify="center">
      <v-col md="10">
        <h2>こうなります</h2>
      </v-col>
      </v-row>
      <v-row justify="center">
      <v-col md="10">
        <v-card class="pa-2" outlined tile>
            <img
            :src="converted_image_URL"
            class="grey darken-4 setting__image"
          >
          <v-card-title>
            After Image
          </v-card-title>
          <v-card-actions>
         <v-btn
         class="light-blue darken-1 text-center white--text"
         @click.prevent="PostingTweet"
         :disabled="processing"
         :loading="processing"
         >
           <font-awesome-icon :icon="['fab', 'twitter']"></font-awesome-icon>
           TwitterにShare
         </v-btn>
        </v-card-actions>
        </v-card>
      </v-col>
      </v-row>
      <v-row justify="center">
      <v-col md="10">
        <v-card class="pa-2" outlined tile>
            <!-- <v-img
            src="../../../public/static/exsample/sample_video.mp4"
            max-height="300"
            class="grey darken-4"
          ></v-img> -->
          <video
          max-height="500"
          controls
          autoplay muted playsinline
          :src="converted_video"
          >
            <!-- <source
            src="../../../public/static/exsample/sample_video.mp4"
            type='video/mp4; codecs="avc1.42E01E, mp4a.40.2"'
            > -->
          </video>
          <v-card-title>
            After Video
          </v-card-title>
          <v-card-actions>
            <v-btn
            class="light-blue darken-1 text-center white--text"
            @click.prevent="PostingTweet"
            :disabled="processing"
            :loading="processing"
            >
              <font-awesome-icon :icon="['fab', 'twitter']"></font-awesome-icon>
            </v-btn>
            <a :href="converted_video" :download="converted_video">
              <v-btn
              class="light-blue darken-1 text-center white--text"
              >
              <!-- <font-awesome-icon :icon="['fab', 'twitter']"></font-awesome-icon> -->
                動画をダウンロード
                </v-btn>
                </a>
            </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// import UserProfile from './UserProfile'
import axios from "axios"
// import NotFound from "./pages/NotFound"
import CONSTANT from "./constans/index"
// import firestore from '../plugins/firebase'
// import firebase from 'firebase'

export default {
  name: "GenerateTweetButton",
  components: {
    // 'user-profile': UserProfile,
    // "not-found": NotFound
  },
  data () {
    return {
      // original_image: this.original_image,
      // converted_image: this.converted_image,
      converted_video: null,
      NotFound: false,
      processing: false,
      tweetUrl: "",
      tweetText: "",
      checkbox: false,
      ishashtag: false
    }
  },
  // mounted() {
  //     // const vm = new Vue();
  //     console.log(this.original_image)

  //     // mitt().on('original_image', this.original_image)
  //     // const vm = new Vue();
  //     console.log(this.converted_image)

  //     // mitt().on('converted_image', this.converted_image)
  // },
  props: {
    original_image_URL: {
      type: String,
      default: null
    },
    converted_image_URL: {
      type: String,
      default: null
    },
    converted_video_URL: {
      type: String,
      default: null
    }
  },
  // pathの:idを直接書き換えた時の対応
  beforeRouteUpdate (to, from, next) {
    // 動的セグメントが変わった場合は、コールバック関数でtargetIdを更新する
    // this.screen_name = to.params.screen_name
    next()
  },
  methods: {
    PostingTweet () {
      if (this.processing) return
      this.processing = true
      // if (this.$store.getters['auth/user']) {
      //   var userinfo = this.$store.getters['auth/user']
      // } else {
      //   var userinfo = {
      //     'screenName': '',
      //     'displayName': '',
      //     'photoURL': ''
      //   }
      // }
      // DBに登録する
      // const UsersTweets = firestore.collection('UsersTweets')
      // const payload = {
      //       'account': userinfo.screenName,
      //       'generated_account': this.screen_name,
      //       'display_name':userinfo.displayName,
      //       'photo_url': userinfo.photoURL,
      //       'generated_text': this.generatedTweet,
      //       'created_at': this.$moment(new Date()).format("YYYY/MM/DD HH:mm:ss"),
      //       'checkbox': this.checkbox
      // }
      // console.log(payload)
      // UsersTweets.add(payload)
      .then((docRef) => {
          console.log("Document written with ID: ", docRef.id);
      })
      .catch((error) => {
          console.error("Error adding document: ", error);
      });
      this.TweetPost()
      // slackに通知
      axios.post(
        CONSTANT.SLACK_TWEET,
        JSON.stringify({
          text: this.generatedTweet,
          username: this.screen_name
        }),
        {
        withCredentials: false,
        transformRequest: [(data, headers) => {
          delete headers.common.Authorization
          delete headers.post["Content-Type"]
          return data
        }]
      }).catch(err => {
          console.log("error: ", err)
          return
        })
    },
    createTweetUrl () {
      // Twitter用のurl作成
      const url = encodeURIComponent(location.href)
      // const generatedText = encodeURI(this.generatedTweet + "\n\n")
      // ハッシュタグを付けないにチェックボックスが入っていたら、ハッシュタグを付けない
      // if (this.ishashtag == true) {
      //   this.tweetUrl = "https://twitter.com/intent/tweet?text=" + generatedText + "&url=" + url
      // } else {
      //   this.tweetUrl = "https://twitter.com/intent/tweet?text=" + generatedText + "%23ついじぇね%20%23自分bot%0A" + "&url=" + url
      // }
      this.tweetUrl = "https://twitter.com/intent/tweet?%23画像に勢いをつけるメーカー%20%23" + "&url=" + url
      return this.tweetUrl
    },
    TweetGenerate () {
      if (this.processing) return
      this.processing = true
      // POST送信する
      axios.post(
        "/convert_img",
          this.original_image
      )
      // 送信完了
        .then(() => {
          // this.converted_image = res.data
          this.processing = false
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
    },
    TweetPost () {
      if (!this.processing) {return}
      this.processing = true
      // const userinfo = this.$store.getters['auth/user']
      const tweetPage = this.createTweetUrl()
      if (!window.open(tweetPage)) {
        window.location.href = tweetPage
      } else {
        window.open(tweetPage)
      }
      this.processing = false
    },
    isTrueURL () {
      const userurl = this.$store.getters["auth/user"]
      if (userurl) {
        if (userurl.screenName === this.$route.params.screen_name) {
          this.NotFound = false
        } else {
          this.NotFound = true
        }
      } else {
        this.$router.push("/")
      }
    }
  }
  // // ゲッター
  // computed: {
  //   // isLogin () {
  //   //   return this.$store.getters['auth/check']
  //   // },
  //   // userinfo () {
  //   //   return this.$store.getters['auth/user']
  //   // }
  // }
}
</script>
<style>
.tweetlist {
  margin: auto;
  display: grid;
  width: 100%;
  height: fit-content;
}

.row__test__delete {
  margin: auto;
}

.index__description {
  /* font-size: small; */
  /* padding: 10px; */
}

.twitter__displayname {
  width: 50px;
}

.title__displayname {
  font-size: 1rem;
  color: #ffffff;
}

.text__description {
  padding-top: 16px !important;
}
.checkbox__tweetgenerate {
  font-size: 16px;
  text-align: left;
}
.setting__image {
  -webkit-touch-callout: default;
  max-width: inherit;
}
</style>
