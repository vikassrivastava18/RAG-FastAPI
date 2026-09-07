<template>
  <div class="container">
    <div class="row g-4 coding-layout">
      <!-- Left column: question -->
      <div class="col-md-5">
        <div class="card h-100">
          <div class="card-header">
            Question
          </div>
          <div class="card-body">
            <p>{{ question || "Loading question..." }}</p>
          </div>
        </div>
      </div>

      <!-- Right column -->
      <div class="col-md-7 coding-column">
        <!-- Code row -->
        <div class="card mb-4">
          <div class="card-header">
            Your Code
          </div>
          <div class="card-body">
            <textarea
              v-model="code"
              class="form-control"
              rows="10"
              @paste.prevent
              spellcheck="false"
              @keydown.tab.prevent="insertIndentation"
            ></textarea>

            <div class="d-flex align-items-center mt-3 gap-3">
              <button
                class="btn btn-primary"
                @click="executeCode"
                :disabled="loading"
              >
                {{ loading ? "Running..." : "Run Python" }}
              </button>

              <div
                v-if="output"
                class="alert mb-0 p-2 "
                :class="answerMatches ? 'alert-success' : 'alert-danger'"
              >
                {{ answerMatches ? "Correct answer" : "Answers do not match" }}
              </div>
            </div>

            <h5 class="mt-4">Your Output</h5>
            <pre class="bg-light p-3">{{ output }}</pre>
          </div>
        </div>

        <!-- Expected answer row -->
        <div class="card">
          <div class="card-header">
            Match Answer
          </div>
          <div class="card-body">
            <label for="expectedAnswer" class="form-label">
              Expected answer
            </label>

            <textarea
              id="expectedAnswer"
              v-model="expectedAnswer"
              class="form-control"
              rows="4"              
            ></textarea>
            
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { runPython } from "../../../services/pythonRunner";
import { baseUrl } from "../../../config";

const question = ref("");
const code = ref("");
const output = ref("");
const expectedAnswer = ref("");
const loading = ref(false);

onMounted(async () => {
  try {
    const response = await fetch(`${baseUrl}/code-snippets/1`);

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const snippet = await response.json();

    question.value = snippet.question;
    code.value = snippet.snippet;
    expectedAnswer.value = String(snippet.expected_answer);
  } catch (error) {
    console.error("Failed to load code snippet:", error);
  }
});

async function executeCode() {
  loading.value = true;
  output.value = "";

  try {
    const result = await runPython(code.value);
    output.value = String(result ?? "");
  } catch (error) {
    output.value = String(error);
  } finally {
    loading.value = false;
  }
}

const answerMatches = computed(() =>
  output.value.trim() === expectedAnswer.value.trim()
);

function insertIndentation(event) {
  const textarea = event.target;
  const indentation = "    ";
  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;

  code.value =
    code.value.substring(0, start) +
    indentation +
    code.value.substring(end);

  requestAnimationFrame(() => {
    textarea.selectionStart = textarea.selectionEnd =
      start + indentation.length;
  });
}
</script>

