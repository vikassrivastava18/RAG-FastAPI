<template>

    <div class="container">
        <i>
            <label for="askInput" class="control-label p-2">
                Ask me anything from Wistech Open books!
            </label>
        </i>
        <input class="form-control py-2 my-2" id="askInput" v-model="userInput" placeholder="Enter your query here..."
            @keyup.enter="answerUserQuery">
        <div v-if="aiLoading" class="d-flex justify-content-center mt-4">
            <div class="spinner-grow text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        <div v-else v-html="queryAnswer" class="mt-2 mb-5 p-4">
        </div>
    </div>

</template>

<script setup>
import { ref, getCurrentInstance } from 'vue'
import { baseUrl } from '../config'

const queryAnswer = ref("");

const instance = getCurrentInstance()
const proxy = instance && instance.proxy
const userInput = ref("")
const queryUrl = baseUrl + "/llm/answer-query"
const aiLoading = ref(false)

async function answerUserQuery() {
    aiLoading.value = true
    const res = await proxy.$axios.post(queryUrl, { "query": userInput.value })
    userInput.value = "";
    aiLoading.value = false
    queryAnswer.value = res.data
}

</script>

<style>
#askInput {
    /* position: fixed;
        bottom: 10px; */
    border: 1px solid rgb(20, 103, 220);
    max-width: 75vw;
}
</style>