<template>
  <div class="twigene-list">
    <user-profile
    v-bind:user_profile="screen_name"
     />
    <v-card>
      <v-container fluid grid-list-md>
        <v-layout row wrap>
          <!-- <h1>Index</h1> -->
          <div class="row justify-content-center">
            <twigene-card v-for="(twigene, index) in tweets" v-bind:key="index" v-bind:twigene="twigene"></twigene-card>
          </div>
        </v-layout>
      </v-container>
    </v-card>
    <!-- <div class="row__test__delete">
      <button
        class="btn-sm btn-dark m-1"
        v-for="(link, index) in links"
        v-bind:key="index"
        v-on:click="remove(link.id)"
      >{{ index }}</button>
    </div> -->
  </div>
</template>

<script>
import UserProfile from '../UserProfile'
import TwigeneCard from '../TwigeneCard'

export default {
  name: 'UserPage',
  components: {
    'user-profile': UserProfile,
    'twigene-card': TwigeneCard
  },
  // data () {
  //   return {
  //   }
  // },
  props: [
    'screen_name'
  ],
  // pathの:idを直接書き換えた時の対応
  beforeRouteUpdate (to, from, next) {
    // 動的セグメントが変わった場合は、コールバック関数でtargetIdを更新する
    this.screen_name = to.params.screen_name
    next()
    this.init()
    this.start(this.screen_name)
    this.getUser(this.screen_name)
  },
  mounted () {
    this.init()
    this.start(this.screen_name)
    // this.getUser(this.screen_name)
  },
  destroyed () {
    this.stop()
  },
  methods: {
    init () {
      this.$store.dispatch('tweets/clear')
    },
    start (screenName) {
      this.$store.dispatch('tweets/startListener', {screenName})
    },
    stop () {
      this.$store.dispatch('tweets/stopListener')
    },
    remove (id) {
      this.$store.dispatch('tweets/deleteLink', {id})
    },
    getUser (userProfile) {
      this.$store.dispatch('user/userData', {screen_name: userProfile})
    }
  },
  // computedには結果がキャッシュされる
  // getterには引数は渡せない
  // ゲッター
  computed: {
    userinfo () {
      return this.$store.getters['auth/user']
    },
    isLogin () {
      return this.$store.getters['auth/check']
    },
    tweets () {
      return this.$store.getters['tweets/data']
    },
    userdata () {
      return this.$store.getters['user/userProfile']
    }
  }
}
</script>
<style>
/* .link-list {
  margin: auto;
} */

.row__test__delete {
  margin: auto;
}
</style>
