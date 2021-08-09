// import Vue from 'vue'
// import Vuetify from 'vuetify'
import { createVuetify } from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.css';

// Vue.use(Vuetify)

const vuetify = createVuetify({
    theme: {
        options: {
            customProperties: true
        },
        themes: {
            light: {
                primary: '#ee44aa',
                secondary: '#424242',
                accent: '#82B1FF',
                error: '#FF5252',
                info: '#2196F3',
                success: '#4CAF50',
                warning: '#FFC107'
            }
        }
    },
    icons: {
        iconfont: 'mdi'
    }
})

export default vuetify;