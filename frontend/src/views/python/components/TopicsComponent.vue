<template>
    <div class="container my-2 p-2">
            <div v-for="topic in topics" :key="topic.id">                
                <router-link class="topic-link" :to="`/python/topic-summary/${topic.id}`">
                    #{{ topic.title }}
                </router-link>
            </div>
        </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

const topics = ref([]);

onMounted(async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/topics/");

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        topics.value = await response.json();
    } catch (error) {
        console.error("Failed to load topics:", error);
    }
});
</script>

<style scoped>
.theory-container {
    padding: 24px;
    /* background: #f7f9fc;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06); */
}

h3 {
    margin: 0 0 16px;
    /* font-size: 1.5rem; */
    color: maroon;
    text-align: center;
}

.theory-iframe {
    width: 100%;
    min-height: 800px;
    border: 1px solid #dfe3e8;
    border-radius: 10px;
    background: #fff;
}

.topic-link {
    font-size: 1.25rem;
}
</style>