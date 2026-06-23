<template>
    <nav class="p-2 navbar">
        <div class="d-flex justify-content-end">

                <router-link to="/ask" class="btn btn-light btn-outline-dark px-4 rounded-pill me-4">
                    Ask
                </router-link>
               
                <router-link to="/dialogue" class="btn btn-light btn-outline-dark px-4 rounded-pill me-4 ms-2">
                    Dialogue
                </router-link>

             
        </div>
    </nav>
</template>

<style>
nav {
    text-align: left;
    border-radius: 5px;
    background: linear-gradient(90deg, #7badd9 0%, #5e98cb 50%, #3f82bd 100%);
}
.nav-link {
    margin-right: 10px;
}

</style>