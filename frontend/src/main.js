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
  {
    path: '/python',
    component: () => import('./views/python/PythonView.vue'),
    children: [
      {
        path: 'topic-summary/:id',
        component: () => import('./views/python/components/SummaryComponent.vue')
      },
      {
        path: 'topics',
        component: () => import('./views/python/components/TopicsComponent.vue')
      },
      {
        path: 'code',
        component: () => import('./views/python/components/CodeComponent.vue')
      }
    ]
    },
  
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

let app = createApp(App)
            .use(router)

app.config.globalProperties.$axios = axios
app.mount('#app')