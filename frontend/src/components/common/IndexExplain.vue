<template>
  <v-container class="grey lighten-5">
    <v-row justify="center">
      <v-col md="10">
        <h1>Sample</h1>
      </v-col>
      <v-col md="10">
        <h2>これが</h2>
      </v-col>
      <v-col md="10">
        <v-card class="pa-2" outlined tile>
            <v-img
            src="../../../public/static/exsample/sample_original_image.png"
            max-height="500"
            class="grey darken-4"
          ></v-img>
          <v-card-title>
            Before
          </v-card-title>
        </v-card>
      </v-col>
      <v-col md="10">
        <h2>こうなります</h2>
      </v-col>
      <v-col md="10">
        <v-card class="pa-2" outlined tile>
            <v-img
            src="../../../public/static/exsample/sample_converted_image.png"
            max-height="500"
            class="grey darken-4"
          ></v-img>
          <v-card-title>
            After Image
          </v-card-title>
        </v-card>
      </v-col>
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
          src="../../../public/static/exsample/sample_video.mp4"
          >
            <!-- <source
            src="../../../public/static/exsample/sample_video.mp4"
            type='video/mp4; codecs="avc1.42E01E, mp4a.40.2"'
            > -->
          </video>
          <v-card-title>
            After Video
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
</style>
