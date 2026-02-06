// ==============================================
// GLOBAL VARIABLES AND CONFIGURATION
// ==============================================
let bookData = null;
const API_ENDPOINTS = {
  books: "/admin/admin-books",
  upload: "/admin/upload-book/",
  extractChapters: "/extract-chapters/",
};

// ==============================================
// DOCUMENT READY HANDLER
// ==============================================
$(document).ready(function () {
  // Initialize all components
  initializeDataTable();
  setupFileUploadHandlers();
  setupEventListeners();
  loadBooks();

  // Form submission handler
  $("#submitBtn").click(handleFormSubmit);
});

// ==============================================
// CORE FUNCTIONALITY
// ==============================================

/**
 * Initialize DataTable with configuration
 */
function initializeDataTable() {
  $("#myTable").DataTable({
    responsive: true,
    searching: false,
    order: [[0, 'desc']],
    pageLength: 10,
    lengthMenu: [5, 10, 25, 50],
    columnDefs: [
      { orderable: true, targets: [5] },
    ],
    initComplete: function () {
      attachDynamicEventHandlers();
    },
  });
}

/**
 * Set up file upload handlers
 */
function setupFileUploadHandlers() {

  $("body").on(
    "change",
    "#chooseFile, #logoOne, #logoTwo, #editLogoOne, #editLogoTwo, #editBookFile",
    function () {
      const filename = $(this).val().split("\\").pop();
      const noFileElement = $(this).siblings(".file-select-name");
      const uploadDiv = $(this).closest(".file-upload");

      if (filename) {
        noFileElement.text(filename);
        uploadDiv.addClass("active");
      } else {
        noFileElement.text("No file chosen...");
        uploadDiv.removeClass("active");
      }
    }
  );
}

/**
 * Set up event listeners
 */
function setupEventListeners() {

  $("#popup-close").click(function () {
    $("#custom-popup").fadeOut();
  });

  $("body").on("change", ".chapter-select", function () {
    const bookId = $(this).data("book-id");
    const selectedValue = $(this).val();
    console.log(`Book ${bookId} chapter changed to: ${selectedValue}`);
  });
}

/**
 * Attach handlers to dynamically created elements
 */
function attachDynamicEventHandlers() {
  $("body").on("click", ".table-editBtn", function () {
    const bookId = $(this).data("book-id");
    editEntry(bookId);
  });


  $("body").on("click", ".table-viewBtn", function () {
    const bookId = $(this).data("book-id");
    viewEntry(bookId);
  });

  $("body").on("click", ".table-hideBtn", function () {
    const bookId = $(this).data("book-id");
    deleteEntry(bookId);
  });
}

// ==============================================
// BOOK MANAGEMENT FUNCTIONS
// ==============================================

/**
 * Load books from API
 */
async function loadBooks() {
  try {
    const response = await fetch(API_ENDPOINTS.books);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    bookData = await response.json();
    generateTableRows();
  } catch (error) {
    console.error("Error loading books:", error);
    showPopup("Error loading books: " + error.message);
  }
}

/**
 * Generate table rows from book data
 */

function generateTableRows() {
  const tbody = $("#myTable tbody");
  tbody.empty();

  if (!bookData || !Array.isArray(bookData)) {
    tbody.html(
      '<tr><td colspan="6" class="text-center">No books found</td></tr>'
    );
    return;
  }

  if ($.fn.DataTable.isDataTable("#myTable")) {
    $("#myTable").DataTable().clear().destroy();
  }

  // Append rows
  bookData.forEach((item) => {
    tbody.append(`
      <tr>
        <td class="text-center"><span>${item.id}</span></td>
        <td class="text-center"><span>${item.name || "N/A"}</span></td>
        <td class="text-center">
          <img src="/media/${item.logo1}" alt="Logo 1" style="max-width: 70px;">
        </td>
        <td class="text-center">
          ${item.logo2 ? `<img src="/media/${item.logo2}" alt="Logo 2" style="max-width: 70px;">` : "None"}
        </td>
        <td class="text-center">
          <div class="chapter-container chepterList">
            <ul class="list list--main" id="js-list"></ul>
          </div>
          <select class="form-select chapter-select" data-book-id="${item.id}">
            <option value="">Make a Selection</option>
            ${(item.chaptersTopics || [])
        .map(topic => `<option value="${topic}">${topic}</option>`)
        .join("")}
          </select>
        </td>
        <td class="text-center actionCol">
          <button type="button" class="table-editBtn custooltip" onclick="editEntry(${item.id})" data-book-id="${item.id}">
            <i class="fa-solid fa-pen"></i>
            <span class="custooltiptext">Edit</span>
          </button>
          <button type="button" class="table-viewBtn custooltip activated disabled" onclick="changeStatus(${item.id}, 1)" data-book-id="${item.id}">
            <i class="fa-solid fa-eye"></i>
            <span class="custooltiptext">Activated</span>
          </button>
          <button type="button" class="table-hideBtn custooltip de-actived" onclick="changeStatus(${item.id}, 0)" data-book-id="${item.id}">
            <i class="fa-solid fa-eye-slash"></i>
            <span class="custooltiptext">De-activated</span>
          </button>
        </td>
      </tr>
    `);
  });


  $("#myTable").DataTable({
    pageLength: 5,
    lengthMenu: [5, 10, 25, 50],
    ordering: true,
  });
}


/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
  e.preventDefault();

  const bookName = $("#bookName").val();
  const disclaimer = $("#disclaimer").val();
  const bookFile = $("#chooseFile")[0].files[0];
  const logo1 = $("#logoOne")[0].files[0];
  const logo2 = $("#logoTwo")[0].files[0];


  if (!bookName || !disclaimer || !bookFile) {
    showPopup("Please fill all required fields");
    return;
  }


  const formData = new FormData();
  formData.append("book_name", bookName);
  formData.append("disclaimer", disclaimer);
  formData.append("book_file", bookFile);

  if (logo1) formData.append("logo1", logo1);
  if (logo2) formData.append("logo2", logo2);

  try {

    const submitBtn = $("#submitBtn");
    submitBtn
      .prop("disabled", true)
      .html(
        '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...'
      );


    const response = await fetch(API_ENDPOINTS.upload, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error(`Error: ${response.statusText}`);


    const data = await response.json();
    showPopup("Book processed successfully!");

    location.reload();

  }
  catch (error) {

    showPopup("This book name already exists");

  } finally {
    $("#submitBtn").prop("disabled", false).text("Submit");
  }
}

// ==============================================
// CRUD OPERATIONS
// ==============================================

function editEntry(id) {
  const book = bookData.find((item) => item.id == id);
  if (!book) {
    showPopup("Book not found");
    return;
  }

  $("#editBookId").val(book.id);
  $("#editBookName").val(book.book_name || book.name);


  $("#editDiscalimer").val(book.disclaimer);

  if (book.logo1) {
    $("#currentLogoOne .current-logo-path").text(book.logo1);
    $("#currentLogoOne").show();
  } else {
    $("#currentLogoOne").hide();
  }

  if (book.logo2) {
    $("#currentLogoTwo .current-logo-path").text(book.logo2);
    $("#currentLogoTwo").show();
  } else {
    $("#currentLogoTwo").hide();
  }

  $("#editBookModal").modal("show");
}

$(document).on('click', '#saveBookChanges', function () {
  const formData = new FormData();
  const bookId = $("#editBookId").val();


  if (!$("#editBookName").val().trim() || !$("#editDiscalimer").val().trim()) {
    showPopup("Please fill all required fields", "error");
    return;
  }

  formData.append("book_name", $("#editBookName").val().trim());
  formData.append("disclaimer", $("#editDiscalimer").val().trim());
  const editBookName = $("#editBookName").val();
  $.ajax({
    url: `/books`,
    type: 'GET',
    dataType: 'json',
    success: function (response) {

      const bookIndex = bookData.find(item => item.name == editBookName);


      const logo1File = $("#editLogoOne")[0].files[0];
      if (logo1File) formData.append("logo1", logo1File);

      const logo2File = $("#editLogoTwo")[0].files[0];
      if (logo2File) formData.append("logo2", logo2File);

      const saveBtn = $(this);
      saveBtn.prop("disabled", true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...');

      // Call FastAPI endpoint
      $.ajax({
        url: `/update-book/${bookId}`,
        type: "PUT",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
          showPopup("Book updated successfully", "success");
          $("#editBookModal").modal("hide");

          // Update the book in local data and refresh UI
          const index = bookData.findIndex(b => b.id == bookId);
          if (index !== -1) {
            bookData[index] = response;

            location.reload();  // Your function to update the UI
          }

          // Reset form
          $("#editBookForm")[0].reset();
          $(".file-select-name").text("No file chosen...");
        },
        error: function (xhr) {
          const errorMsg = xhr.responseJSON?.detail.message || "Failed to update book";
          showPopup(errorMsg, "error");
        },
        complete: function () {
          saveBtn.prop("disabled", false).text("Save Changes");
        }
      });
      // }
      // else {
      //   showPopup("This book name already exists");

      // }
    },
    error: function (xhr, status, error) {
      let errorMessage = "Error updating book status";
      if (xhr.responseJSON && xhr.responseJSON.detail) {
        errorMessage = xhr.responseJSON.detail;
      }
      showPopup(errorMessage);
    }
  });

});



// File input change handlers
$(document).on('change', '#editLogoOne', function () {
  const fileName = this.files[0] ? this.files[0].name : "No file chosen...";
  $("#editNoFileOne").text(fileName);
});

$(document).on('change', '#editLogoTwo', function () {
  const fileName = this.files[0] ? this.files[0].name : "No file chosen...";
  $("#editNoFileTwo").text(fileName);
});

// Initialize edit buttons (for dynamically created content)
$(document).on('click', '.table-editBtn', function () {
  const bookId = $(this).data('book-id');
  editEntry(bookId);
});



function changeStatus(id, status) {
  const book = bookData.find((item) => item.id == id);
  if (!book) {
    showPopup("Book not found");
    return;
  }

  $.ajax({
    url: `/book-status/${id}/${status}/`,  // Matches your FastAPI route
    type: 'PATCH',                       // HTTP PATCH method
    dataType: 'json',                    // Expect JSON response
    success: function (response) {
      showPopup(response.message);       // Show success message
      // Optional: Update local bookData or refresh UI
      const bookIndex = bookData.findIndex(item => item.id == id);
      if (bookIndex !== -1) {
        bookData[bookIndex].is_active = (status == 1);

      }

    },
    error: function (xhr, status, error) {
      let errorMessage = "Error updating book status";
      if (xhr.responseJSON && xhr.responseJSON.detail) {
        errorMessage = xhr.responseJSON.detail;
      }


      showPopup(errorMessage);
    }
  });
}


function viewEntry(id) {
  // Implement view functionality
}



// ==============================================
// UI HELPER FUNCTIONS
// ==============================================

function showPopup(message) {
  const popup = $("#custom-popup");
  $("#popup-message").text(message);
  popup.fadeIn();
  setTimeout(() => popup.fadeOut(), 4000);
}

function renderChapterOnTable(chapters) {
  const chapterList = document.getElementById("js-list");
  chapterList.innerHTML = '<li class="loading">Loading chapters...</li>';

  chapters.forEach((chapter, index) => {
    const chapterItem = document.createElement("li");
    chapterItem.className = "list-item--collapse--arrow";
    chapterItem.dataset.chapterId = index;

    chapterItem.innerHTML = `
            <div class="list-item__header chapter-select">
                <button class="list-item__btn-arrow">
                    <input type="checkbox" id="chapter-${index}" data-chapter-id="${index}">
                </button>
                <a href="#" class="list-item__title open-topics">${chapter.chapter_name
      }</a>
            </div>
            <ul class="list-item__body list chapter-topics-select" style="display: none;">
                ${chapter.subtopics
        .map(
          (subtopic, subIndex) => `
                    <li class="list-item--collapse--arrow">
                        <div class="list-item__header">
                            <button class="list-item__btn-arrow">
                                <input type="checkbox" id="topic-${index}-${subIndex}" 
                                       class="topic-checkbox" 
                                       data-chapter-id="${index}"
                                       data-topic-id="${subIndex}">
                            </button>
                            <a href="#" class="list-item__title">${subtopic.subtopic_name}</a>
                        </div>
                    </li>
                `
        )
        .join("")}
            </ul>
        `;
    chapterList.appendChild(chapterItem);
  });
}




