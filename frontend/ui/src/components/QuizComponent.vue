<template>
<div class="container mt-4">

  <h2 class="mb-4">Quiz</h2>

  <!-- MCQ -->
  <div v-if="quizzes.mcq?.length">
    <h4>Multiple Choice</h4>

    <div v-for="(q, index) in quizzes.mcq" :key="'mcq'+index" class="card mb-3 p-3">

      <p><strong>{{ index+1 }}. {{ q.question }}</strong></p>

      <div v-for="opt in q.options" :key="opt" class="form-check">
        <input
          class="form-check-input"
          type="radio"
          :name="'mcq'+index"
          :value="opt"
          v-model="answers.mcq[index]"
        >
        <label class="form-check-label">
          {{ opt }}
        </label>
      </div>

      <ResultBlock
        v-if="submitted"
        :correct="q.answer === answers.mcq[index]"
        :answer="q.answer"
        :explanation="q.explanation"
        :url="q.url"
      />

    </div>
  </div>


  <!-- TRUE FALSE -->
  <div v-if="quizzes.true_false?.length">
    <h4 class="mt-4">True / False</h4>

    <div v-for="(q, index) in quizzes.true_false" :key="'tf'+index" class="card mb-3 p-3">

      <p><strong>{{ index+1 }}. {{ q.question }}</strong></p>

      <div class="form-check">
        <input class="form-check-input" type="radio" :name="'tf'+index" :value="true" v-model="answers.true_false[index]">
        <label class="form-check-label">True</label>
      </div>

      <div class="form-check">
        <input class="form-check-input" type="radio" :name="'tf'+index" :value="false" v-model="answers.true_false[index]">
        <label class="form-check-label">False</label>
      </div>

      <ResultBlock
        v-if="submitted"
        :correct="q.answer === answers.true_false[index]"
        :answer="q.answer"
        :explanation="q.explanation"
        :url="q.url"
      />

    </div>
  </div>


  <!-- FILL BLANK -->
  <div v-if="quizzes.fill_blank?.length">
    <h4 class="mt-4">Fill in the Blank</h4>

    <div v-for="(q, index) in quizzes.fill_blank" :key="'fb'+index" class="card mb-3 p-3">

      <p><strong>{{ index+1 }}. {{ q.question }}</strong></p>

      <input
        type="text"
        class="form-control"
        v-model="answers.fill_blank[index]"
        placeholder="Enter answer"
      >

      <ResultBlock
        v-if="submitted"
        :correct="normalize(q.answer) === normalize(answers.fill_blank[index])"
        :answer="q.answer"
        :url="q.url"
      />

    </div>
  </div>


  <button class="btn btn-primary mt-3" @click="submitQuiz">
    Submit Answers
  </button>

</div>
</template>

<script setup>

import { reactive, ref, defineProps } from "vue"
import ResultBlock from "./ResultBlock.vue"

defineProps({
  quizzes: Object
})

const submitted = ref(false)

const answers = reactive({
  mcq: [],
  true_false: [],
  fill_blank: []
})

function submitQuiz(){
  submitted.value = true
}

function normalize(val){
  if(!val) return ""
  return val.toString().trim().toLowerCase()
}

</script>