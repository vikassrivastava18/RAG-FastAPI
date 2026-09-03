import './assets/base.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import axios from 'axios'
import { createWebHistory, createRouter } from 'vue-router'
import { createApp } from 'vue'

import HomeView from './views/HomeView.vue'
import App from './App.vue'
import PythonView from './views/python/PythonView.vue'
import PythonTopicsView from './views/python/PythonTopicsView.vue'


const routes = [
  { path: '/', component: HomeView },
  { path: '/python-topics', component: PythonTopicsView},
  { path: '/python', component: PythonView}
  
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

let app = createApp(App)
            .use(router)

app.config.globalProperties.$axios = axios
app.mount('#app')