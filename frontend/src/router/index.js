import Vue from "vue";
import VueRouter from "vue-router";
// import Home from "../views/Home.vue";
// ページコンポーネントのインポート
import NotFound from '../components/pages/NotFound'
import Index from '../components/pages/Index'
import TermsOfService from '../components/pages/TermsOfService'
import PrivacyPolicy from '../components/pages/PrivacyPolicy'

Vue.use(VueRouter);

const routes = [{
        path: "/",
        name: "Index",
        component: Index,
    },
    {
        path: '/404',
        component: NotFound
    },
    {
        name: 'TermsOfService',
        path: '/service',
        component: TermsOfService
    },
    {
        name: 'PrivacyPolicy',
        path: '/privacy-policy',
        component: PrivacyPolicy
    },
    {
        path: '*',
        redirect: '/404'
    }
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});

export default router;