<template>
    <div class="tab-pane fade" id="section2">
        <div class="container">
            <i><label for="askInput" class="control-label">Ask me anything from Wistech Open books!</label></i>
            <input class="form-control" id="askInput" 
                placeholder="Enter your query here..."
                @keyup.enter="console.log('entered something')"
            >
        </div>

    </div>
</template>

<script setup>


</script>

<style>
#askInput {
    position: fixed;
    bottom: 10px;
    border: 2px solid crimson;
    max-width: 80vw;
}
</style>