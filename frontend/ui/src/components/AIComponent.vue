<template>
    <div class="container">         
        <button type="button" class="btn btn-primary btn-block"
            @click="getQuizzes(2)">Test my knowledge</button>
        <QuizComponent :quizzes="qizzes" />
        </div>    
    
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue'
import { baseUrl } from '@/config';
import QuizComponent from './QuizComponent.vue';

const instance = getCurrentInstance()
const proxy = instance && instance.proxy
const quizUrl = baseUrl + "/generate-quizzes";

const qizzes = ref({})

async function getQuizzes(params) {
    const url = quizUrl;
    const id = Number(params) 
    const res = await proxy.$axios.post(url, {"chapter_id":id})
    // const res = await proxy.$axios.post(url, id)
    console.log("Quiz response: ", res.data);
    qizzes.value = res.data.quizzes.quizzes
    
}
</script>

<style scoped>
 
    button {
        position:fixed;
        bottom: 10px;
        width: 80vw;
    }

</style>