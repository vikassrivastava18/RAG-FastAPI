<template>
<div class="mt-2">

  <div v-if="correct" class="alert alert-success">
    Correct ✅
  </div>

  <div v-else class="alert alert-danger">
    Incorrect ❌ <br>
    <strong>Correct Answer:</strong> {{ answer }}
  </div>

  <div v-if="explanation" class="mt-2">
    {{ explanation }}
  </div>

  <div v-if="url">
    <a :href="url" target="_blank">Learn more</a>
  </div>

</div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  correct: Boolean,
  answer: [String, Boolean],
  explanation: String,
  url: String
})
</script>