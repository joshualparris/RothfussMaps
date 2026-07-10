# Website Audit Improvements for University Atlas

## 1. Mobile Responsiveness
Implement responsive design to ensure the atlas works well on mobile devices and tablets. The current fixed-width sidebar (320px) may cause issues on smaller screens. Use media queries to stack the layout vertically on mobile.

**Implementation:** Added media queries in `styles.css` to change grid layout on screens <=768px and <=480px. Sidebar becomes full width and stacks above main panel on mobile.

## 2. Accessibility Enhancements
- Add alt text to all images in the image stage and thumbnails.
- Improve ARIA labels and roles for better screen reader support.
- Ensure keyboard navigation works for all interactive elements, including image navigation buttons and mode switches.
- Add focus indicators for keyboard users.

**Implementation:** 
- Alt text already present in `app.js` for images (e.g., `img.alt = \`${selection.title} - ${current.name}\``).
- Added `role="main"` to main panel in `index.html`.
- Added focus styles in `styles.css` for buttons and inputs (outline: 2px solid #b08a46).
- Keyboard navigation for image arrows already implemented in `app.js`.

## 3. Performance Optimization
- Implement lazy loading for images to improve initial load times.
- Compress and optimize image files (JPEG/WebP formats).
- Minify CSS and JavaScript files.
- Consider code splitting if the JS bundle grows.

**Implementation:** Added `loading="lazy"` to all img elements in `app.js` (main image, thumbnails, reader images).

## 4. Image Zoom Functionality
Add zoom controls or click-to-zoom for map images to allow users to see details more clearly, especially on high-resolution displays.

**Implementation:** 
- Added zoom button (🔍) in `index.html` viewer actions.
- Added zoom state and event listener in `app.js`.
- Added `.zoomed` class in `styles.css` to allow larger image display with hover scale.

## 5. Loading States and Error Handling
- Add loading spinners or skeletons while content loads.
- Implement error boundaries for failed image loads or data fetching.
- Provide user-friendly error messages when content cannot be displayed.

**Implementation:** In `app.js` renderSelection, show "Loading image..." text before img loads, and "Failed to load image" on error. Added CSS for .loading and .error classes in `styles.css`.

## 6. Search Functionality Enhancement
The search input exists but may need improvements:
- Add autocomplete suggestions.
- Highlight search results in the navigation.
- Support advanced search filters (by district, type, etc.).

**Implementation:** Search functionality is already implemented in `app.js` with case-insensitive search across titles, blurbs, notes, etc. No additional enhancements added beyond existing.

## 7. Print Styles
Add CSS print styles to make the maps printable, hiding UI elements and optimizing layout for paper.

**Implementation:** Added `@media print` in `styles.css` to hide sidebar, actions, thumbnails, and adjust layout for printing.

## 8. Dark Mode Toggle
Implement a dark mode option for users who prefer it, especially for long reading sessions.

**Implementation:** 
- Added dark mode button (🌙/☀️) in `index.html` sidebar.
- Added darkMode state and toggle event in `app.js`.
- Added dark mode CSS variables in `styles.css` and body.dark-mode class.

## 9. SEO and Meta Tags
If deploying online, add proper meta descriptions, Open Graph tags for social sharing, and structured data for search engines.

**Implementation:** Added meta description, keywords, and Open Graph tags in `index.html` head.

## 10. User Documentation
Create a help section or README explaining how to use the atlas, including navigation tips, search features, and archive mode.

**Implementation:** 
- Added help button (?) in `index.html` sidebar.
- Added help section with instructions in `index.html` main panel.
- Added toggle event in `app.js` to show/hide help.
- Added CSS for .help-section in `styles.css`.

## Additional Improvements Implemented

### Coverage / Backlog Dashboard
**Implementation:** Added coverage summary in sidebar showing Rendered, Prompts, and Awaiting counts. Updated `build_atlas.py` to scan `ai-prompts/` and calculate stats. Added `updateCoverageStats()` in `app.js`.

### Surface Awaiting Areas Properly
**Implementation:** Modified `build_atlas.py` to create "prompt-only" items for prompts without images. Added "awaiting" badge and "Open Prompt" button in study cards. Added `.prompt-only` CSS class.

### Split Active Canon from Legacy Drift
**Implementation:** Items with `kind: "legacy"` in `ITEM_META` get `status: "legacy"`. Badge shows "legacy" in UI.

### Prompt-to-Render Trace
**Implementation:** Added `sourcePrompt`, `sourceBrief`, `dependsOn`, `canonRisk` fields to items in `build_atlas.py`. Displayed in study details panel in `app.js`.

### Normalise Naming and Paths
**Implementation:** Enhanced `slugify()` and `clean_name()` functions in `build_atlas.py` to handle underscores and apostrophes consistently.

### Relationship Navigation
**Implementation:** Added "Open Prompt" button for prompt-only items. Can be extended for related studies.

### Render Quality / Canon Audit Layer
**Implementation:** Added status badges (rendered, awaiting, legacy) and caution pills for canon drift warnings.