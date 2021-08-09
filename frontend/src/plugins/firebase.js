// import Vue from 'vue'
// import { firestorePlugin } from 'vuefire'
import firebase from "firebase/app";
import "firebase/firestore";

// Vue.use(firestorePlugin)

// Your web app's Firebase configuration DEV
// const firebaseConfig = {
//     apiKey: "AIzaSyCG3rsVk5qRg8LfpQLUwyLl9PiruRT8imY",
//     authDomain: "aitter-twigene-dev.firebaseapp.com",
//     databaseURL: "https://aitter-twigene-dev.firebaseio.com",
//     projectId: "aitter-twigene-dev",
//     storageBucket: "aitter-twigene-dev.appspot.com",
//     messagingSenderId: "1076901828982",
//     appId: "1:1076901828982:web:abb6274d756df5e0614257",
//     measurementId: "G-5M4RH2DZZ2"
// };

// 本番用
const firebaseConfig = {
  apiKey: "AIzaSyASl-5HORauWkx_iTmZ2dn-SyI0L90jA-w",
  authDomain: "aitter-twigene.firebaseapp.com",
  databaseURL: "https://aitter-twigene.firebaseio.com",
  projectId: "aitter-twigene",
  storageBucket: "aitter-twigene.appspot.com",
  messagingSenderId: "416427124433",
  appId: "1:416427124433:web:f5a63ca70ff60099d247f0",
  measurementId: "G-XF3CWTJMTP",
};

// Initialize Firebase
const firebaseApp = firebase.initializeApp(firebaseConfig);
const firestore = firebaseApp.firestore();
export default firestore;
