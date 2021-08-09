<template>
  <div class="index__conteiner text-center">
    <h1>自分botを作ってみよう！</h1>
    <h3 class="index__description">
      Aitter -ついじぇね-
      は、「あなたっぽい」ツイートを自動生成するサービスです。<br />ツイートすればするほど学習データが増えてあなたらしくなります
    </h3>
    <p class="index__attention">
      初めてのツイート生成は時間が掛かります。 <br />また鍵アカウントの場合、
      <br />初回ツイート生成時のみ鍵を外して頂けたら、それ以降は鍵アカウントでも使用可能です。
    </p>
    <!-- <div class="account__tweetgenerate">
        <select-getenrate-user
          @generateScreenName="generateAccountName"
        ></select-getenrate-user>
      </div>
      <generate-tweet-button
      :screen_name="generateScreenName"
      >
      </generate-tweet-button> -->
    <!-- <h2 v-if="!isLogin" class="login__attention">
        ログインするとアカウント名入力省略・過去のついじぇね生成結果が見られます
        <login />
      </h2> -->
    <!-- <div>
        <twitter-time-line></twitter-time-line>
      </div> -->
    <index-explain></index-explain>
  </div>
</template>

<script>
// import Login from '../common/Login'
// import GenerateTweetButton from '../GenerateTweetButton'
import IndexExplain from "../common/IndexExplain";
// import TwitterTimeLine from '../common/TwitterTimeLine'
// import SelectGenerateUser from '../SelectGenerateUser'
export default {
  name: "Index",
  data() {
    return {
      selectOtherUserName: "",
      selectOwnUserCheck: true,
      generateScreenName: "",
      generateAccount: "",
    };
  },
  components: {
    // 'login': Login,
    // 'generate-tweet-button': GenerateTweetButton,
    "index-explain": IndexExplain,
    // 'twitter-time-line': TwitterTimeLine,
    // 'select-getenrate-user': SelectGenerateUser
  },
  methods: {
    generateAccountName(generateAccount) {
      this.generateScreenName = generateAccount;
    },
  },
  computed: {
    // isLogin () {
    //   return this.$store.getters['auth/check']
    // },
    // userinfo () {
    //   return this.$store.getters['auth/user']
    // }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
h1 {
  font-weight: bold;
  font-size: 24px;
}
h2 {
  font-weight: bold;
  font-size: 20px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.index__description {
  font-size: small;
  padding: 10px;
}
.index__conteiner {
  margin: auto;
}
.index__attention {
  color: red;
  font-weight: bold;
}
</style>
