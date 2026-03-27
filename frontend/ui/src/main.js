import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import axios from 'axios'
import { createWebHistory, createRouter } from 'vue-router'
import { createApp } from 'vue'
import App from './App.vue'
import LearnView from './views/LearnView.vue'

const routes = [
  { path: '/', component: LearnView },
  { path: '/ask', component: () => import('./views/AskView.vue')},
  { path: '/quiz', component: () => import('./views/QuizView.vue')},
  { path: '/dialogue', component: () => import('./views/DialogueView.vue')}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


let app = createApp(App)
            .use(router)

app.config.globalProperties.$axios = axios
app.mount('#app')