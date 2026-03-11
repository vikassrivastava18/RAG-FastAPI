<template>
    <div class="tab-pane fade show active p-4" id="section1">
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
                    <option v-for="chapter of bookChapters" :key="chapter.id" :value="chapter.id">{{
                        chapter.chapter_name }}
                    </option>
                </select>
            </div>

        </div>

        <div v-if="aiLoading" class="d-flex justify-content-center mt-4">
            <div class="spinner-grow text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        <div v-else>
            <div v-html="content" class="mt-2 mb-5 p-4"></div>
        </div>

        <div v-if="!aiLoading && selectedChapter !== 0" class="container">
            <div v-if="qizzLoaded">
                <QuizComponent :quizzes="qizzes" />
            </div>
            <div v-else>
                <button type="button" class="btn btn-primary mt-3" 
                    id="getQuizBtn" @click="getQuizzes()">Test
                    my knowledge
                </button>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, getCurrentInstance, watch } from 'vue'
import QuizComponent from './QuizComponent.vue';
import { baseUrl } from '../config'

const instance = getCurrentInstance()
const proxy = instance && instance.proxy

const booksUrl = baseUrl + "/books";
const bookChaptersUrl = baseUrl + "/chapter-subtopics/";
const quizUrl = baseUrl + "/generate-quizzes";
const chapterSummaryUrl = baseUrl + "/chapter-summary"

const books = ref([])
const selectedBook = ref(0); // A reactive reference for the select value
const bookChapters = ref([]);
const selectedChapter = ref(0)
const aiLoading = ref(false)
const content = ref("")
const qizzLoaded = ref(false)
const qizzes = ref({})

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
    qizzLoaded.value = false
    console.log("selectedChapter: ", newValue);
    if (newValue !== 0) { // use strict numeric check
        aiLoading.value = true
        fetchChapterContent(newValue)    
    }    
});

async function fetchChapterContent(chapterId) {
    // content.value = chapterContent
    const res = await proxy.$axios.post(chapterSummaryUrl, {"chapter_id": chapterId})
    console.log("Response: ", res.data);
    content.value = res.data.content
    console.log("Response: ", res.data);
    
    aiLoading.value = false
}

async function getQuizzes() {
    document.getElementById('getQuizBtn').setAttribute('disabled', true)

    const url = quizUrl;
    try{
        const id = Number(selectedChapter.value)
        const res = await proxy.$axios.post(url, { "chapter_id": id })
        qizzes.value = res.data.quizzes
        console.log("Quiz response: ", res.data);
    } finally {
        qizzLoaded.value = true
        document.getElementById('getQuizBtn').setAttribute('disabled', false)
    }    
    
}

async function getBooks() {
    const url = booksUrl;
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

</script>

<style>
/* label {
    color: cornflowerblue
} */
select {
    min-width: 250px;
}

#getQuizBtn {
    position: fixed;
    bottom: 10px;
}
</style>