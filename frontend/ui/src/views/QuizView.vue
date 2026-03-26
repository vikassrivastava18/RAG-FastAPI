<template>
    <div class="container mt-4">

        <h2 class="mb-4">Quiz</h2>
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
        <div v-if="quizzLoading" class="d-flex justify-content-center mt-4">
            <div class="spinner-grow text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        <div class="container p-4" v-else>
            <!-- MCQ -->
            <div v-if="quizzes.mcq?.length">
                <h4>Multiple Choice</h4>

                <div v-for="(q, index) in quizzes.mcq" :key="'mcq' + index" class="card mb-3 p-3">

                    <p><strong>{{ index + 1 }}. {{ q.question }}</strong></p>

                    <div v-for="opt in q.options" :key="opt" class="form-check">
                        <input class="form-check-input" type="radio" :name="'mcq' + index" :value="opt"
                            v-model="answers.mcq[index]">
                        <label class="form-check-label">
                            {{ opt }}
                        </label>
                    </div>

                    <ResultBlock v-if="submitted" :correct="q.answer === answers.mcq[index]" :answer="q.answer"
                        :explanation="q.explanation" :url="q.url" />

                </div>
            </div>

            <!-- TRUE FALSE -->
            <div v-if="quizzes.true_false?.length">
                <h4 class="mt-4">True / False</h4>

                <div v-for="(q, index) in quizzes.true_false" :key="'tf' + index" class="card mb-3 p-3">

                    <p><strong>{{ index + 1 }}. {{ q.question }}</strong></p>

                    <div class="form-check">
                        <input class="form-check-input" type="radio" :name="'tf' + index" :value="true"
                            v-model="answers.true_false[index]">
                        <label class="form-check-label">True</label>
                    </div>

                    <div class="form-check">
                        <input class="form-check-input" type="radio" :name="'tf' + index" :value="false"
                            v-model="answers.true_false[index]">
                        <label class="form-check-label">False</label>
                    </div>

                    <ResultBlock v-if="submitted" :correct="q.answer === answers.true_false[index]" :answer="q.answer"
                        :explanation="q.explanation" :url="q.url" />

                </div>
            </div>

            <!-- FILL BLANK -->
            <div v-if="quizzes.fill_blank?.length">
                <h4 class="mt-4">Fill in the Blank</h4>

                <div v-for="(q, index) in quizzes.fill_blank" :key="'fb' + index" class="card mb-3 p-3">

                    <p><strong>{{ index + 1 }}. {{ q.question }}</strong></p>

                    <input type="text" class="form-control" v-model="answers.fill_blank[index]"
                        placeholder="Enter answer">

                    <ResultBlock v-if="submitted"
                        :correct="normalize(q.answer) === normalize(answers.fill_blank[index])" :answer="q.answer"
                        :url="q.url" />

                </div>
            </div>

            <button v-if="quizzes.mcq?.length || quizzes.true_false?.length || quizzes.fill_blank?.length" 
            class="btn btn-primary mt-3" @click="submitQuiz">
                Submit Answers
            </button>
        </div>


    </div>
</template>

<script setup>
import { reactive, onMounted, ref, watch, getCurrentInstance } from "vue"
import ResultBlock from "../components/ResultBlock.vue"
import { baseUrl } from "@/config";
const quizUrl = baseUrl + "/llm/generate-quizzes";

const instance = getCurrentInstance()
const proxy = instance && instance.proxy

// const booksUrl = baseUrl + "/llm";
const books = ref([])
const bookChaptersUrl = baseUrl + "/chapter-subtopics/";
const selectedBook = ref(0); // A reactive reference for the select value
const bookChapters = ref([]);
const selectedChapter = ref(0)
const quizzes = ref({})
const quizzLoading = ref(false)

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
    quizzLoading.value = true
    console.log("selectedChapter: ", newValue);
    if (newValue !== 0) { // use strict numeric check
        getQuizzes(newValue)
    }
});


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


async function getBooks() {
    const url = baseUrl + '/books';
    try {
        const res = await proxy.$axios.get(url)
        books.value = res.data
    } catch (error) {
        console.error('Error:', error.message)
    }
}

async function getQuizzes() {

    const url = quizUrl;
    try {
        const id = Number(selectedChapter.value)
        const res = await proxy.$axios.post(url, { "chapter_id": id })
        quizzes.value = res.data.quizzes

    } finally {
        quizzLoading.value = false
    }

}

const submitted = ref(false)

const answers = reactive({
    mcq: [],
    true_false: [],
    fill_blank: []
})

function submitQuiz() {
    submitted.value = true
}

function normalize(val) {
    if (!val) return ""
    return val.toString().trim().toLowerCase()
}

</script>

<style></style>