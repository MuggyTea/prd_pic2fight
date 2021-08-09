<template>
  <div class="twigene-list">
      <v-container fluid grid-list-md>
        <v-layout row wrap>
          <!-- <h1>Index</h1> -->
          <div class="row justify-content-center">
            <twigene-card v-for="(twigene, index) in alltweets" v-bind:key="index" v-bind:twigene="twigene"></twigene-card>
          </div>
        </v-layout>
      </v-container>
  </div>
</template>

<script>
import TwigeneCard from '../TwigeneCard'

export default {
  name: 'AllTweetsList',
  components: {
    'twigene-card': TwigeneCard
    // 'link-list-card': LinkListCard,
    // 'link-list-form': LinkListForm,
    // 'user-profile': UserProfile
  },
  data () {
    return {
    }
  },
  // pathの:idを直接書き換えた時の対応
  beforeRouteUpdate (to, from, next) {
    // 動的セグメントが変わった場合は、コールバック関数でtargetIdを更新する
    this.screen_name = to.params.screen_name
    this.init()
    this.start()
    next()
  },
  mounted () {
    this.init()
    this.start()
  },
  destroyed () {
    this.stop()
  },
  methods: {
    init () {
      this.$store.dispatch('tweets/clear')
    },
    start () {
      this.$store.dispatch('tweets/startListenerAll')
    },
    stop () {
      this.$store.dispatch('tweets/stopListener')
    },
    remove (id) {
      this.$store.dispatch('tweets/deleteLink', {id})
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
    alltweets () {
      return this.$store.getters['tweets/alldata']
    }
  }
}

</script>
