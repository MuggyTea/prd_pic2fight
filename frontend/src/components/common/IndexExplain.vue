<template>
  <v-container class="grey lighten-5">
    <v-row justify="center">
      <h3>こんな画像と動画が作れるよ</h3>
    </v-row>
    <v-row justify="center">
      <v-col md="10">
        <h3>これが</h3>
      </v-col>
      <v-col md="10">
        <v-card class="pa-2" outlined tile>
            <v-img
            src="../../../public/static/exsample/sample_original_image.jpg"
            max-height="500"
            class="grey darken-4"
          ></v-img>
          <v-card-title>
            アップロード画像
          </v-card-title>
        </v-card>
      </v-col>
      <v-col md="10">
        <h3>こうなります</h3>
      </v-col>
      <v-col md="10">
        <v-card class="pa-2" outlined tile>
            <v-img
            src="../../../public/static/exsample/sample_converted_image.jpg"
            max-height="500"
            class="grey darken-4"
          ></v-img>
          <v-card-title>
            勢いをつけた画像
          </v-card-title>
        </v-card>
      </v-col>
      <v-col md="10">
        <v-card class="pa-2 video__wrapper" outlined tile>
            <!-- <v-img
            src="../../../public/static/exsample/sample_video.mp4"
            max-height="300"
            class="grey darken-4"
          ></v-img> -->
          <video
          controls
          autoplay muted playsinline
          src="../../../public/static/exsample/sample_video.mp4"
          style="max-width:100%;"
          >
            <!-- <source src="../../../public/static/exsample/sample_video.mp4" type="video/mp4"> -->
            <!-- <source
            src="../../../public/static/exsample/sample_video.mp4"
            type='video/mp4; codecs="avc1.42E01E, mp4a.40.2"'
            > -->
          </video>
          <v-card-title>
            勢いをつけた動画
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>
    <!-- <v-row justify="center" v-if="!isLogin" >
            <v-col md="10">
                    <h1>まずはやってみよう！</h1>
                    <login />
            </v-col>
        </v-row> -->
  </v-container>
</template>

<script>
// import Login from '../common/Login'
export default {
  name: "IndexExplain",
  components: {
    // 'login': Login
  },
  computed: {
    // isLogin () {
    //   return this.$store.getters['auth/check']
    // }
  },
};
</script>

<style lang="scss" scoped>
.index__description__icon {
  width: 40px;
  height: 40px;
}

.video__wrapper {
    position: relative;
    // overflow: hidden;
}

.video_wrapper > video {
  // max-height: 300px;
  // max-width:100%;
  position: absolute;
    // top: 50%;
    // left: 50%;
    // transform: translateX(-50%) translateY(-50%);
    // min-width: 300px;
    // min-height: 100%;
}
</style>
