<template>
    <main>
        <div class="container my-2" id="mainContent">
            <div class="innerContainer p-2">
                <header>
                    <HeaderComponent />                    
                </header>

                <NavComponent />

                <div class="tab-content mt-3">
                    <RouterView />                  
                </div>

            </div>
        </div>
    </main>
  
</template>

<script setup>
import HeaderComponent from './components/HeaderComponent.vue';
import NavComponent from './components/NavComponent.vue';

</script>

<style>
#mainContent {
    background: white;
    border: 1px solid #dfdfdf;
    border-radius: 10px;
    box-shadow: 0 5px 40px rgb(0, 0, 0, 4%);
    height: 100%; 
    background-image: linear-gradient(#f8f8f8, #f8f8f8de), url('@/assets/Blue_Flames.jpg');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: top;
}

#mainContent {
    min-height: 100vh;
}
</style>
