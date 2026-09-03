<template>
    <div class="theory-container">
        <h2>Week 0 </h2>
        <h5>Summary</h5>
        Python programming begins with writing and running simple programs in VS Code, such as using
        <code>print()</code> to display “hello, world.” The lesson explains that <b>functions</b> perform actions,
        <b>variables</b> store values, and <b>comments</b> document code or describe planned steps through pseudocode.
        It introduces <b>strings</b> and their methods like <code>strip()</code> and <code>title()</code>, along with
        f-strings for formatting text. Since <code>input()</code> returns text, <b>casting</b> with <code>int()</code>
        or <code>float()</code> is needed for numerical calculations. The lesson also covers rounding and formatting
        numbers, emphasizes <b>readable code</b>, and explains how to create custom functions using <code>def</code>,
        parameters, default values, and indentation. Finally, it introduces <code>return</code>, which allows a function
        to send a calculated value back to another part of the program, while emphasizing that bugs and errors are a
        normal and useful part of learning to program.
        
        <br><br>
        <a href="https://cs50.harvard.edu/python/notes/0/" target="_blank" rel="noopener noreferrer"
            class="theory-link">
            Open CS50 Python Notes
        </a>
    </div>
</template>

<style scoped>
.theory-container {
    padding: 24px;
    /* background: #f7f9fc;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06); */
}

h2 {
    margin: 0 0 16px;
    font-size: 1.5rem;
    color: #1f2937;
}

.theory-iframe {
    width: 100%;
    min-height: 800px;
    border: 1px solid #dfe3e8;
    border-radius: 10px;
    background: #fff;
}
</style>