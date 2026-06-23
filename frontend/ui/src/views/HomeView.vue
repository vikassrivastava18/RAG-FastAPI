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

        <!-- Small Heading -->
        <span class="text-uppercase fw-semibold text-primary small letter-spacing">
          Our Story
        </span>

        <!-- Main Heading -->
        <h2 class="display-5 fw-bold text-dark mt-2 mb-4">
          About WisTech Open
        </h2>

        <!-- Paragraph -->
        <p class="text-secondary fs-5 lh-lg mb-4">
          The story of WisTech Open begins with an idea: that high-quality
          learning should be free and accessible to everyone. In 2019,
          Chippewa Valley Technical College launched Open RN (Open Resources
          for Nursing) with support from a U.S. Department of Education Open
          Textbooks Pilot Grant.
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

</style>