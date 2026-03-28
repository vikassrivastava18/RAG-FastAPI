<template>
    <div class="container">
        <h2 class="mb-4">Dialogue</h2>
        <div class="d-flex justify-content-start">
            <div class="col-xs-3">
                <label for="bookSelect" class="control-label">Select a book</label>
                <select name="bookSelect" id="bookSelect" v-model="selectedBook" class="form-select">
                    <option :key="0" :value="0">------</option>
                    <option v-for="book of books" :key="book.id" :value="book.id" class="form-control">{{ book.name }}
                    </option>
                </select>
            </div>
            <div class="col-xs-3 ms-4">
                <label for="chapterSelect" class="control-label">Select a Chapter</label>
                <select name="chapterSelect" id="chapterSelect" v-model="selectedChapter" class="form-select">
                    <option :key="0" :value="0">------</option>
                    <option v-for="chapter of bookChapters" :key="chapter.id" :value="chapter.id">
                        {{ chapter.chapter_name }}
                    </option>
                </select>
            </div>
        </div>
    </div>

    <div class="container">
        <p v-html="message" class="p-4"></p>

        <input class="form-control py-2 my-2" id="askInput" v-model="userInput" placeholder="Enter your answer here..."
            @keyup.enter="reviewAnswer" :hidden="inputDisabled">
        <div v-if="aiLoading" class="d-flex justify-content-center mt-4">
            <div class="spinner-grow text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    </div>

</template>

<script setup>
import { ref, onMounted, getCurrentInstance, watch } from 'vue'
import { baseUrl } from '../config'

const instance = getCurrentInstance()
const proxy = instance && instance.proxy
const bookChaptersUrl = baseUrl + "/chapter-subtopics/";
const startDialogueUrl = baseUrl + "/llm/generate-question";
const answerReviewUrl = baseUrl + "/llm/evaluate-response";

const books = ref([]);
const selectedBook = ref(0);
const selectedChapter = ref(0);
const bookChapters = ref([]);
const aiLoading = ref(false);
const dialogue = ref({});
const message = ref("");
const userInput = ref("");
const inputDisabled = ref(true)

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
        console.log("Chapters: ", res.data)
        bookChapters.value = res.data.chapters
        // selectedChapter.value = res.data.chapters[0].id
    } catch (error) {
        console.error('Error:', error.message)
    }
}

async function fetchDialogue(chapterId) {
    const res = await proxy.$axios.post(startDialogueUrl,
        { "chapter_id": chapterId })
    dialogue.value = res.data.dialogue

    message.value = `🚀<b>Welcome</b>, we will be learning some importance concepts related to the chapter, 
                starting with the  topic <b>${dialogue.value["questions"][0]["topic"]} </b>` + `<br> <br>` +
        `${dialogue.value["questions"][0]["question"]}`

    aiLoading.value = false;
    inputDisabled.value = false;
}

async function reviewAnswer() {
    // prepare a plain JSON payload (strip Vue reactivity)
    dialogue.value["user_answer"] = userInput.value;
    message.value += "<br> <p>" + userInput.value + "</p>"
    const payload = { "answer": userInput.value, "session_id": dialogue.value.session_id }
    // const payload = JSON.parse(JSON.stringify(dialogue.value || {}));
    // payload.user_answer = userInput.value;
    console.log("Sending evaluate-response payload:", payload);

    inputDisabled.value = true
    aiLoading.value = true

    try {
        const res = await proxy.$axios.post(answerReviewUrl, payload)
        console.log('Review response:', res.data)
        const evaluation = res.data.dialogue
         message.value += "<br> <p>" + evaluation["llm_response"] + "</p>"

        if (evaluation["state"] === "incorrect" || evaluation["state"] === "correct") {           
            message.value += "<br> <p>" + evaluation["question"] + "</p>"
        } else if (evaluation["state"] === "END") {           
            message.value += "<br> <p>" + "Congratulation, you have completed the chapter" + "</p>"
        }

        userInput.value = "";
        inputDisabled.value = false

    } catch (error) {
        console.error('evaluate-response error:', error)
        if (error.response) {
            console.error('Status:', error.response.status, 'Data:', error.response.data)
            // show a concise message to the user (server validation details)
            message.value = `<span class="text-danger">Server: ${error.response.status} - ${JSON.stringify(error.response.data)}</span>`
        } else {
            message.value = `<span class="text-danger">Request failed</span>`
        }
    } finally {
        aiLoading.value = false
        inputDisabled.value = false
    }
}

</script>

<style>
#askInput {
    position: fixed;
    bottom: 10px;
    border: 1px solid rgb(20, 103, 220);
    max-width: 75vw;
}
</style>