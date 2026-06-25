# WordPress Gutenberg Plugin: Release Notes v22.0-22.3

## Major New Features

### Image Cropping Tool
New built-in image cropper lets you crop images directly in the editor without needing external tools. Perfect for adjusting featured images, gallery photos, or any image block to get the exact framing you want. [#72414](https://github.com/WordPress/gutenberg/pull/72414), [#73277](https://github.com/WordPress/gutenberg/pull/73277)

### Enhanced HTML Block with CSS/JS Support
The HTML block now supports adding custom CSS and JavaScript, making it easier for developers to embed custom code snippets and styling directly into posts and pages. [#73108](https://github.com/WordPress/gutenberg/pull/73108)

### New Theme Package & Color System
Added a comprehensive theme package with improved color management, including a new caution color ramp and optimized contrast adjustments for better accessibility. [#72305](https://github.com/WordPress/gutenberg/pull/72305), [#72782](https://github.com/WordPress/gutenberg/pull/72782), [#73155](https://github.com/WordPress/gutenberg/pull/73155)

## Block Improvements

### Breadcrumbs Block - Now Feature Complete
The Breadcrumbs block received major enhancements to handle virtually any page type:
- Archive pages, 404 pages, and search results [#72714](https://github.com/WordPress/gutenberg/pull/72714)
- Attachment pages and paginated content [#73249](https://github.com/WordPress/gutenberg/pull/73249), [#72905](https://github.com/WordPress/gutenberg/pull/72905)
- Post type archives and comment pagination [#73435](https://github.com/WordPress/gutenberg/pull/73435), [#73670](https://github.com/WordPress/gutenberg/pull/73670)
- Home page handling with customizable display options [#72839](https://github.com/WordPress/gutenberg/pull/72839)
- Alignment support for better layout control [#73794](https://github.com/WordPress/gutenberg/pull/73794)

### Cover Block Video Embeds
You can now use video embeds (like YouTube or Vimeo) as background videos in Cover blocks, expanding your design options beyond uploaded video files. [#73023](https://github.com/WordPress/gutenberg/pull/73023)

### Math Block Improvements
- Monospaced font for LaTeX input makes writing mathematical expressions clearer [#72557](https://github.com/WordPress/gutenberg/pull/72557)
- Added style options for better visual customization [#73544](https://github.com/WordPress/gutenberg/pull/73544)

### Enhanced Button Block
Added support for pseudo-elements in theme.json, allowing theme developers to create more sophisticated button styling effects. [#71418](https://github.com/WordPress/gutenberg/pull/71418)

### Text Alignment Improvements
- Paragraph and Button blocks now use the standardized text-align block support system [#73111](https://github.com/WordPress/gutenberg/pull/73111), [#73732](https://github.com/WordPress/gutenberg/pull/73732)
- Added text justify alignment option across supported blocks [#73201](https://github.com/WordPress/gutenberg/pull/73201)
- New width block support under dimensions for better layout control [#71905](https://github.com/WordPress/gutenberg/pull/71905)

### Categories & Comments Enhancements
- Categories block now includes proper taxonomy CSS classes for better theme styling [#72662](https://github.com/WordPress/gutenberg/pull/72662)
- Latest Comments block can now display full comment text instead of just excerpts [#72665](https://github.com/WordPress/gutenberg/pull/72665)
- Comments Pagination Numbers block gained spacing controls [#67267](https://github.com/WordPress/gutenberg/pull/67267)

## Editor Experience Improvements

### Grid Block Responsiveness
Grid blocks now automatically adapt to different screen sizes when columns are set, making your layouts mobile-friendly by default. The interface was also simplified by removing unnecessary drag handles in stable mode. [#73662](https://github.com/WordPress/gutenberg/pull/73662), [#73864](https://github.com/WordPress/gutenberg/pull/73864)

### Pattern Editing Enhancements
- Improved language throughout: "Detach" is now "Disconnect pattern" for clarity [#73105](https://github.com/WordPress/gutenberg/pull/73105)
- Pattern sections now show the actual pattern icon and name instead of generic labels [#73203](https://github.com/WordPress/gutenberg/pull/73203)
- Better editing flow with "Edit section" replacing confusing "Ungroup" options [#73199](https://github.com/WordPress/gutenberg/pull/73199)
- Pattern name displays in document toolbar when editing in spotlight mode [#73208](https://github.com/WordPress/gutenberg/pull/73208)

### Navigation & Table Improvements
- Navigation block now shows helpful notifications when creating new pages [#72627](https://github.com/WordPress/gutenberg/pull/72627)
- Table editing got easier with right-click context menus and insert column options [#73104](https://github.com/WordPress/gutenberg/pull/73104), [#72929](https://github.com/WordPress/gutenberg/pull/72929)

### Enhanced Media Selection
The media modal now uses an improved DataViewsPicker interface with table view options, making it easier to browse and select images and other media files. [#71944](https://github.com/WordPress/gutenberg/pull/71944), [#72914](https://github.com/WordPress/gutenberg/pull/72914)

## Interface & Usability Updates

### Mobile Optimization
- Better mobile experience with optimized button layouts [#72761](https://github.com/WordPress/gutenberg/pull/72761), [#72597](https://github.com/WordPress/gutenberg/pull/72597)
- Menu items now use consistent 32px height for better touch interaction [#73429](https://github.com/WordPress/gutenberg/pull/73429)

### Visual Polish
- Consistent font weight adjustments (499 instead of 500) for better text rendering [#72473](https://github.com/WordPress/gutenberg/pull/72473)
- Updated sidebar icons and improved spacing throughout [#72772](https://github.com/WordPress/gutenberg/pull/72772)
- Social media updates: Twitter references updated to "X" with new iconography [#73110](https://github.com/WordPress/gutenberg/pull/73110)
- New cart icon added to the icon library [#73509](https://github.com/WordPress/gutenberg/pull/73509)

### Form & Component Enhancements
- Color picker now supports pasting complete color values [#73166](https://github.com/WordPress/gutenberg/pull/73166)
- Textarea controls have improved minimum height for better usability [#72867](https://github.com/WordPress/gutenberg/pull/72867)
- ComboboxControl only shows reset button when there's actually a value to reset [#72595](https://github.com/WordPress/gutenberg/pull/72595)
- Shorter timeout duration for notification messages [#73814](https://github.com/WordPress/gutenberg/pull/73814)

## Site Editor & Data Management

### Notes System
A new collaborative notes system was introduced with:
- Email notifications for team collaboration [#73645](https://github.com/WordPress/gutenberg/pull/73645)
- Keyboard navigation support [#73136](https://github.com/WordPress/gutenberg/pull/73136)
- Form submission shortcuts for faster note creation [#72868](https://github.com/WordPress/gutenberg/pull/72868)
- Notes count field in the Pages interface [#73609](https://github.com/WordPress/gutenberg/pull/73609)

### DataViews & Forms Evolution
- New activity layout for better data visualization [#72780](https://github.com/WordPress/gutenberg/pull/72780)
- Enhanced DataForm with details layout, pattern validation, and min/max input validation [#72355](https://github.com/WordPress/gutenberg/pull/72355), [#73156](https://github.com/WordPress/gutenberg/pull/73156), [#73465](https://github.com/WordPress/gutenberg/pull/73465)
- Improved card layouts with borderless options and better spacing [#72514](https://github.com/WordPress/gutenberg/pull/72514), [#72511](https://github.com/WordPress/gutenberg/pull/72511)

### Better Error Handling
Improved offline error notices help users understand connectivity issues and know when their changes might not be saved. [#73874](https://github.com/WordPress/gutenberg/pull/73874)

---

These updates represent a significant step forward in WordPress block editing, focusing on user experience, mobile responsiveness, and powerful new creative tools. Whether you're a content creator, designer, or developer, these enhancements make building beautiful, functional websites easier and more intuitive.