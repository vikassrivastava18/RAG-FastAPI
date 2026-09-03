<template>
    <nav class="p-2 navbar">
        <div class="d-flex justify-content-end">
            <router-link to="/" class="nav-link text_white px-4 py-1 me-2">
              HOME
            </router-link>
             <router-link to="/python" class="nav-link text_white px-4 py-1 me-2">
                PYTHON
            </router-link>
            <router-link to="/sql" class="nav-link text_white px-4 py-1 me-2">
                SQL
            </router-link>
            <router-link to="/cybersecurity" class="nav-link text_white px-4 py-1">
                CYBERSECURITY
            </router-link>
            <!-- <img src="../assets/logo.svg" width="100" alt=""> -->

        </div>
    </nav>
</template>

<style scoped>
nav {
    text-align: left;
    border: 1px dotted grey;
    border-radius: 5px;
    /* background: linear-gradient(90deg, #dcdfe2 0%, #5e98cb 50%, #3f82bd 100%); */
}

.nav-link {
    margin-right: 10px;
    font-size: large;
    color: #000;
}

.router-link-exact-active, .router-link-active {
    background-color: #7ef473;
    border: none;
    color: #000;
}

.text_white {
    color: #000;
}

.navbar {
    color: #000;
}
img {
    float: right;
}
</style>