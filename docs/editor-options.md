# Editor Options Evaluation

This document compares two rich text editor approaches for the project: `django-ckeditor-5` and a simple Markdown textarea.

## django-ckeditor-5
- **Pros**
  - Provides a full-featured WYSIWYG editing experience powered by CKEditor 5.
  - Supports rich formatting such as headings, lists, and block quotes out of the box.
  - Produces HTML compatible with existing `content` fields.
- **Cons**
  - Adds a JavaScript bundle and additional static assets.
  - More complex configuration compared to a plain textarea.

## Simple Markdown
- **Pros**
  - Lightweight and minimal dependencies.
  - Content stored as Markdown which is easy to version and edit manually.
- **Cons**
  - Requires a renderer to convert Markdown to HTML on display.
  - Less intuitive for non-technical users who prefer a WYSIWYG interface.

## Recommendation
`django-ckeditor-5` offers a modern WYSIWYG editor with HTML output compatible with existing data, making migration straightforward while preserving authoring convenience. The open-source core meets our needs, so premium CKEditor add-ons remain optional.
