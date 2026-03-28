<template>
    <nav class="p-2">
        <div class="d-flex justify-content-end">
            <router-link to="/" class="nav-link mx-4">
                Summary
            </router-link>
            <router-link to="/ask" class="nav-link mx-4">
                Ask
            </router-link>
            <router-link to="/quiz" class="nav-link mx-4">
                Quiz
            </router-link>
            <router-link to="/dialogue" class="nav-link mx-4">
                Dialogue
            </router-link>
        </div>
    </nav>
</template>

<style>
nav {
    /* color: #fff; */
    background-color: rgb(98, 201, 236);
    /* text-align: left; */
}
.nav-link {
    margin-right: 10px;
    font-size: larger;
}

</style>