<template>
    <div class="tab-pane fade show active p-2" id="section1">
        <h2 class="mb-4">Summary</h2>
        <div class="d-flex justify-content-start">
            <div class="col-xs-3">
                <label for="bookSelect" class="control-label">Select a book</label>
                <select name="bookSelect" id="bookSelect" 
                    v-model="selectedBook" class="form-select">
                    <option :key="0" :value="0">------</option>
                    <option v-for="book of books" :key="book.id" 
                        :value="book.id" class="form-control">{{ book.name }}
                    </option>
                </select>
            </div>
            <div class="col-xs-3 ms-4">
                <label for="chapterSelect" class="control-label">Select a Chapter</label>
                <select name="chapterSelect" id="chapterSelect" 
                    v-model="selectedChapter" class="form-select">
                    <option :key="0" :value="0">------</option>
                    <option v-for="chapter of bookChapters" :key="chapter.id" 
                        :value="chapter.id">
                        {{chapter.chapter_name }}
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

    </div>
</template>

<script setup>
import { ref, onMounted, getCurrentInstance, watch } from 'vue'
import { baseUrl } from '../config'

const instance = getCurrentInstance()
const proxy = instance && instance.proxy

// const booksUrl = baseUrl + "/llm";
const bookChaptersUrl = baseUrl + "/chapter-subtopics/";

const chapterSummaryUrl = baseUrl + "/llm/chapter-summary"

const books = ref([])
const selectedBook = ref(0); // A reactive reference for the select value
const bookChapters = ref([]);
const selectedChapter = ref(0)
const aiLoading = ref(false)
const content = ref("")


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
        fetchChapterContent(newValue)    
    }    
});

async function fetchChapterContent(chapterId) {
    // content.value = chapterContent
    const res = await proxy.$axios.post(chapterSummaryUrl, 
                {"chapter_id": chapterId})
    content.value = res.data.content
    
    aiLoading.value = false
}

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

</script>

<style>
    select {
        min-width: 250px;
    }
    #getQuizBtn {
        position: fixed;
        bottom: 10px;
    }
</style>