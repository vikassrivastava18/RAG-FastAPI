import './assets/base.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import axios from 'axios'
import { createWebHistory, createRouter } from 'vue-router'
import { createApp } from 'vue'
import HomeView from './views/HomeView.vue'
import App from './App.vue'


const routes = [
  { path: '/', component: HomeView },
  { path: '/ask', component: () => import('./views/AskView.vue')},
  { path: '/quiz', component: () => import('./views/QuizView.vue')},
  { path: '/answer', component: () => import('./views/AnswerView.vue')},
  { path: '/dialogue', component: () => import('./views/DialogueView.vue')},
  { path: '/select', component: () => import('./components/SelectComponent.vue')}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


let app = createApp(App)
            .use(router)

app.config.globalProperties.$axios = axios
app.mount('#app')