<template>
      <main>
        <div class="container my-2" id="mainContent">
            <div class="innerContainer p-2">
                <header>
                  <HeaderComponent />                    
                </header>

                <!-- Bootstap tabs -->
                <ul class="nav nav-tabs">
                    <li class="nav-item">
                        <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#section1">
                            Learn
                        </button>
                    </li>
                    <li class="nav-item">
                        <button class="nav-link" data-bs-toggle="tab" data-bs-target="#section2">
                            Ask
                        </button>
                    </li>
                </ul>

                <div class="tab-content mt-3">
                  <LearnComponent />
                  <AskComponent />                  
                </div>

            </div>
        </div>
      </main>
        

  
</template>

<script>
import HeaderComponent from './components/HeaderComponent.vue';
import AskComponent from './components/AskComponent.vue';
import LearnComponent from './components/LearnComponent.vue';

export default {
  name: 'App',
  components: {
    HeaderComponent,
    AskComponent,
    LearnComponent
  }
}
</script>

<style>
#mainContent {
    background: white;
    border: 1px solid #dfdfdf;
    border-radius: 10px;
    box-shadow: 0 5px 40px rgb(0, 0, 0, 4%);
}

#mainContent {
    min-height: 100vh;
}
</style>
