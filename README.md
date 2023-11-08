# LINK.BOOK
#### Video Demo:  <https://youtu.be/t7_ycUD0weI>
#### Description: This README will provide an overview of the project.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [License](#license)


## Introduction

LINK.BOOK is a Flask-based web application designed using (Flask, SQLite, HTMl and CSS) to help users organize and store educational links, such as videos and web pages, in a structured manner. It allows users to categorize links into books, chapters, titles, and descriptions, making it a valuable tool for anyone looking to streamline their learning process.

## Features

User Registration: Users can create accounts to save and manage their links.

Link Organization: Categorize links into books, chapters, titles, and descriptions for easy retrieval.

Search Functionality: Users can search for links by Book(category), Chapter(subject), and Title(title).

Responsive UI: A user-friendly web interface that works well on both desktop and mobile devices.

## Getting Startedr

Go to URL https: 'todo'

## Usage

1. Registration: Users must create an account to save and manage links.

2. Login: Log in using your registered credentials. Web page starts at the Login page.

3. HTML Page and Python Code Discription:
    - [Index Page](#index-page)
    - [Category Page](#category-page)
    - [Subject Page](#subject-page)
    - [Titles Page](#titles-page)
    - [Apology Page](#apology-page)
## Index Page

The "Index Page" is the main page of the LINK.BOOK application, where users can view and manage their saved links. This page displays a greeting message, provides an overview of the application, and allows users to access their saved content.

### Flask Route: `@app.route("/", methods=["GET", "POST"])`

- This route handles both GET and POST requests at the root URL ("/").
- It ensures that the user is logged in before accessing the page, adding a layer of security to the route.

### Python Function: `def index():`

- This function is responsible for rendering the "Index Page" and processing form submissions.

#### Greeting Message

- It retrieves the user's name and displays a greeting message in uppercase.

#### Form Handling

- It checks if the request method is POST and if a form parameter named "table_info" exists. If these conditions are met, it fetches table information from the database based on the user's ID and orders it by category in ascending order.
- If the request is a POST request, it renders the `index.html` template with the table information.

#### Rendering `index.html`

- If the request is not a POST request or if the "table_info" form parameter is not present, it renders the `index.html` template with the user's greeting message.

### HTML Template: `index.html`

- The `index.html` template extends a layout template, sets the title, and defines the main content block.

- It displays a greeting message, provides an explanation of the LINK.BOOK application's purpose, and encourages users to click to view their content.

- It also displays a table of contents (if `table_info` exists) in a tabular format, including Books, Chapters, Titles, Descriptions, and option to quick open the link

This page offers users a user-friendly interface for navigating their saved links and gaining insights into the LINK.BOOK application's capabilities.
 
## Category Page

The "Category Page" in the LINK.BOOK application allows users to view and manage their saved links categorized by books. Users can select a book category, view subjects within the category, and access individual link titles.

### HTML Template: `category.html`

- The `category.html` template extends a layout template, sets the title, and defines the main content block.

- It displays a menu on the left side with buttons to select book categories. Users can choose a category to view subjects, create new books, or edit and delete existing categories.

- The template also allows users to view a list of subjects within the selected book category and provides options to play link titles or edit and delete the book category.

- A form for creating a new link is included, where users can enter the URL link, select a category, specify a chapter, provide a title, and add a description.

- The template offers options to edit or delete book categories. Users can change the name of a category, and a warning is displayed about the implications of this action. Additionally, they can delete a category, along with its associated subjects and titles.

### Python Function: `catogrie_list()`

- The `catogrie_list` function in the Python code handles the logic for the "Category Page."

- It manages variables for subjects, subject lists, titles, form generation, and user details.

- The function retrieves subjects and titles when a user selects a book category or plays a link title.

- It handles form submissions for generating edit or delete forms, as well as changing category names and deleting categories.

- It also provides a form for creating new links with proper validation and ensures that the category, subject, and title are saved correctly.

- The function returns the rendered `category.html` template with relevant data.

This page allows users to efficiently manage and categorize their saved links, providing a well-structured approach to organizing their digital resources.


## Subject Page

The "Chapters Subjects Page" in the LINK.BOOK application allows users to view and manage their saved links organized by chapters. Users can select a chapter to view individual link titles within it.

### HTML Template: `subjects.html`

- The `subjects.html` template extends a layout template, sets the title, and defines the main content block.

- It displays a menu on the left side with buttons to select chapters. Users can choose a chapter to view titles, create new chapters, or edit and delete existing chapters.

- The template offers options to play link titles within the selected chapter.

- A form for creating a new chapter is included, where users can enter the chapter name. Users can also edit or delete existing chapters.

### Python Function: `subject_list()`

- The `subject_list` function in the Python code handles the logic for the "Chapters Subjects Page."

- It manages variables for chapters, chapter names, titles, form generation, and user details.

- The function retrieves titles when a user selects a chapter or plays a link title.

- It handles form submissions for generating edit or delete forms, as well as changing chapter names and deleting chapters.

- It also provides a form for creating new chapters and ensures that the chapter name is saved correctly.

- The function returns the rendered `subjects.html` template with relevant data.

This page enables users to effectively organize and access their saved links by chapters, providing a structured way to manage their digital resources.


## Titles Page

The "Titles Page" in the LINK.BOOK application allows users to view and manage their saved link titles. Users can select a title to view detailed information and perform various actions like editing, deleting, and opening links.

### HTML Template: `titles.html`

- The `titles.html` template extends a layout template, sets the title, and defines the main content block.

- It displays a menu on the left side with buttons to select titles. Users can choose a title to view its details, create new titles, or edit and delete existing titles.

- The template provides a form for creating a new title, where users can input the Title name, Book, Chapter, URL link, and Description.

- It allows users to view detailed information about a selected title, including  book (category), chapter (subject), title name, URL link, and description. Users can also open the link in a new tab.

- Users can edit or delete the selected title or update its description.

### Python Function: `title()`

- The `title()` function in the Python code handles the logic for the "Titles Page."

- It manages variables for title details, categories, chapters, links, descriptions, and title ID.

- The function retrieves detailed information when a user selects a title.

- It handles form submissions for generating edit or delete forms, changing title names, updating descriptions, and deleting titles.

- The function also provides a form for creating new titles and ensures that the title data is saved correctly.

- Users can return to the main page with a table of saved links by clicking the "Link.Book" button.

This page provides users with a comprehensive view of their saved link titles, allowing them to manage and access them conveniently.


## Apology Page

The "Apology Page" in the LINK.BOOK application is a simple page designed to display apologies or error messages to users. It is used to inform users when something goes wrong or when they encounter an issue.

### HTML Template: `apology.html`

- The `apology.html` template extends a layout template, sets the title to "Home," and defines the main content block.

- It displays a header with a message passed to it via a variable.

### Python Function: `apology()`

- The `apology()` function in the Python code handles the logic for displaying apology messages.

- It renders the `apology.html` template and allows developers to pass a custom message to it when called.

- This page is used to provide users with information in case of errors or exceptional conditions.

The "Apology Page" serves as a straightforward way to communicate issues or errors to users, making the application more user-friendly.

## License

This project is licensed under the MIT License.

