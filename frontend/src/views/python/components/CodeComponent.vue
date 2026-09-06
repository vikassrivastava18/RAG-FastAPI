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
            <p>
              Write a Python program that prints
              <strong>Hello World</strong>.
            </p>
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
            ></textarea>

            <button
              class="btn btn-primary mt-3"
              @click="executeCode"
              :disabled="loading"
            >
              {{ loading ? "Running..." : "Run Python" }}
            </button>

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

            <div
              v-if="output"
              class="alert mt-3"
              :class="answerMatches ? 'alert-success' : 'alert-danger'"
            >
              {{ answerMatches ? "Correct answer" : "Answers do not match" }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { runPython } from "../../../services/pythonRunner";

const code = ref(`print("Hello World")`);
const output = ref("");
const expectedAnswer = ref("Hello World");
const loading = ref(false);

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
</script>

