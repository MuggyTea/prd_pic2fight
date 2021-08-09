<template>
    <v-container class="grey lighten-5">
        <v-row justify="center">
            <v-col md="10">
                    <h1>AItter-ついじぇね-って？</h1>
            </v-col>
        </v-row>
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
                :icon="['fas', 'user-astronaut']">
                </font-awesome-icon>
            </v-col>
            <v-col
                cols="4"
                sm="5"
            >
                <font-awesome-icon
                class="index__description__icon"
                :icon="['fas', 'comment-dots']">
                </font-awesome-icon>
            </v-col>
        <v-row justify="center">
            <v-col md="10">
                <h2>自分ロボットを作ってみよう！</h2>
            </v-col>
        </v-row>
        </v-row>
        <v-row justify="center">
            <v-col md="10">
                <v-card
                    class="pa-2"
                    outlined
                    tile
                >
                    機械学習を使ってあなたのツイートを解析し、<br>まるで自分が書いたかのようなツイートを自動生成するツイートジェネレーターです。
                </v-card>
            </v-col>
        </v-row>
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
                :icon="['fas', 'dove']">
                </font-awesome-icon>
            </v-col>
            <v-col
                cols="4"
                sm="5"
            >
                <font-awesome-icon
                class="index__description__icon"
                :icon="['fab', 'twitter']">
                </font-awesome-icon>
            </v-col>
        <v-row justify="center">
            <v-col md="10">
                <h2>遊ぶたびに精度が上がります</h2>
            </v-col>
        </v-row>
        </v-row>
        <v-row justify="center">
            <v-col md="10">
                <v-card
                    class="pa-2"
                    outlined
                    tile
                >
                    ツイート生成するたびに現在のツイートを集計するので、<br>ツイート数が増えれば増えるほど、ついじぇねの精度は上がっていきます
                </v-card>
            </v-col>
        </v-row>
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
                <h2>初めてのツイート生成には時間がかかります</h2>
            </v-col>
        </v-row>
        </v-row>
        <v-row justify="center">
            <v-col md="10">
                <v-card
                    class="pa-2"
                    outlined
                    tile
                >
                    3200ツイートを解析するので、2~5分ほど時間がかかります。<br>
                    バックグラウンドで動作するので、一度生成ボタンを押したらブラウザを閉じても大丈夫です。<br>
                    ２回目以降は時間はかかりません。
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
  name: 'IndexExplain',
  components: {
    // 'login': Login
  },
  computed: {
    // isLogin () {
    //   return this.$store.getters['auth/check']
    // }
  }
}
</script>

<style scoped>
.index__description__icon {
    width: 40px;
    height: 40px;
}
</style>
