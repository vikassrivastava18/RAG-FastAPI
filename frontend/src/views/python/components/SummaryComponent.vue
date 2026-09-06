<template>
  <div class="container summary-container">
    <h3 class="p-2">{{ topic.title }}</h3>

    <div
      v-if="topic.summary"
      class="topic-summary my-2 p-2"
      v-html="renderedSummary"
    ></div>

    <p v-else>Loading summary...</p>

    <div class="input-group mt-auto mb-3">
      <input
        type="text"
        class="form-control"
        placeholder="Ask a question..."
        aria-label="Ask a question"
      />
      <button class="btn btn-outline-success" type="button">
        Send
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { marked } from "marked";

const route = useRoute();
const topic = ref({});

const renderedSummary = computed(() =>
  marked.parse(topic.value.summary || "")
);

onMounted(async () => {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/topics/${route.params.id}`
    );

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    topic.value = await response.json();
  } catch (error) {
    console.error("Failed to load topic summary:", error);
  }
});
</script>

<style scoped>
.topic-summary {
  line-height: 1.7;
}
h3 {
  color: maroon;
}
.summary-container {
  /* min-height: 75vh; */
  display: flex;
  flex-direction: column;
}
</style>