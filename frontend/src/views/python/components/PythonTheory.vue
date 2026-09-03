<template>
    <div class="theory-container">
        <h3 style="text-align: center;">Cheat Sheet (Week 0) </h3>
        <div class="container">
            <div>
                <h4>1. Running Python</h4>
                <p>Write Python code in a <code>.py</code> file and run it from the terminal:</p>
                <pre><code>python hello.py</code></pre>
                <h4>2. Functions</h4>
                <p>A <strong>function</strong> performs an action. A value passed to a function is called an
                    <strong>argument</strong>.</p>
                <pre><code>print("Hello")

name = input("What's your name? ")</code></pre>

                <h4>3. Variables</h4>
                <p>A <strong>variable</strong> stores a value. The <code>=</code> operator assigns a value to a
                    variable.</p>
                <pre><code>name = "David" x = 10</code></pre>
                <h4>4. Comments &amp; Pseudocode</h4>
                <p><strong>Comments</strong> begin with <code>#</code> and explain code or record ideas.
                    <strong>Pseudocode</strong> describes the steps of a solution before writing actual code.</p>
                <pre><code># Ask the user for their name name = input("What's your name? ")</code></pre>
                <h4>5. Strings (<code>str</code>)</h4>
                <p>A <strong>string</strong> is text. <code>strip()</code> removes extra whitespace, while
                    <code>title()</code> capitalizes the first letter of each word.</p>
                <pre><code>name = input("What's your name? ")

name = name.strip()
name = name.title()

print(f"Hello, {name}")</code></pre>

                <h4>6. F-Strings</h4>
                <p><strong>F-strings</strong> provide a convenient way to insert variables into strings.</p>
                <pre><code>name = "David"

print(f"Hello, {name}")</code></pre>

                <h4>7. Numbers &amp; Casting</h4>
                <p><strong>int</strong> represents whole numbers and <strong>float</strong> represents decimal numbers.
                    Since <code>input()</code> returns a string, numerical input often needs to be converted.</p>
                <pre><code>x = int(input("What's x? ")) y = int(input("What's y? "))

print(x + y)</code></pre>

                <p>This conversion is called <strong>casting</strong>.</p>
                <pre><code>x = float(input("What's x? ")) y = float(input("What's y? ")) print(x + y)</code></pre>
                <h4>8. Operators</h4>
                <p>Common mathematical operators include <code>+</code> addition, <code>-</code> subtraction,
                    <code>*</code> multiplication, <code>/</code> division, and <code>%</code> modulo (remainder).</p>
                <pre><code>x = 10 y = 3

print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x % y)</code></pre>

                <h4>9. Rounding &amp; Formatting</h4>
                <p>Use <code>round()</code> to round numbers and f-strings to format output.</p>
                <pre><code>number = 10.567

print(round(number, 2))</code></pre>

                <p>F-strings can also control decimal places and add commas:</p>
                <pre><code>number = 1234.5678

print(f"{number:,.2f}")</code></pre>

                <h4>10. Custom Functions</h4>
                <p>Use <code>def</code> to create your own function. Python uses <strong>indentation</strong> to define
                    the function's body.</p>
                <pre><code>def hello(to): print("Hello,", to)

hello("David")</code></pre>

                <h4>11. Default Parameters</h4>
                <p>A parameter can have a <strong>default value</strong>. Python uses it when no argument is provided.
                </p>
                <pre><code>def hello(to="world"): print("Hello,", to)

hello("David")
hello()</code></pre>

                <p>The output is:</p>
                <pre><code>Hello, David Hello, world</code></pre>
                <h4>12. The <code>main()</code> Function</h4>
                <p>A <code>main()</code> function can organize the main logic of a program. It must be called for the
                    program to execute it.</p>
                <pre><code>def main(): name = input("What's your name? ") hello(name)

def hello(to):
print("Hello,", to)

main()</code></pre>

                <h3>13. Return Values</h3>
                <p>The <code>return</code> statement sends a value back from a function so it can be used elsewhere.</p>
                <pre><code>def square(n): return n * n

def main():
x = int(input("What's x? "))
result = square(x)

print("x squared is", result)


main()</code></pre>

                <h3>⭐ Key Terms to Remember</h3>
                <ul>
                    <li><strong>Function:</strong> Performs a specific action.</li>
                    <li><strong>Argument:</strong> A value passed to a function.</li>
                    <li><strong>Parameter:</strong> A variable accepted by a function.</li>
                    <li><strong>Variable:</strong> Stores a value.</li>
                    <li><strong>String:</strong> A sequence of text.</li>
                    <li><strong>int:</strong> A whole number.</li>
                    <li><strong>float:</strong> A decimal number.</li>
                    <li><strong>Casting:</strong> Converting a value from one data type to another.</li>
                    <li><strong>return:</strong> Sends a value back from a function.</li>
                    <li><strong>Indentation:</strong> Defines blocks of Python code.</li>
                    <li><strong>Comment:</strong> A note in code beginning with <code>#</code>.</li>
                    <li><strong>Readability:</strong> Code should be clear, organized, and easy to understand.</li>
                </ul>
            </div>
            <br>
            <a href="https://cs50.harvard.edu/python/notes/0/" target="_blank" rel="noopener noreferrer"
                class="theory-link">
                Week-0 Notes
            </a>
        </div>

        

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
}

.theory-iframe {
    width: 100%;
    min-height: 800px;
    border: 1px solid #dfe3e8;
    border-radius: 10px;
    background: #fff;
}
</style>