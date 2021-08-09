import firestore from "../../plugins/firebase";
// import CONSTANS from '../../components/constants'
/**
 * リンクページで表示するリンク一件分のデータを管理する
 */

// DBを呼び出す
const LinkRef = firestore.collection("UsersTweets");
// const currentUserInfo = firestore.collection('currentUserInfo')

export default {
  namespaced: true,
  unsubscribe: null,
  state() {
    return {
      // 一件分なので
      data: {},
    };
  },
  mutations: {
    // 受け取ったデータpayloadをステートに格納
    init(state, payload) {
      state.data = payload;
    },
    // リンク追加時
    add(state, payload) {
      state.data.push(payload);
    },
    // 呼び出すとき
    set(state, payload) {
      const index = state.data.findIndex((link) => link.id === payload.id);
      if (index !== -1) {
        state.data[index] = payload;
      }
    },
    // 削除時
    remove(state, payload) {
      const index = state.data.findIndex((link) => link.id === payload.id);
      if (index !== -1) {
        state.data.splice(index, 1);
      }
    },
  },
  // コンポーネントはゲッターを通して状態監視する
  getters: {
    data(state) {
      return state.data;
    },
  },
  actions: {
    // clear({ commit }) {
    //     commit('init', CONSTANS.NEW_EMPTY_MEMO())
    // },
    // リスナーの起動
    startListener({ commit }, payload) {
      if (this.unsubscribe) {
        console.warn("listener is already running. ", this.unsubscribe);
        this.unsubscribe();
        this.unsubscribe = null;
      }
      console.log(payload);
      console.log(payload.tweet_id);
      // firestoreからデータを検索する
      this.unsubscribe = LinkRef.doc(payload.tweet_id).onSnapshot(function (
        doc
      ) {
        // querySnapshot.forEach(function(doc) {
        // データが更新されるたびに呼び出される
        commit("init", {
          id: doc.id,
          screen_name: doc.data().account,
          generated_text: doc.data().generated_text,
          created_at: new Date(doc.data().created_at),
        });
        // })
      });
    },
    // リスナーの停止
    stopListener() {
      if (this.unsubscribe) {
        this.unsubscribe();
        this.unsubscribe = null;
      }
    },
    updateMillion({ state }) {
      const million = !state.data.million;
      LinkRef.doc(state.data.id)
        .update({ million: million })
        .then(() => {})
        .catch((err) => {
          console.err("Error updateing document: ", err);
        });
    },
    updatePlatforms({ state }, payload) {
      const platforms = [].concat(state.data.platforms);
      if (platforms.includes(payload.platforms)) {
        platforms.splice(platforms.indexOf(payload.platforms), 1);
      } else {
        platforms.push(payload.platform);
      }
      LinkRef.doc(state.data.id)
        .update({ platforms: platforms })
        .then(() => {})
        .catch((err) => {
          console.error("Error updating document: ", err);
        });
    },
  },
};
