let books = [];

// Fetch the books first
async function fetchBooks() {
    try {
        const res = await fetch("/books", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        });
        if (!res.ok) {
            console.error("Failed to fetch books:", res.status, res.statusText);
            books = [];
            return books;
        }
        books = await res.json();
        return books;
    } catch (err) {
        console.error("Error fetching books:", err);
        books = [];
        return books;
    }
}

// Fetch and log results
fetchBooks().then(b => console.log("Books: ", b)).catch(err => console.error(err));
