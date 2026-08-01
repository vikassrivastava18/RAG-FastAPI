<template>
    <nav class="p-2 navbar">
        <div class="d-flex justify-content-end">
            <router-link to="/ask" class="nav-link text_white px-4 py-1 me-2">
              Ask
            </router-link>

            <router-link to="/dialogue" class="nav-link text_white px-4 py-1 me-2">
                Dialogue
            </router-link>

            <router-link to="/answer" class="nav-link text_white px-4 py-1">
                Answer
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
    font-size: large;
    color: #fff;
}

.router-link-exact-active, .router-link-active {
    font-weight: bold;
    background-color: #7ef473;
    border: none;
    /* border-radius: 15px; */
}

.text_white {
    color: white;
}


:deep(.router-link-active) {
    color: #fff;
}

:deep(a:active) {
    color: #fff;
}
.navbar {
    color: #fff;
}
</style>