import firestore from '../../plugins/firebase'
import { ADD, REMOVE } from './mutation-types'
/**
 * ユーザーごとランク付けのストアモジュール
 * ユーザーごとの使用回数を検索する
 */

// DBを呼び出す
const UploadFiles = firestore.collection('UploadImages')

export default {
    namespaced: true,
    unsubscribe: null,
    state() {
        return {
            // 配列
            recentUser: [],
            countUser: [],
            recentPost: []
        }
    },
    mutations: {
        // 受け取ったデータpayloadをステートに格納
        init(state) {
            state.countUser = []
            state.recentUser = []
            state.recentPost = []
        },
        // リンク追加時
        [ADD](state, payload) {
            // DBから受け取ったデータをステートにセット
            // state.alldata.push(payload)
            state.data.push(payload)
        },
        recentUser(state, payload) {
            // state.data.push(payload)
            // link_idを追加で更新する
            state.recentUser.push(payload)
        },
        countUser(state, payload) {
            state.countUser.push(payload)
        },
        recentPost(state, payload) {
            state.recentPost.push(payload)
        },
        // 呼び出すとき
        set(state, payload) {
            const index = state.data.findIndex(link => link.id === payload.id)
            if (index !== -1) {
                state.data[index] = payload
                state.data.push(payload)
            }
        },
        // 削除時
        [REMOVE](state, payload) {
            const index = state.data.findIndex(link => link.id === payload.id)
            if (index !== -1) {
                state.data.splice(index, 1)
            }
        }
    },
    // コンポーネントはゲッターを通して状態監視する
    getters: {
        recentUser(state) {
            return state.recentUser
        },
        recentPost(state) {
            return state.recentPost
        },
        countUser(state) {
            return state.countUser
        }
    },
    actions: {
        clear({ commit }) {
            commit('init', [])
        },
        // リスナーの起動
        async countUser({ commit }) {
            // データをゲットする
            const alldata = await UploadFiles.get();

            // firestoreからユーザーごとにデータを検索する
            const groutByUser = alldata.docs
                .map(doc => doc.data())
                .reduce((prev, current) => {
                    const element = prev.find(value => value.account === current.account)
                    if (element) {
                        element.count++;
                        element.generated_text += current.generated_text
                    } else {
                        prev.push({
                            account: current.account,
                            count: 1,
                            generated_text: current.generated_text
                        });
                    }
                    return prev
                }, []);
            console.log(groutByUser)
                // ステート変更する
            commit("countUser", groutByUser)
        },
        recentPost({ commit }) {
            if (this.unsubscribe) {
                console.warn('listener is already running. ', this.unsubscribe)
                this.unsubscribe()
                this.unsubscribe = null
            }
            // firestoreからデータを検索する
            UploadFiles.orderBy("timestamp", "desc").limit(10).get()
                .then(querySnapshot => {
                    // データ１つずつ取得
                    querySnapshot.forEach((postData) => {
                        // .then(querySnapshot => {
                        // データが更新されるたびに呼び出される
                        // querySnapshot.docChanges().some(change => {
                        console.log(postData.data())
                            // ランキングに表示しないにチェックが入っていたら表示しない
                        if (postData.data().checkbox == true) {
                            return
                        }
                        // 10件をコミットする
                        commit('recentPost', postData.data())
                    })
                }, (error) => {
                    console.error(error)
                })
        },
        // リスナーの停止
        stopListener() {
            if (this.unsubscribe) {
                this.unsubscribe()
                this.unsubscribe = null
            }
        },
        addLink(payload) {
            UploadFiles.add(payload)
                .then(doc => {
                    // ミューテーションの外でステート管理しない
                    // link_idをDBに追加
                    UploadFiles.doc(doc.id).update({
                        'id': doc.id,
                        'link_id': (doc.id).substr(0, 4)
                    })
                })
                .catch(err => {
                    console.error('Error adding document: ', err)
                })
        },
        deleteLink(payload) {
            UploadFiles.doc(payload.id).delete()
                .then(() => {

                })
                .catch(err => {
                    console.error('Error removing document: ', err)
                })
        }
    }
}