<template>
    <v-container class="twitter-widget">
    <p>製作者Twitter<br>お問い合わせはDMリプライお気軽にどうぞ〜</p>
    <v-timeline
      :id="twitterId"
      :source-type="'profile'"
      :options="{ 'height': twitterHeight }" />
    </v-container>
</template>

<script>
import { Timeline } from 'vue-tweet-embed'

export default{
  components: {
    'v-timeline': Timeline,
  },
  data() {
    return {
      twitterId: 'MuggyTeaa',
      twitterHeight: '400',
    }
  },
}
</script>

<style scoped>
.twitter-widget {
  padding: 2px 8px;
  max-width:400px;
  display: inline-block;
}
</style>
