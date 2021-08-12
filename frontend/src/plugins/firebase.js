// import Vue from 'vue'
// import { firestorePlugin } from 'vuefire'
import firebase from 'firebase/app';
import 'firebase/firestore';

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

// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: 'AIzaSyC9r5N0LwaebA5qfAUussk_JUWMoL8GbrA',
    authDomain: 'pic2force.firebaseapp.com',
    projectId: 'pic2force',
    storageBucket: 'pic2force.appspot.com',
    messagingSenderId: '838988345433',
    appId: '1:838988345433:web:e2e8ca2491616a37ec8148',
    measurementId: 'G-1FBT6SK2YL',
};

// Initialize Firebase
const firebaseApp = firebase.initializeApp(firebaseConfig);
const firestore = firebaseApp.firestore();
export default firestore;