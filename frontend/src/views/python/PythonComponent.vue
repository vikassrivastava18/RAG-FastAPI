<script setup>
import { ref } from "vue";
import { runPython } from "../../services/pythonRunner";

const code = ref(`print("Hello World")`);

const output = ref("");
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
</script>

<template>
  <div>
    <textarea v-model="code" rows="10" cols="60"></textarea>
    <br />

    <button @click="executeCode" :disabled="loading">
      {{ loading ? "Running..." : "Run Python" }}
    </button>

    <h3>Output</h3>

    <pre>{{ output }}</pre>
  </div>
</template>