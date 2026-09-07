<template>
  <div class="container summary-container">
    <h3 class="p-2">{{ topic.title }}</h3>

    <div v-if="topic.summary" class="topic-summary my-2 p-2" v-html="renderedSummary"></div>

    <p v-else>Loading summary...</p>

    <div class="chat-messages my-3">
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="chat-message mb-3"
      >
        <div class="query p-2">
          <strong>You</strong>
          <div>{{ message.query }}</div>
        </div>
        <div class="response p-2" v-html="message.renderedResponse"></div>
      </div>
    </div>

    <form class="input-group mt-auto" @submit.prevent="sendQuery">
      <input
        type="text"
        class="form-control"
        placeholder="Ask your query"
        v-model="userQuery"
        :disabled="isLoading"
      />
      <button type="submit" class="btn btn-primary" :disabled="isLoading || !userQuery.trim()">
        Submit
      </button>
    </form>

    <p v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</p>

    <div class="summary-actions mt-2 mb-3">
      <button type="button" class="btn btn-danger">
        Continue
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { marked } from "marked";
import { baseUrl } from "../../../config";

const route = useRoute();
const topic = ref({});
const userQuery = ref("");
const messages = ref([]);
const threadId = ref(null);
const isLoading = ref(false);
const errorMessage = ref("");

const renderedSummary = computed(() =>
  marked.parse(topic.value.summary || "")
);

async function sendQuery() {
  const query = userQuery.value.trim();

  if (!query || isLoading.value) {
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";

  const requestBody = { query };
  if (threadId.value !== null) {
    requestBody.thread_id = threadId.value;
  }

  try {
    const response = await fetch(
      `${baseUrl}/subtopics/${route.params.id}/chat/`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      }
    );

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const data = await response.json();
    const responseText = data.response ?? data.answer ?? data.message ?? data;

    if (data.thread_id !== undefined) {
      threadId.value = data.thread_id;
    }

    messages.value.push({
      query,
      renderedResponse: marked.parse(String(responseText)),
    });
    userQuery.value = "";
  } catch (error) {
    errorMessage.value = "Unable to get a response. Please try again.";
    console.error("Failed to send subtopic query:", error);
  } finally {
    isLoading.value = false;
  }
}

onMounted(async () => {
  try {
    const response = await fetch(
      `${baseUrl}/subtopics/${route.params.id}`
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
.summary-actions {
    text-align: center;
}
</style>