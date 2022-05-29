import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// import VueGoogleMaps from '@fawmi/vue-google-maps'

const app = createApp(App)

// app.use(VueGoogleMaps, {
//     load: {
//         key: 'AIzaSyDRP8nSFiRqi-kKZMOBKYoghzawthJgUhs',
//     },
// })

app.use(router)

app.mount('#app')