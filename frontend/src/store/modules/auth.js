/**
 * ログイン済みユーザーを管理するストア
 */
import firestore from '../../plugins/firebase'
import firebase from 'firebase'

// DBを呼び出す
const TwitterUsersInfo = firestore.collection('TwitterUsersInfo')
const currentUserInfo = firestore.collection('currentUserInfo')

const state = {
    user: null
}

const getters = {
    // ログインチェック
    check: state => !!state.user,
    // ログインユーザー
    user: state => state.user ? state.user : null
}

const mutations = {
    setUser(state, user) {
        state.user = user
    }
}

const actions = {
    async login(context) {
        // twitterログイン
        const provider = new firebase.auth.TwitterAuthProvider()
            // await firebase.auth().signInWithPopup(provider)
            // アプリ内ブラウザでもログインできるようにリダイレクトで呼び出す
        await firebase.auth().signInWithRedirect(provider)
    },
    async logout(context) {
        await firebase.auth().signOut()
        context.commit('setUser', null)
    },
    async currentUser(context, nowUser) {
        // ログインしていたら、認証情報からDBを引く
        if (!nowUser) {
            context.commit('setUser', null)
        } else {
            // ログイン後の処理
            await firebase.auth().getRedirectResult().then((userCredential) => {
                    if (!userCredential.user) {
                        // ログイン済だったらそのまま返す
                        return
                    }
                    // ユーザー情報を取り出す
                    const userInfo = userCredential.additionalUserInfo.profile
                        // firestoreに送る
                    TwitterUsersInfo.doc(userInfo.id_str).get()
                        .then(function(docs) {
                            // 新規ユーザーだったらDBに登録
                            if (docs.exists) {
                                console.log('exsting user')
                            } else {
                                TwitterUsersInfo.doc(userInfo.id_str).set({
                                        userInfo,
                                        'timestamp': firebase.firestore.FieldValue.serverTimestamp()
                                    }, { merge: true })
                                    .then(doc => {
                                        // ミューテーションの外でステート管理しない
                                    })
                            }
                        })
                        // currentUserテーブルに登録
                    firebase.auth().onAuthStateChanged(function(user) {
                        if (user) {
                            // firestoreに送る
                            if (!userInfo.profile_banner_url) {
                                userInfo.profile_banner_url = null
                            }
                            const payload = {
                                'displayName': user.displayName,
                                'photoURL': user.photoURL,
                                'backgroundPhoto': userInfo.profile_banner_url,
                                'uid': user.uid,
                                'screenName': userInfo.screen_name,
                                'description': userInfo.description,
                                'id_str': userInfo.id_str,
                                'twitterURL': 'https://twitter.com/' + userInfo.screen_name,
                                'timestamp': firebase.firestore.FieldValue.serverTimestamp()
                            }
                            currentUserInfo.doc(user.uid).set(payload, { merge: true })
                                // context.commit('setUser', payload)
                                //   .then(doc => {
                                //     // ミューテーションの外でステート管理しない
                                //   })
                        } else {
                            context.commit('setUser', null)
                        }
                    })
                })
                .catch((error) => {
                    console.log(error)
                })
            const currentUser = await currentUserInfo.doc(nowUser.uid)
            await currentUser.get().then((doc) => {
                // ステート更新
                context.commit('setUser', doc.data())
            })
        }
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}