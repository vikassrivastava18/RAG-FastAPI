const {
  Document,
  Packer,
  Paragraph,
  Table,
  TableRow,
  TableCell,
  TextRun,
  AlignmentType,
  WidthType,
  VerticalAlign,
  BorderStyle,
  ImageRun,
} = docx;
//=====================================================================================

// ======================================================================================

function clearInputs() {
  $(".onCngMetril").prop("checked", false);
  $("#questionCount").val("");
}

const questionInput = document.getElementById("questionCount");

questionInput.addEventListener("input", () => {
  let value = questionInput.value;

  // Remove anything that is NOT a digit (0-9)
  value = value.replace(/[^0-9]/g, "");

  // Convert to integer number
  let intValue = parseInt(value, 10);

  // If empty or NaN, clear input
  if (isNaN(intValue)) {
    questionInput.value = "";
    return;
  }

  // Clamp value between 1 and 50
  if (intValue < 1) intValue = 1;
  if (intValue > 50) intValue = 50;

  questionInput.value = intValue;
});

document.addEventListener("DOMContentLoaded", () => {
  window.showPopup = function (message, type = "info") {
    const popup = document.getElementById("custom-popup");
    const messageBox = document.getElementById("popup-message");

    if (!popup || !messageBox) return;

    messageBox.textContent = message;

    // Optional: change background color based on type (success/warning/info)
    popup.className = `popup-overlay ${type}`;
    popup.style.display = "flex";

    // // Auto-close after 3 seconds
    // setTimeout(() => {
    //   popup.style.display = 'none';
    // }, 3000);
  };

  const closeBtn = document.getElementById("popup-close");
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      document.getElementById("custom-popup").style.display = "none";
    });
  }
});

// =======================================================================================
// ----------------------------------------------------------------------------------------------
// resizable script
const resizableDiv = document.getElementById("resizable-div");
const divider = document.getElementById("divider");
let isResizing = false;
divider.addEventListener("mousedown", (event) => {
  isResizing = true;
});
document.addEventListener("mousemove", (event) => {
  if (isResizing) {
    const newWidth = event.clientX - resizableDiv.getBoundingClientRect().left;
    if (newWidth > 50) {
      resizableDiv.style.width = `${newWidth}px`;
    }
  }
});

document.addEventListener("mouseup", () => {
  isResizing = false;
});

// ========================
// global
// ========================
let selectedMetarialType = null;
let selectedQuestionTypes = [];
let no_of_question = null;
let materialType = null;
let selectedTopics = [];
let notebookMeta = null;
let questionTypes;

let notes = document.getElementById("exampleFormControlTextarea1").value;

// ==============================================================================

function showLoader() {
  // Show the loader
  document.getElementById("loader").style.display = "block";
  document.getElementById("loader-overlay").classList.add("active");
  document.getElementById("loader-overlay").style.display = "block";
  $("#custom-popup").css("display", "none");
}
function hideLoader() {
  // Hide loader and remove fade effect
  document.getElementById("loader").style.display = "none";
  document.getElementById("loader-overlay").classList.remove("active");
  document.getElementById("loader-overlay").style.display = "none";
}

// ==============================================================================

// Show/hide question count input based on checkbox selection
$(".onCngMetril").change(function () {
  if ($(".onCngMetril:checked").length > 0) {
    $("#questionCountField").show();
  } else {
    $("#questionCountField").hide();
  }
});

// Event listener for the main select dropdown
$("#mySelect").on("change", function () {
  selectedValue = $(this).val();
  selectedMetarialType = selectedValue;
  // Hide the question count field if no checkboxes are associated with the selected option
  if (
    selectedValue == "caseStudy" ||
    selectedValue == "quizTest" ||
    selectedValue == "workSheet"
  ) {
    $("#quesType").addClass("d-block");
  } else {
    $("#quesType").removeClass("d-block");
    $("#questionCountField").hide(); // Hide the question count input field
    $("#questionCount").val(""); // Clear the input value
  }
});

// question type value
$(".onCngMetril").change(function () {
  const checkboxId = this.id;
  if (this.checked) {
    // Add if not already present
    if (!selectedQuestionTypes.includes(checkboxId)) {
      selectedQuestionTypes.push(checkboxId);
    }
  } else {
    // Remove if unchecked
    selectedQuestionTypes = selectedQuestionTypes.filter(
      (id) => id !== checkboxId
    );
  }

  // Show/hide question count input
  if (selectedQuestionTypes.length > 0) {
    $("#questionCountField").show();
  } else {
    $("#questionCountField").hide();
  }

  console.log("Current selected question types:", selectedQuestionTypes);
});

//  question count value
$("#questionCount").on("input", function () {
  questionCount = $(this).val().trim();
  console.log("Question Count updated:", questionCount);
});

// select dropdown JS start
$(document).ready(function () {
  $("#mySelect").select2({
    minimumResultsForSearch: Infinity,
    placeholder: "Open this select menu",
    allowClear: false,
  });

  $("#mySelect2").select2({
    placeholder: "Open this select menu",
    allowClear: false,
  });

  $("#mySelect4").select2({
    minimumResultsForSearch: Infinity,
    placeholder: "Make a Selection",
    allowClear: false,
  });

  $("#mySelect5").select2({
    placeholder: "Open this select menu",
    allowClear: false,
  });

  $("#mySelect3").select2({
    minimumResultsForSearch: Infinity,
    placeholder: "Make a Selection",
    allowClear: false,
    // multiple: true
  });
});

//  new version
// Initially hide the chapter selection container
document.getElementById("select-chapter").style.display = "none";

// Store the current book data globally for reference
let currentBookData = null;

async function toggleChapterSelection() {
  // debugger;
  const selectElement = document.getElementById("mySelect2");
  const chapterContainer = document.getElementById("select-chapter");

  if (selectElement.value) {
    chapterContainer.style.display = "block";
    // When a textbook is selected, fetch its chapters
    await fetchChapters(selectElement.value);
  } else {
    chapterContainer.style.display = "none";
    // Clear the chapter list when no book is selected
    document.getElementById("js-list").innerHTML = "";
  }
}

async function fetchChapters(textbookId) {
  try {
    // Show loading state
    const chapterList = document.getElementById("js-list");
    chapterList.innerHTML = '<li class="loading">Loading chapters...</li>';

    // Fetch chapters for the selected textbook
    const response = await fetch("/chapter-subtopics/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ book_id: textbookId }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    currentBookData = data; // Store the response data

    // Clear loading state and existing chapters
    chapterList.innerHTML = "";

    if (!data.chapters || data.chapters.length === 0) {
      chapterList.innerHTML =
        '<li class="no-chapters">No chapters available for this textbook</li>';
      return;
    }

    // Generate new chapters from API response
    data.chapters.forEach((chapter, index) => {
      const chapterItem = document.createElement("li");
      chapterItem.className = "list-item--collapse--arrow";
      chapterItem.dataset.chapterId = index;

      chapterItem.innerHTML = `
        <div class="list-item__header chapter-select">
          <button class="list-item__btn-arrow">
            <input type="checkbox" id="chapter-${index}" 
            data-chapter-id="${index}" data-ch-id="${chapter.id}"
            class="chapterCheck">
          </button>
          <a href="#" class="list-item__title open-topics">${chapter.chapter_name}</a>
        </div>
        <ul class="list-item__body list chapter-topics-select" style="display: none;">
          ${chapter.subtopics
          .map(
            (subtopic, subIndex) => `
            <li class="list-item--collapse--arrow">
              <div class="list-item__header">
                <button class="list-item__btn-arrow">
                  <input type="checkbox" 
                         id="topic-${index}-${subIndex}" 
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
  } catch (error) {
    console.error("Error fetching chapters:", error);
    const chapterList = document.getElementById("js-list");
    chapterList.innerHTML =
      '<li class="error">Failed to load chapters. Please try again.</li>';
  }
}

// Get all selected chapters and topics
function getSelectedContent() {
  // debugger;
  if (!currentBookData) return null;

  const selectedChapters = [];

  const chapterCheckboxes = document.querySelectorAll(
    '.chapter-select input[type="checkbox"]:checked'
  );

  chapterCheckboxes.forEach((chapterCB) => {
    const chapterId = chapterCB.dataset.chapterId;
    const chapter = currentBookData.chapters[chapterId];

    selectedTopics = [];
    const topicCheckboxes = document.querySelectorAll(
      `.topic-checkbox[data-chapter-id="${chapterId}"]:checked`
    );

    topicCheckboxes.forEach((topicCB) => {
      const topicId = topicCB.dataset.topicId;
      selectedTopics.push(chapter.subtopics[topicId].subtopic_name);
    });
    console.log(selectedTopics, "selectedTopics");

    selectedChapters.push({
      chapter_title: chapter.chapter_title,
      selected_topics:
        selectedTopics.length > 0
          ? selectedTopics
          : chapter.subtopics.map((t) => t.subtopic_name),
    });
  });

  return {
    book_id: document.getElementById("mySelect2").value,
    book_name: currentBookData.notebook_name,
    selected_chapters: selectedChapters,
  };
}

document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("js-list")
    .addEventListener("change", function (event) {
      // Handle chapter checkbox changes
      if (event.target.matches('.chapter-select input[type="checkbox"]')) {
        const chapterId = event.target.dataset.chapterId;
        const subchapters = document.querySelectorAll(
          `.topic-checkbox[data-chapter-id="${chapterId}"]`
        );
        const isChecked = event.target.checked;
        setTimeout(() => {
          updateSelectedTopics();
        }, 500);

        subchapters.forEach((subchapter) => {
          subchapter.checked = isChecked;
        });
      }

      // Handle topic checkbox changes
      if (event.target.matches(".topic-checkbox")) {
        // debugger;
        const chapterId = event.target.dataset.chapterId;
        const chapterCheckbox = document.querySelector(
          `.chapter-select input[type="checkbox"][data-chapter-id="${chapterId}"]`
        );
        const topicCheckboxes = document.querySelectorAll(
          `.topic-checkbox[data-chapter-id="${chapterId}"]`
        );
        const checkedCount = document.querySelectorAll(
          `.topic-checkbox[data-chapter-id="${chapterId}"]:checked`
        ).length;

        updateSelectedTopics();

        // Update chapter checkbox state
        if (checkedCount === 0) {
          chapterCheckbox.checked = false;
          chapterCheckbox.indeterminate = false;
        } else if (checkedCount === topicCheckboxes.length) {
          chapterCheckbox.checked = true;
          chapterCheckbox.indeterminate = false;
        } else {
          chapterCheckbox.checked = false;
          chapterCheckbox.indeterminate = true;
        }
      }
    });

  function updateSelectedTopics() {
    // debugger;
    selected_topics = [];

    document.querySelectorAll(".topic-checkbox:checked").forEach((topic) => {
      const chapterId = topic.dataset.chapterId;
      const topicId = topic.dataset.topicId;

      if (currentBookData?.chapters[chapterId]?.subtopics[topicId]) {
        selected_topics.push(
          currentBookData.chapters[chapterId].subtopics[topicId].subtopic_name
        );
      }
    });

    console.log("Updated selected_topics2:--->", selected_topics);
  }

  // Handle opening/closing of topics
  document
    .getElementById("js-list")
    .addEventListener("click", function (event) {
      if (event.target.matches(".open-topics")) {
        event.preventDefault();
        const chapterBody = event.target
          .closest("li.list-item--collapse--arrow")
          .querySelector(".list-item__body");
        const isHidden =
          chapterBody.style.display === "none" || !chapterBody.style.display;

        chapterBody.style.display = isHidden ? "block" : "none";

        // Toggle arrow icon if you have one
        const arrowBtn = event.target
          .closest(".list-item__header")
          .querySelector(".list-item__btn-arrow");
        if (arrowBtn) {
          arrowBtn.classList.toggle("expanded", isHidden);
        }
      }
    });
});

////// institution
$(document).ready(function () {
  // Array of institutions (could also fetch this from an API)
  const institutions = [
    { value: "1", name: "Blackhawk Technical College" },
    { value: "2", name: "Chippewa Valley Technical College" },
    { value: "3", name: "Fox Valley Technical College" },
    { value: "4", name: "Gateway Technical College" },
    { value: "5", name: "Lakeshore Technical College" },
    { value: "6", name: "Madison Area Technical College" },
    { value: "7", name: "Milwaukee Area Technical College" },
    { value: "8", name: "Mid-State Technical College" },
    { value: "9", name: "Moraine Park Technical College" },
    { value: "10", name: "Nicolet College" },
    { value: "11", name: "Northcentral Technical College" },
    { value: "12", name: "Northeast Wisconsin Technical College" },
    { value: "13", name: "Northwood College" },
    { value: "14", name: "Western Technical College" },
    { value: "15", name: "Southwest Wisconsin Technical College" },
    { value: "16", name: "Waukesha County Technical College" },
    { value: "17", name: "Others" },
  ];

  // Get the select element
  const $select = $("#mySelect5");

  // Clear existing options except the first one
  $select.empty().append("<option selected>Make a Selection</option>");

  // Add institutions dynamically
  $.each(institutions, function (index, institution) {
    $select.append(
      $("<option>", {
        value: institution.value,
        text: institution.name,
      })
    );
  });

  // Initialize Select2
  $select.select2({
    placeholder: "Select Your Institution",
    allowClear: false,
  });

  // Log selected value when changed
  $select.on("change", function () {
    const selectedValue = $(this).val();
    const selectedText = $(this).find("option:selected").text();
    // Assign to global variable (use `window` for explicit global)
    window.institution = selectedText; // Or just `institution` in non-module scripts

    console.log("Selected Value:", selectedValue);
    console.log("Selected Text:", selectedText);
  });
});

$(document).ready(function () {
  // Array of languages
  const languages = [
    { value: "English", name: "English" },
    { value: "French", name: "French" },
    { value: "German", name: "German" },
    { value: "Hmong", name: "Hmong" },
    { value: "Spanish", name: "Spanish" },
  ];

  const defaultLanguage = "English";

  const $languageSelect = $("#mySelect4");

  // Empty the select
  $languageSelect.empty();

  // Add language options
  $.each(languages, function (index, language) {
    $languageSelect.append(
      $("<option>", {
        value: language.value,
        text: language.name,
        selected: language.value === defaultLanguage,
      })
    );
  });

  // Set global variable to default on load
  window.language = defaultLanguage;

  // Track changes
  $languageSelect.on("change", function () {
    const selectedValue = $(this).val();
    const selectedText = $(this).find("option:selected").text();

    console.log("Selected Language Value:", selectedValue);
    console.log("Selected Language Text:", selectedText);

    window.language = selectedValue;
  });
});

// ============================================================
// book fetch api call

$(document).ready(function () {
  // Fetch books from API and populate select
  $.get("/books", function (response) {
    const $select = $("#mySelect2");

    // Clear existing options except the default
    $select
      .empty()
      .append('<option selected value="">Make a Selection</option>');

    // Add books from API response
    response.forEach(function (book) {
      $select.append(
        $("<option>", {
          value: book.id,
          text: book.name,
        })
      );
    });

    // Initialize Select2 after populating options
    $select.select2({
      placeholder: "Select a resource",
      allowClear: false,
    });

    // Track selection changes
    $select.on("change", function () {
      const selectedId = $(this).val();
      const selectedBook = response.find((book) => book.id == selectedId);

      if (selectedBook) {
        console.log("Selected Book:", {
          id: selectedBook.id,
          name: selectedBook.name,
        });
        // Store in global variable if needed
        window.selectedBook = selectedBook;
        window.book_id = selectedBook.id;

        $.get(`/books/${window.book_id}/footer`, function (response) {
          console.log(response);
          notebookMeta = response;
        });
      }
    });
  }).fail(function (error) {
    console.error("Error loading books:", error);
    // Optionally show error message to user
    $("#mySelect2").after(
      '<div class="error-message">Failed to load resources. Please refresh the page.</div>'
    );
  });

  $("#mySelect").on("change", function () {
    clearInputs();
  });
});

// ===============================================================================================


function getSelectedChaptersWithSubchapters() {
  const selected = [];

  // Find all chapter checkboxes that are checked
  const chapterCheckboxes = document.querySelectorAll('input[type="checkbox"][id^="chapter-"]:checked');

  chapterCheckboxes.forEach(chapterCheckbox => {
    const chapterItem = chapterCheckbox.closest('.list-item--collapse--arrow');

    // Find chapter title
    const chapterTitleElement = chapterItem.querySelector('.list-item__title.open-topics');
    const chapterName = chapterTitleElement ? chapterTitleElement.textContent.trim() : null;

    // Prepare chapter object
    const chapterData = {
      chapter: chapterName,
      subchapters: []
    };

    // Find all checked subchapter/topic checkboxes inside this chapter
    const topicCheckboxes = chapterItem.querySelectorAll('input[type="checkbox"].topic-checkbox:checked');

    topicCheckboxes.forEach(topicCheckbox => {
      const topicHeader = topicCheckbox.closest('.list-item__header');
      const topicTitleElement = topicHeader.querySelector('.list-item__title');
      const topicName = topicTitleElement ? topicTitleElement.textContent.trim() : null;
      if (topicName) {
        chapterData.subchapters.push(topicName);
      }
    });

    // Add to the list
    selected.push(chapterData);
  });

  return selected;
}

function resetFormAfterSubmission() {
  $("#mySelect").val("Make a selection").trigger("change.select2");

  document
    .querySelectorAll('#quesType input[type="checkbox"]')
    .forEach((checkbox) => {
      checkbox.checked = false;
    });

  document.getElementById("questionCountField").style.display = "none";
  document.getElementById("questionCount").value = "";

  $("#mySelect2").val("").trigger("change.select2");

  document.getElementById("js-list").innerHTML = "";
  document.getElementById("select-chapter").style.display = "none";

  document.getElementById("exampleFormControlTextarea1").value = "";

  $("#mySelect4").val("English").trigger("change");

  $("#mySelect5").val("Make a Selection").trigger("change.select2");
  document.getElementById("exampleFormControlInput1").value = "";

  selectedMetarialType = null;
  selectedQuestionTypes = [];
  selected_topics = [];
  questionCount = null;
  notes = "";
  currentBookData = null;
  selectedBook = null;
  notebookMeta = null;
}

// =======================================================
document.querySelector("#submitBtn").addEventListener("click", async (e) => {
  e.preventDefault();
  notes = document.getElementById("exampleFormControlTextarea1").value;

  $(".pdfviewer-container").addClass("pdfShow");

  if (!validateForm()) {
    return false;
  }

  // Get all checkboxes with the class 'onCngMetril'
  const checkboxes = document.querySelectorAll('.onCngMetril');

  // Filter the checkboxes to find those that are checked
  const selectedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked).map(checkbox => checkbox.id);

  // Get checked chapters IDs
  const chapterBoxes = document.querySelectorAll('.chapterCheck');
  const chapterChecked = Array.from(chapterBoxes).filter(checkbox => checkbox.checked).map(checkbox => checkbox.getAttribute('data-ch-id'));

  // Save form data
  const email = document.getElementById("exampleFormControlInput1")?.value || "";
  let payloads = {
    material_type: selectedMetarialType,
    question_types: selectedCheckboxes,
    chapters: chapterChecked,
    topics: selected_topics,
    notes: notes,
    institution: institution,
    email: email,
    language: language,
    number_of_question: questionCount,
  };

  try {
    // Send to FastAPI backend
    await fetch("/save-form/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payloads),
    });

    showLoader();

    // Construct main payload based on material type
    let bookName = $('#mySelect2').select2('data')[0].text;

    let payload;
    if (selectedMetarialType === "powerPoint") {
      payload = {
        chapters: chapterChecked,
        topics: selected_topics,
        textbook_name: bookName,
        language: language,
        notes: notes,
        selections: getSelectedChaptersWithSubchapters()
      };
    } else {
      payload = {
        question_types: selectedCheckboxes,
        chapters: chapterChecked,
        topics: selected_topics,
        notes: notes,
        institution: institution,
        language: language,
        number_of_question: questionCount,
        textbook_name: bookName,
        selections: getSelectedChaptersWithSubchapters()
      };
    }

    // Determine API endpoint
    let apiUrl;
    switch (selectedMetarialType) {
      case "quizTest":
        apiUrl = "/llm/quiz-response/";
        break;
      case "studyGuide":
        apiUrl = "/llm/summarize/";
        break;
      case "caseStudy":
        apiUrl = "/llm/case-study/";
        break;
      case "workSheet":
        apiUrl = "/worksheet/";
        break;
      case "powerPoint":
        apiUrl = "/llm/preview-slides/";
        break;
      default:
        showPopup("Please select a valid material type!");
        return;
    }

    const response = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error(`API request failed with status ${response.status}`);

    const data = await response.json();
    const resultElement = document.querySelector("#result");
    resultElement.innerHTML = ""; // Clear previous results

    // Process response based on material type
    switch (selectedMetarialType) {
      case "caseStudy":
        const caseResults = Object.values(data.data || {});
        resultElement.textContent = [...new Set(caseResults)].join("\n\n");
        break;

      case "workSheet":
        resultElement.textContent = typeof data.worksheet === "string"
          ? data.worksheet
          : JSON.stringify(data.worksheet, null, 2);
        break;

      case "powerPoint":
        const slides = Object.values(data)[0] || [];
        slides.forEach(slide => {
          const title = slide.title || "Untitled Section";
          resultElement.innerHTML += `<h6>${title}</h6>`;

          if (Array.isArray(slide.bullets)) {
            resultElement.innerHTML += `<ul>${slide.bullets.map(bullet => `<li>${bullet}</li>`).join('')
              }</ul>`;
          } else if (typeof slide.bullets === "string") {
            resultElement.innerHTML += `<p>${slide.bullets}</p>`;
          }
        });
        break;

      case "quizTest":
        resultElement.textContent = Array.isArray(data.data)
          ? data.data.join("\n")
          : data.data || "No quiz data available";
        break;

      default:
        const defaultResults = Object.values(data.data || {});
        resultElement.textContent = defaultResults.join("\n\n");
    }

    // Show download button
    document.getElementById("downloadBtn").style.display = "inline-block";
    hideLoader();

  } catch (error) {
    hideLoader();
    console.error("API Error:", error);
    showPopup(`Failed to submit: ${error.message}`);
  }
});

const downloadBtn = document.getElementById("downloadBtn");

if (!downloadBtn) {
  console.error("Download button not found! Check the ID in HTML.");
} else {
  downloadBtn.addEventListener("click", async function () {
    // Get selected material type (PowerPoint or Word Document)
    let selectedMaterialType = document.getElementById("mySelect").value;

    if (!selectedMaterialType) {
      // alert("Please select a material type.");
      showPopup("Please select a material type.");
      return;
    }

    materialType = selectedMaterialType;
    // Check if PowerPoint is selected
    if (selectedMaterialType === "powerPoint") {

      let payload = {
        topics: selected_topics,
        textbook_name: selectedBook.name,
        language: window.language,
        book_id: selectedBook.id,
        notes: document.getElementById("exampleFormControlTextarea1").value,
        selections: getSelectedChaptersWithSubchapters()
      };

      let apiUrl = "/generate-ppt/";
      try {
        // Call API to generate PowerPoint
        let response = await fetch(apiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        if (!response.ok) {
          throw new Error("Network response was not ok.");
        }

        // Create Blob for PowerPoint download
        const blob = await response.blob();
        const now = new Date();
        const MM = String(now.getMonth() + 1).padStart(2, "0");
        const DD = String(now.getDate()).padStart(2, "0");
        const YY = String(now.getFullYear()).slice(2);
        const HH = String(now.getHours()).padStart(2, "0");
        const mm = String(now.getMinutes()).padStart(2, "0");
        const timestamp = `${MM}${DD}${YY}${HH}${mm}`;
        const fileName = `${selectedBook.name}_${materialType}_${timestamp}.pptx`;
        // Trigger download of PowerPoint
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } catch (error) {
        console.error("PPT download error:", error);
        // alert("Failed to generate PowerPoint.");
        showPopup("Failed to generate PowerPoint.");
      }
    } else {
      // If Word Document is selected
      const summaryElement = document.getElementById("result");

      if (!summaryElement) {
        console.error("Result element not found!");
        // alert("No documents available!");
        showPopup("No documents available!");
        return;
      }

      const summaryText = summaryElement.innerText;

      if (!summaryText) {
        console.warn("Summary is empty.");
        // alert("Summary is empty! Generate content first.");
        showPopup("Summary is empty! Generate content first.");
        return;
      }
      if (typeof docx === "undefined") {
        console.error("docx library is not loaded! Check your script tag.");
        return;
      }
      const lines = summaryText.split("\n");

      let docChildren = [
        new docx.Paragraph({
          text: materialType.toUpperCase(),
          heading: docx.HeadingLevel.HEADING_1,
        }),
      ];

      lines.forEach((line) => {
        const trimmed = line.trim();

        if (trimmed === "") {
          // Preserve empty lines as spacing
          docChildren.push(new docx.Paragraph({ text: "" }));
        } else if (trimmed.startsWith("#### ")) {
          docChildren.push(
            new docx.Paragraph({
              text: trimmed.replace("#### ", ""),
              heading: docx.HeadingLevel.HEADING_3,
            })
          );
        } else if (trimmed.startsWith("### ")) {
          docChildren.push(
            new docx.Paragraph({
              text: trimmed.replace("### ", ""),
              heading: docx.HeadingLevel.HEADING_2,
            })
          );
        } else if (trimmed.startsWith("* ")) {
          docChildren.push(
            new docx.Paragraph({
              text: trimmed.replace("* ", ""),
              bullet: { level: 0 },
            })
          );
        } else {
          docChildren.push(new docx.Paragraph({ text: trimmed }));
        }
      });

      notebook_data = fetch();
      const doc = new docx.Document({
        sections: [
          {
            properties: {},
            headers: {},
            footers: {
              default: new docx.Footer({
                children: [
                  new docx.Table({
                    width: {
                      size: 100,
                      type: docx.WidthType.PERCENTAGE,
                    },
                    borders: {
                      top: {
                        style: BorderStyle.SINGLE,
                        size: 1,
                        color: "AAAAAA",
                      },
                      bottom: { style: BorderStyle.NONE },
                      left: { style: BorderStyle.NONE },
                      right: { style: BorderStyle.NONE },
                      insideHorizontal: { style: BorderStyle.NONE },
                      insideVertical: { style: BorderStyle.NONE },
                    },
                    rows: [
                      new docx.TableRow({
                        children: [
                          // LEFT Logo
                          new docx.TableCell({
                            width: { size: 15, type: WidthType.PERCENTAGE },

                            verticalAlign: docx.VerticalAlign.CENTER,
                            children: [
                              ...(await (async () => {
                                if (!notebookMeta.logo1)
                                  return [new docx.Paragraph("")];
                                try {
                                  const res = await fetch(
                                    // `/media/${notebookMeta.logo1}`
                                    `/media/folders/logos/logo.png`
                                  );
                                  if (!res.ok) throw new Error(res.statusText);
                                  const img = await res.arrayBuffer();
                                  return [
                                    new docx.Paragraph({
                                      alignment: docx.AlignmentType.LEFT,
                                      children: [
                                        new docx.ImageRun({
                                          data: img,
                                          transformation: {
                                            width: 40,
                                            height: 40,
                                          },
                                        }),
                                      ],
                                    }),
                                  ];
                                } catch (e) {
                                  console.error("Left logo error:", e);
                                  return [new docx.Paragraph("")];
                                }
                              })()),
                            ],
                          }),

                          // Merged CENTER + RIGHT Cell (combines both)
                          new docx.TableCell({
                            width: { size: 70, type: WidthType.PERCENTAGE },
                            verticalAlign: docx.VerticalAlign.CENTER,
                            children: [
                              new docx.Paragraph({
                                alignment: docx.AlignmentType.CENTER,
                                children: [
                                  new docx.TextRun({
                                    text: (notebookMeta.disclaimer || "")
                                      .split("Copyright")[0]
                                      .trim(),
                                    font: "Karla",
                                    size: 20,
                                    color: "999999",
                                  }),
                                  new docx.TextRun({
                                    text:
                                      "Copyright" +
                                      (notebookMeta.disclaimer.split(
                                        "Copyright"
                                      )[1] || " © …"),
                                    font: "Karla",
                                    size: 20,
                                    color: "999999",
                                    break: 1,
                                  }),
                                ],
                              }),
                            ],
                          }),

                          new docx.TableCell({
                            width: { size: 15, type: WidthType.PERCENTAGE },
                            verticalAlign: docx.VerticalAlign.CENTER,
                            margins: {
                              top: 100,
                              bottom: 100,
                              left: 100,
                              right: 100,
                            },
                            children: [
                              ...(await (async () => {
                                if (!notebookMeta.logo2)
                                  return [new docx.Paragraph("")];
                                try {
                                  const res = await fetch(
                                    `/media/${notebookMeta.logo2}`
                                  );
                                  if (!res.ok) throw new Error(res.statusText);
                                  const img = await res.arrayBuffer();
                                  return [
                                    new docx.Paragraph({
                                      alignment: docx.AlignmentType.RIGHT,
                                      children: [
                                        new docx.ImageRun({
                                          data: img,
                                          transformation: {
                                            width: 40,
                                            height: 40,
                                          },
                                        }),
                                      ],
                                    }),
                                  ];
                                } catch (e) {
                                  console.error("Right logo error:", e);
                                  return [new docx.Paragraph("")];
                                }
                              })()),
                            ],
                          }),
                        ],
                      }),
                    ],
                  }),
                ],
              }),
            },

            children: docChildren,
          },
        ],
        styles: {
          paragraphStyles: [
            {
              id: "footerText",
              name: "Footer Text",
              basedOn: "Normal",
              next: "Normal",
              run: {
                font: "Karla",
                size: 18,
                color: "999999",
              },
              paragraph: {
                spacing: { before: 120 },
              },
            },
          ],
        },
      });

      const now = new Date();
      const MM = String(now.getMonth() + 1).padStart(2, "0");
      const DD = String(now.getDate()).padStart(2, "0");
      const YY = String(now.getFullYear()).slice(2);
      const HH = String(now.getHours()).padStart(2, "0");
      const mm = String(now.getMinutes()).padStart(2, "0");
      const timestamp = `${MM}${DD}${YY}${HH}${mm}`;
      const fileName = `${selectedBook.name}_${materialType}${timestamp}.docx`;
      docx.Packer.toBlob(doc).then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      });
    }
  });
}

// ==================================================================================

function validateForm() {
  // 1. Check if material type is selected
  const materialTypeSelected = document.getElementById("mySelect");
  if (materialTypeSelected.value === "Make a selection") {
    // alert('Please select what you want to build (Material Type)');
    showPopup("Please select what you want to build (Material Type)");
    return false;
  }

  // 2. For Quiz/Test, check if at least one question type is selected
  if (
    materialTypeSelected.value === "quizTest" ||
    materialTypeSelected.value === "caseStudy" ||
    materialTypeSelected.value === "workSheet"
  ) {
    questionTypes = document.querySelectorAll(
      '#quesType input[type="checkbox"]:checked'
    );
    if (questionTypes.length === 0) {
      // alert('Please select at least one Question Type');
      showPopup("Please select at least one Question Type");
      return false;
    }

    // Check number of questions for quiz/test
    const questionCount = document.getElementById("questionCount").value;
    if (
      !questionCount ||
      isNaN(questionCount) ||
      questionCount < 1 ||
      questionCount > 50
    ) {
      // alert('Please enter a valid number of questions (1-50)');
      showPopup("Please enter a valid number of questions (1-50)");
      return false;
    }
  }

  // 3. Check if textbook is selected
  const textbookSelected = document.getElementById("mySelect2");
  if (
    !textbookSelected.value ||
    textbookSelected.value === "Make a Selection"
  ) {
    // alert('Please select a Textbook/Resource');
    showPopup("Please select a Textbook/Resource");
    return false;
  }

  // 4. Check if chapters are selected
  // const chapterCheckboxes = document.querySelectorAll('#js-list .chapter-select input[type="checkbox"]:checked');

  const chapterCheckboxes = document.querySelectorAll(
    ".topic-checkbox:checked"
  );

  console.log("chapter : ", chapterCheckboxes);
  if (chapterCheckboxes.length === 0) {
    // alert('Please select at least one Chapter');
    showPopup("Please select at least one Chapter");
    return false;
  }

  // 6. Check institution selection
  const institutionSelected = document.getElementById("mySelect5");
  if (
    !institutionSelected.value ||
    institutionSelected.value === "Make a Selection"
  ) {
    // alert('Please select your Institution');
    showPopup("Please select your Institution");
    return false;
  }

  // 7. Check email
  const emailInput = document.getElementById("exampleFormControlInput1");
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailInput.value || !emailRegex.test(emailInput.value)) {
    // alert('Please enter a valid email address');
    showPopup("Please enter a valid email address");
    return false;
  }

  return true; // All validations passed
}
