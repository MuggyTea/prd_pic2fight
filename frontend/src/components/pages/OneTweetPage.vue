<template>
  <div class="details container-fluent text-center">
    <div class="col">
        <h class="card-title">{{ tweet.screen_name }}</h>
      <div class="card-body text-left">
        <p class="card-text" v-html="formatedDescription" />
        <hr class="mb-3" />
        <small>Release Date. {{ tweet.created_at }}</small>
      </div>
      <div class="card-footer text-right">
        <button class="btn btn-primary" v-on:click="historyBack">back</button>
      </div>
    </div>
  </div>
</template>

<script>
import CONSTANS from '../constants/'
export default {
  name: 'OneTweetPage',
  data: function () {
    return {
      // 監視対象のidをdataプロパティにtargetIdとして定義
      // targetIdはpropsのidで更新する
      targetId: this.id
    }
  },
  // routeの動的セグメント
  props: [
    'tweet_id',
    'id',
    'screen_name'
  ],
  // pathの:idを直接書き換えた時の対応
  beforeRouteUpdate (to, from, next) {
    // 動的セグメントが変わった場合は、コールバック関数でtargetIdを更新する
    console.log('URL書き換え')
    this.targetId = to.params.id
    next()
  },
  mounted () {
    console.log('mounted')
    this.init()
    this.start()
  },
  destroyed () {
    this.stop()
  },
  methods: {
    init () {
      this.$store.dispatch('tweet/clear')
    },
    start () {
      this.$store.dispatch('tweet/startListener', {tweet_id: this.targetId})
    },
    stop () {
      this.$store.dispatch('tweet/stopListener')
    },
    historyBack () {
      this.$router.back()
    }
  },
  computed: {
    userinfo () {
      return this.$store.getters['auth/user']
    },
    tweet () {
      if (!this.targetId) {
        console.error('invalid id')
        console.error(this.targetId)
        console.log(this.id)
        console.log(this.tweet_id)
        return CONSTANS.ERROR_MEMO
      }
      console.log('link() sotore getter ')
      console.log(this.$store.getters['tweet/data'])
      return this.$store.getters['tweet/data']
    },
    platforms () {
      return CONSTANS.PLATFORMS
    },
    formatedDescription () {
      if (!this.tweet.generated_text) {
        return ''
      }
      return this.tweet.generated_text
    },
    formatedReleasedAt () {
      if (!this.tweet.created_at) {
        console.log('releaseAt is none')
        console.log(this.tweet.created_at)
        return ''
      }
      return this.$moment(this.tweet.created_at).format('YYYY/MM/DD-HH:MM:SS')
    }
  },
  watch: {
    'tweet' (n, o) {
      if (!n) {
        this.$router.push(':screen_name')
      }
    }
  }
}
</script>
