<template>
  <div class="index__conteiner text-center">
    <h1>画像に勢いをつけるメーカー</h1>
    <h2 class="index__description">
      あなたの画像に勢いをつけます
    </h2>
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
    <set-function/>
    <index-explain></index-explain>
  </div>
</template>

<script>
// import Login from '../common/Login'
// import GenerateTweetButton from '../GenerateTweetButton'
import IndexExplain from "../common/IndexExplain";
import SetFunction from "../SetFunction"
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
    "set-function": SetFunction
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
<style lang="scss">
h1 {
  font-weight: bold;
  font-size: 24px;
}
h2 {
  font-size: 18px;
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
  // font-size: small;
  font-size: 18px;
  padding: 10px;
}
.index__conteiner {
  margin: auto;
  padding: 20px;
}
.index__attention {
  color: red;
  font-weight: bold;
}
</style>
