<template>

<section class="py-5 bg-light">
  <div class="container">
    <div class="row g-5">

      <!-- Image Column -->
      <div class="col-lg-6">
        <img
          src="https://cdn.prod.website-files.com/679c2851aa61fe501c78835f/684209eccec40c45cade6906_CVTC%202.avif"
          alt="About WisTech Open"
          class="rounded-4 shadow-lg w-100 object-fit-cover mt-0"
        />
      </div>

      <!-- Content Column -->
      <div class="col-lg-6">

        <!-- Main Heading -->
        <h4 class="display-6 fw-bold text-dark mt-2 mb-4">
          About WisTechfusion (V2)
        </h4>

        <!-- Paragraph -->
        <p class="text-secondary fs-5 lh-lg mb-4">
          WisTechfusion is an AI application created to help students in their study. 
          The digital books made available through WistechOpen have been integrated in the application. Students can 
          ask questions through chat, start a dialogue with AI agent on topics, learn from quizzes
          and prepare by answering AI generated questions.
        </p>
      </div>
    </div>
  </div>
</section>


</template>

<style scoped>
  .letter-spacing {
    letter-spacing: 1px;
  }

  .object-fit-cover {
    object-fit: cover;
    max-height: 650px;
  }

  section {
    background-image: linear-gradient(#f8f8f8, #f8f8f8de), url('@/assets/Blue_Flames.jpg');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: top;
  }

</style>