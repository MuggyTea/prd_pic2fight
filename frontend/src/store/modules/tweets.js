import firestore from "../../plugins/firebase";
import { ADD, REMOVE } from "./mutation-types";
/**
 * リンクページ一覧のストアモジュール
 * リンク詳細ページで表示するリンクの配列を管理する
 */

// DBを呼び出す
const LinkRef = firestore.collection("UsersTweets");
// const TwitterUser = firestore.collection('Users')

export default {
  namespaced: true,
  unsubscribe: null,
  state() {
    return {
      // 配列
      data: [],
      alldata: [],
    };
  },
  mutations: {
    // 受け取ったデータpayloadをステートに格納
    init(state, payload) {
      state.data = payload;
      state.alldata = payload;
    },
    // リンク追加時
    [ADD](state, payload) {
      // DBから受け取ったデータをステートにセット
      // state.alldata.push(payload)
      state.data.push(payload);
    },
    alldata(state, payload) {
      // state.data.push(payload)
      // link_idを追加で更新する
      state.alldata.push(payload);
    },
    addData(state, payload) {
      state.data.unshift(payload);
      state.alldata.unshift(payload);
    },
    // 呼び出すとき
    set(state, payload) {
      const index = state.data.findIndex((link) => link.id === payload.id);
      if (index !== -1) {
        state.data[index] = payload;
        state.data.push(payload);
      }
    },
    // 削除時
    [REMOVE](state, payload) {
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
    alldata(state) {
      return state.alldata;
    },
  },
  actions: {
    clear({ commit }) {
      commit("init", []);
    },
    // リスナーの起動
    startListener({ commit }, userinfo) {
      if (this.unsubscribe || this.userinfo) {
        console.warn("listener is already running. ", this.unsubscribe);
        this.unsubscribe();
        this.unsubscribe = null;
      }
      // ユーザー情報がないものは表示しない
      if (!userinfo.screenName || !userinfo) {
        console.warn("user does not exist");
        userinfo.screenName = null;
      }
      // firestoreからデータを検索する
      this.unsubscribe = LinkRef.where("account", "==", userinfo.screenName)
        .orderBy("created_at", "desc")
        .limit(50)
        .onSnapshot(
          (querySnapshot) => {
            // データが更新されるたびに呼び出される
            querySnapshot.docChanges().forEach((change) => {
              // querySnapshot.forEach(change => {
              // ステート更新するために配列に格納（DBから直接読み込むと同期が追いつかない）
              const payload = {
                id: change.doc.id,
                tweet_id: change.doc.id.substr(0, 4),
                generated_text: change.doc.data().generated_text,
                screenName: change.doc.data().account,
                created_at: new Date(change.doc.data().created_at),
              };
              // 時刻がnullのものとログインユーザー以外は表示しない
              if (!change.doc.data().account || !change.doc.data().created_at) {
                console.warn("user does not exist");
                return;
              }
              // ミューテーションを通してステートを更新する
              if (change.type === "added" && change.doc.data()) {
                commit(ADD, payload);
              } else if (change.type === "modified" && change.doc.data()) {
                commit("addData", change.doc.data());
              } else if (change.type === "removed") {
                commit("REMOVE", payload);
              }
            });
          },
          (error) => {
            console.error(error.name);
          }
        );
    },
    startListenerAll({ commit }) {
      if (this.unsubscribe) {
        console.warn("listener is already running. ", this.unsubscribe);
        this.unsubscribe();
        this.unsubscribe = null;
      }
      // firestoreからデータを検索する
      this.unsubscribe = LinkRef.orderBy("created_at", "desc")
        .limit(50)
        .onSnapshot(
          (querySnapshot) => {
            // データが更新されるたびに呼び出される
            querySnapshot.docChanges().some((change) => {
              // 時刻がnullのものとログインユーザー以外は表示しない
              if (
                !change.doc.data().account ||
                !change.doc.data().created_at ||
                change.doc.data().checkbox == true
              ) {
                return;
              }
              // ステート更新するために配列に格納（DBから直接読み込むと同期が追いつかない）
              const payload = {
                id: change.doc.id,
                tweet_id: change.doc.id.substr(0, 4),
                generated_text: change.doc.data().generated_text,
                account: change.doc.data().account,
                created_at: new Date(change.doc.data().created_at),
              };
              // ミューテーションを通してステートを更新する
              if (change.type === "modified" && change.doc.data()) {
                commit("addData", payload);
              } else if (change.type === "added" && change.doc.data()) {
                commit("alldata", payload);
              } else if (change.type === "removed") {
                commit("REMOVE", payload);
              }
            });
          },
          (error) => {
            console.error(error.name);
          }
        );
    },
    // リスナーの停止
    stopListener() {
      if (this.unsubscribe) {
        this.unsubscribe();
        this.unsubscribe = null;
      }
    },
    addLink({ commit }, payload) {
      LinkRef.add(payload)
        .then((doc) => {
          // ミューテーションの外でステート管理しない
          // link_idをDBに追加
          LinkRef.doc(doc.id).update({
            id: doc.id,
            link_id: doc.id.substr(0, 4),
          });
        })
        .catch((err) => {
          console.error("Error adding document: ", err);
        });
    },
    deleteLink({ commit }, payload) {
      LinkRef.doc(payload.id)
        .delete()
        .then(() => {})
        .catch((err) => {
          console.error("Error removing document: ", err);
        });
    },
  },
};
