<template>
    <v-container class="grey lighten-5">
        <v-row
            no-gutters
            justify="center"
        >
            <v-col
                cols="4"
                md="5"
            >
                <font-awesome-icon
                class="index__description__icon"
                :icon="['fas', 'ghost']">
                </font-awesome-icon>
            </v-col>
            <v-col
                cols="4"
                sm="5"
            >
                <font-awesome-icon
                class="index__description__icon"
                :icon="['fas', 'chart-bar']">
                </font-awesome-icon>
            </v-col>
        <v-row justify="center">
            <v-col md="10">
                <h2>最新の投稿ランキング</h2>
            </v-col>
        </v-row>
        </v-row>
        <v-row justify="center">
            <v-col md="10">
                <h3>
                <v-list rounded>
                <v-list-item
                    class="pa-3"
                    outlined
                    tile
                    v-for="(recentPost, index) in recentPosts"
                    :key="recentPost.id"
                >
                <v-list-item-title>
                <!-- <router-link
                    class="ranking__title"
                    v-bind:to="{name: 'UserPage',
                    params: {screen_name: recentPost}}"> -->
                {{index + 1}} 位 
                    <v-row justify="center">
                    <v-col md="10">
                        <v-card class="pa-2" outlined tile>
                            <img
                            :src="recentPost.converted_image_URL"
                            class="grey darken-4 setting__image"
                        >
                        </v-card>
                    </v-col>
                    </v-row>
                    <!-- <v-row justify="center">
                    <v-col md="10">
                        <v-card class="pa-2" outlined tile>
                        <video
                        max-height="500"
                        controls
                        autoplay muted playsinline
                        :src="recentPost.converted_video"
                        >
                        </video>
                        </v-card>
                    </v-col>
                    </v-row> -->
                <!-- </router-link> -->
                </v-list-item-title>
                </v-list-item>
                </v-list>
                </h3>
            </v-col>
        </v-row>
        <!-- <v-row
            no-gutters
            justify="center"
        >
            <v-col
                cols="4"
                md="5"
            >
                <font-awesome-icon
                class="index__description__icon"
                :icon="['fas', 'ghost']">
                </font-awesome-icon>
            </v-col>
            <v-col
                cols="4"
                sm="5"
            >
                <font-awesome-icon
                class="index__description__icon"
                :icon="['fas', 'chart-bar']">
                </font-awesome-icon>
            </v-col> -->
        <!-- <v-row justify="center">
            <v-col md="10">
                <h2>最近登録してくれたランキング</h2>
            </v-col>
        </v-row>
        </v-row>
        <v-row justify="center">
            <v-col md="10">
                <h3>
                <v-list>
                <v-list-item
                    center
                    class="pa-3"
                    outlined
                    tile
                    v-for="(recentUser, index) in recentUsers"
                    :key="recentUser.id"
                >
                <v-list-item-title
                >
                <router-link
                    class="ranking__title"
                    v-bind:to="{name: 'UserPage',
                    params: {screen_name: recentUser.userInfo.screen_name}}">
                {{index+1}} 位 
                {{recentUser.userInfo.screen_name}}
                </router-link>
                </v-list-item-title>
                </v-list-item>
                </v-list>
                </h3>
            </v-col>
        </v-row> -->
    </v-container>
</template>

<script>
export default {
  name: 'Ranking',
  data () {
      return {
          recentPosts: null
      }
  },
  components: {
  },
mounted () {
    this.init()
    this.start()
    this.recentPosts = this.getRecentPosts()
    // console.log(this.recentPosts())
  },
unmounted () {
    this.stop()
  },
  methods: {
    init () {
      this.$store.dispatch('user_count/clear')
    },
    start () {
    //   this.$store.dispatch('user_count/countUser')
    //   this.$store.dispatch('user_count/recentUser')
      this.$store.dispatch('user_count/recentPost')
    },
    stop () {
      this.$store.dispatch('user_count/stopListener')
    },
    getRecentPosts() {
        return this.$store.getters['user_count/recentPost']
    }
  }
//   computed: {
//     // countUsers() {
//     //     return this.$store.getters['user_count/countUser']
//     // },
//     // recentUsers() {
//     //     // console.log(this.$store.getters['user_count/recentUser'])
//     //     return this.$store.getters['user_count/recentUser']
//     // },
//     recentPosts() {
//         return this.$store.getters['user_count/recentPost']
//     }
//   }
}
</script>

<style scoped>
.index__description__icon {
    width: 40px;
    height: 40px;
}

.ranking__title {
  color:#546E7A !important;
  /* text-decoration: inherit; */
}
</style>
