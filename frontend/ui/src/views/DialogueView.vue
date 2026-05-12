<template>
    <div>
        <div class="container px-4">
            <i>
                <label for="askInput" class="control-label py-2 mb-2">
                    Let's learn something new today!
                </label>
            </i>
            <div class="d-flex justify-content-start">
                <div class="col-xs-3">
                    <label for="bookSelect" class="control-label">
                        Select a book</label>
                    <select name="bookSelect" id="bookSelect" 
                        v-model="selectedBook" class="form-select">
                        <option :key="0" :value="0">----</option>
                        <option v-for="book of books" :key="book.id" 
                            :value="book.id" class="form-control">{{ book.name }}
                        </option>
                    </select>
                </div>
                <div class="col-xs-3 ms-4">
                    <label for="chapterSelect" class="control-label">
                        Select a Chapter</label>
                    <select name="chapterSelect" id="chapterSelect" 
                        v-model="selectedChapter" class="form-select">
                        <option :key="0" :value="0">----</option>
                        <option v-for="chapter of bookChapters" :key="chapter.id" 
                            :value="chapter.id">
                            {{ chapter.chapter_name }}
                        </option>
                    </select>
                </div>
            </div>
        </div>

        <div class="container">
            <div v-if="quizMode">
                <QuizComponent :quizzes="quizzes" @next-summary="nextTopic" />
                
            </div>
            <p v-else v-html="message" class="p-4"></p>

            <input class="form-control py-2 my-2" id="askInput" 
                v-model="userInput" placeholder="Enter your answer here..."
                @keyup.enter="sendResponse" :hidden="inputDisabled"
                v-if="!quizMode">
            <div v-if="aiLoading" class="d-flex justify-content-center mt-4">
                <div class="spinner-grow text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, getCurrentInstance, watch } from 'vue'
import { baseUrl } from '../config'
import QuizComponent from '../components/QuizComponent.vue'

const instance = getCurrentInstance()
const proxy = instance && instance.proxy
const bookChaptersUrl = baseUrl + "/chapter-subtopics/";
const startDialogueUrl = baseUrl + "/dialogue/start-dialogue";
const answerReviewUrl = baseUrl + "/dialogue/review-response";
const nextTopicUrl = baseUrl + "/dialogue/next-topic";

const books = ref([]);
const selectedBook = ref(0);
const selectedChapter = ref(0);
const bookChapters = ref([]);
const aiLoading = ref(false);
const dialogue = ref({});
const message = ref("");
const userInput = ref("");
const inputDisabled = ref(true)
const quizMode = ref(false)
const quizzes = ref({})

onMounted(() => {
    getBooks()
})

// Watch the selectedBook ref
watch(selectedBook, (newValue) => {
    const id = Number(newValue)
    if (id > 0) {
        getChapters(id)
    }
});

// Watch the selectedChapter ref
watch(selectedChapter, (newValue) => {
    console.log("selectedChapter: ", newValue);
    if (newValue !== 0) { // use strict numeric check
        aiLoading.value = true
        fetchDialogue(newValue)
    }
});


async function getBooks() {
    const url = baseUrl + '/books';
    try {
        const res = await proxy.$axios.get(url)
        books.value = res.data

    } catch (error) {
        console.error('Error:', error.message)
    }
}


async function getChapters(bookId) {
    const url = bookChaptersUrl;
    try {
        const id = Number(bookId)
        if (!id) return // don't call backend for invalid id
        const bookInfo = { "book_id": id }
        const res = await proxy.$axios.post(url, bookInfo)
        bookChapters.value = res.data.chapters
        // selectedChapter.value = res.data.chapters[0].id
    } catch (error) {
        console.error('Error:', error.message)
    }
}

async function fetchDialogue(chapterId) {
    const res = await proxy.$axios.post(startDialogueUrl,{"chapter_id": chapterId })
    console.log("data: ", res.data);
    
    dialogue.value = res.data

    message.value = `🚀<b>Welcome</b>, we will be learning importance concepts related to the 
                    chapter.<br> <p>${dialogue.value.dialogue}</p>`

    aiLoading.value = false;
    inputDisabled.value = false;
}

async function sendResponse() {
   
    message.value += "<br> <p>" + userInput.value + "</p>"
    const payload = { "answer": userInput.value, "session_id": dialogue.value.session_id }
    console.log("Sending evaluate payload:", payload);

    inputDisabled.value = true
    aiLoading.value = true

    try {
        const res = await proxy.$axios.post(answerReviewUrl, payload)
        console.log('Review response:', res.data)
        const result = res.data.response
        console.log("Result: ". result);
        if (res.data.state === "clear") {
            quizMode.value = true
            quizzes.value = result
        } else message.value = result


    } catch (error) {
        console.error('evaluate-response error:', error)
        if (error.response) {
            console.error('Status:', error.response.status, 'Data:', error.response.data)
            // show a concise message to the user (server validation details)
            message.value = `<span class="text-danger">Server: ${error.response.status} 
                            - ${JSON.stringify(error.response.data)}</span>`
        } else {
            message.value = `<span class="text-danger">Request failed</span>`
        }
    } finally {
        aiLoading.value = false
        inputDisabled.value = false
    }
}

async function nextTopic() {
    inputDisabled.value = true
    aiLoading.value = true
    const payload = {"session_id": dialogue.value.session_id}
    try {
        const res = await proxy.$axios.post(nextTopicUrl, payload)
        
        const result = res.data.response
        console.log("Result: ". result);
        quizMode.value = false
        message.value = result
        

    } catch (error) {
        console.error('evaluate-response error:', error)
        if (error.response) {
            console.error('Status:', error.response.status, 'Data:', error.response.data)
            // show a concise message to the user (server validation details)
            message.value = `<span class="text-danger">Server: ${error.response.status} 
                            - ${JSON.stringify(error.response.data)}</span>`
        } else {
            message.value = `<span class="text-danger">Request failed</span>`
        }
    } finally {
        aiLoading.value = false
        inputDisabled.value = false
    }
}

</script>

<style scoped>
    #askInput {
        position: fixed;
        bottom: 10px;
        border: 1px solid rgb(20, 103, 220);
        max-width: 75vw;
    }
    #chapterSelect {
        min-width: 20vw;
    }
</style>