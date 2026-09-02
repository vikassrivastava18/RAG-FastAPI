<template>
    <div class="d-flex justify-content-start">
                <div class="col-xs-3">
                    <label for="bookSelect" class="form-label">Select a book</label>
                    <select name="bookSelect" id="bookSelect" 
                        v-model="selectedBook" class="form-select">
                        <option :key="0" :value="0">Open the select menu</option>
                        <option v-for="book of books" :key="book.id" 
                        :value="book.id" class="form-control">{{ book.name }}
                        </option>
                    </select>
                </div>
                <div class="col-xs-3 ms-4">
                    <label for="chapterSelect" class="form-label">Select a Chapter</label>
                    <select name="chapterSelect" id="chapterSelect" 
                        v-model="selectedChapter" class="form-select">
                        <option :key="0" :value="0" selected>Open the select menu</option>
                        <option v-for="chapter of bookChapters" :key="chapter.id" :value="chapter.id">
                            {{ chapter.chapter_name }}
                        </option>
                    </select>
                </div>
            </div>
</template>

<script setup>
import { ref, onMounted, getCurrentInstance, watch, defineEmits } from 'vue'
import { baseUrl } from '../../config'

const instance = getCurrentInstance()
const proxy = instance && instance.proxy
const bookChaptersUrl = baseUrl + "/chapter-subtopics/";

const books = ref([]);
const selectedBook = ref(0);
const selectedChapter = ref(0);
const bookChapters = ref([]);
const aiLoading = ref(false);
const emit = defineEmits(['save'])

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
        emit('startDialogue', newValue)
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
    } catch (error) {
        console.error('Error:', error.message)
    }
}
</script>