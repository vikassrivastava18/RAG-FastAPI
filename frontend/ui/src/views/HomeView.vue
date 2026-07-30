<template>

<section class="py-5 bg-light">
  <div class="container">
    <div class="row g-5">

      <!-- Image Column -->
      <div class="col-lg-6">
        <img
          src="https://cdn.prod.website-files.com/679c2851aa61fe501c78835f/684209eccec40c45cade6906_CVTC%202.avif"
          alt="About WisTech Open"
          class="rounded-4 shadow-lg w-100 object-fit-cover mt-4"
        />
      </div>

      <!-- Content Column -->
      <div class="col-lg-6">

        <!-- Main Heading -->
        <h4 class="display-6 fw-bold text-dark mt-2 mb-4">
          About WisTechfusion (V2)
        </h4>

        <!-- Paragraph -->
        <p class="text-secondary fs-5 lh-lg mb-4">
          WisTechfusion is an AI application created to help students in their study. 
          The digital books made available through WistechOpen have been integrated and students can 
          clear their doubts, have dialogues with an AI agent and learn from quizzes through this platform.
        </p>

      </div>
    </div>
  </div>
</section>


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

<style scoped>
  .letter-spacing {
    letter-spacing: 1px;
  }

  .object-fit-cover {
    object-fit: cover;
    max-height: 650px;
  }

  section {
    background-image: linear-gradient(#f8f8f8, #f8f8f8de), url('@/assets/Blue_Flames.jpg');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: top;
  }

</style>