import Vue from 'vue'
import Vuex from 'vuex'
// import tweets from './modules/tweets'
// import tweet from './modules/tweet'
// import auth from './modules/auth'
// import user from './modules/user'
import user_count from './modules/user-count'

Vue.use(Vuex)

const store = new Vuex.Store({
    modules: {
        // tweets: tweets,
        // tweet: tweet,
        // auth: auth,
        // user: user,
        user_count: user_count
    },
    strict: process.env.NODE_ENV !== 'production'
})

export default store