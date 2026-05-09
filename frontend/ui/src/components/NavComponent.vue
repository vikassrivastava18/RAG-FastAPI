<template>
    <nav class="p-2 navbar navbar-light bg-light">
        <div class="d-flex justify-content-end">

                <router-link to="/ask" class="btn btn-outline-dark px-4 rounded-pill me-3">
                    Ask
                </router-link>
               
                <router-link to="/dialogue" class="btn btn-outline-dark px-4 rounded-pill">
                    Dialogue
                </router-link>
        </div>
    </nav>
</template>

<style>
nav {
    text-align: left;
    border-radius: 5px
}
.nav-link {
    margin-right: 10px;
}

</style>