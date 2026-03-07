import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import axios from 'axios'
import { createApp } from 'vue'
import App from './App.vue'

let app = createApp(App)

app.config.globalProperties.$axios = axios
app.mount('#app')