<template>

<!-- <PythonComponent /> -->
 <div class="container">
        <h3 class="p-2">
            <img src="../../assets/snake_svg.svg" alt="" width="50">
            Python
        </h3>
        
        <RouterView />
        
    </div>
    
</template>


<style scoped>
.theory-container {
    padding: 24px;
    /* background: #f7f9fc;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06); */
}

h3 {
    margin: 0 0 16px;
    /* font-size: 1.5rem; */
    color: maroon;
    text-align: center;
}

.theory-iframe {
    width: 100%;
    min-height: 800px;
    border: 1px solid #dfe3e8;
    border-radius: 10px;
    background: #fff;
}

.topic-link {
    font-size: 1.25rem;
}
</style>