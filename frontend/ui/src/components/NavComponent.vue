<template>
    <nav class="navbar navbar-expand-lg navbar-light">
        <div class="container-fluid">
            <router-link to="/" class="nav-link">
                Summary
            </router-link>
            <router-link to="/ask" class="nav-link">
                Ask
            </router-link>
            <router-link to="/quiz" class="nav-link">
                Quiz
            </router-link>
            <!-- <router-link to="/" class="nav-link">
                Dialogue
            </router-link> -->
        </div>
    </nav>
</template>

<style>
.navbar {
    color: #fff;
    background-color: rgb(67, 132, 154);
    /* text-align: left; */
}

</style>