import '@babel/polyfill'
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import { createApp } from 'vue'
import vuetify from './plugins/vuetify'
// ルートコンポーネントをインポートする
import App from './App'
// ルーティングの定義をインポートする
import router from './router'
// firebase構成をインポートする
import './plugins/firebase'
// 状態管理のストアをインポートする
// import store from './store'
// CSRF対策
// import '../static/js/bootstrap'
// CSS有効化
// import moment from 'vue-moment'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
// import firebase from 'firebase'
// font awesomeをインポート
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// import VueAdsense from 'vue-adsense'

library.add(fas, fab, far)
const app = createApp(App)
app.use(router)
app.use(vuetify)
app.component('font-awesome-icon', FontAwesomeIcon)
    // Vue.component('adsense', VueAdsense)

// app.use(moment)
app.mount('#app')

app.config.productionTip = false

// let createApp = (callback) => {
//     firebase.auth().onAuthStateChanged(user => {
//         if (user) {
//             store.dispatch('auth/currentUser', user)
//         } else {
//             store.dispatch('auth/currentUser', null)
//         }
//     })

//     /* eslint-disable no-new */
//     new Vue({
//         // 他のコンポーネトから、this.$routerやthis.$storeという方法でルーターや洗濯したパラメータの情報にアクセスできる
//         'router': router,
//         'store': store,
//         components: { App },
//         vuetify,
//         template: '<App/>'
//     })
// }
// createApp()