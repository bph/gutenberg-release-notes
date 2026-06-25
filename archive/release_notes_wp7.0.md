# WordPress Gutenberg Release Notes: v22.0.0 - v22.5.0

This release cycle brings significant improvements to the editing experience with major enhancements to block functionality, design tools, and interface usability. Here's what's new:

## 🎨 New Design System & Theming

**WordPress Theme Package**  
[#72305](https://github.com/WordPress/gutenberg/pull/72305), [#72782](https://github.com/WordPress/gutenberg/pull/72782), [#73155](https://github.com/WordPress/gutenberg/pull/73155), [#73004](https://github.com/WordPress/gutenberg/pull/73004)  
A new comprehensive theming system with improved color management, including caution color ramps and optimized contrast adjustments. This provides more consistent and accessible color choices across your site.

**Enhanced Design Tokens**  
[#74226](https://github.com/WordPress/gutenberg/pull/74226), [#74325](https://github.com/WordPress/gutenberg/pull/74325), [#74617](https://github.com/WordPress/gutenberg/pull/74617)  
Improved design consistency with consolidated border tokens and automatic design token linting to ensure visual coherence across the editor.

## 🧭 Breadcrumbs Block - Comprehensive Navigation

**Complete Breadcrumb System**  
[#72478](https://github.com/WordPress/gutenberg/pull/72478), [#72714](https://github.com/WordPress/gutenberg/pull/72714), [#72839](https://github.com/WordPress/gutenberg/pull/72839), [#72832](https://github.com/WordPress/gutenberg/pull/72832), [#73249](https://github.com/WordPress/gutenberg/pull/73249), [#73435](https://github.com/WordPress/gutenberg/pull/73435), [#72905](https://github.com/WordPress/gutenberg/pull/72905), [#73670](https://github.com/WordPress/gutenberg/pull/73670), [#73966](https://github.com/WordPress/gutenberg/pull/73966), [#73794](https://github.com/WordPress/gutenberg/pull/73794), [#74808](https://github.com/WordPress/gutenberg/pull/74808)  
The new Breadcrumbs block now supports virtually every page type: archives, 404 pages, search results, paginated content, comments pagination, attachments, and post type archives. It intelligently shows the current page context and includes alignment options for perfect placement in your design.

## 🖼️ Media & Image Enhancements

**Image Cropping Tool**  
[#72414](https://github.com/WordPress/gutenberg/pull/72414), [#73277](https://github.com/WordPress/gutenberg/pull/73277)  
A brand new image cropper package lets you crop images directly in the editor without needing external tools.

**Advanced Image Controls**  
[#73115](https://github.com/WordPress/gutenberg/pull/73115), [#74519](https://github.com/WordPress/gutenberg/pull/74519), [#74201](https://github.com/WordPress/gutenberg/pull/74201)  
Images now support focal point controls and aspect ratio adjustments for wide and full alignments, plus reorganized inspector controls with a dedicated content tab.

**Enhanced Media Management**  
[#74455](https://github.com/WordPress/gutenberg/pull/74455), [#74336](https://github.com/WordPress/gutenberg/pull/74336), [#74401](https://github.com/WordPress/gutenberg/pull/74401), [#74432](https://github.com/WordPress/gutenberg/pull/74432), [#74484](https://github.com/WordPress/gutenberg/pull/74484)  
Drag and drop functionality, expanded view, and new media fields for dates, thumbnails, authors, and attachments make media organization much more powerful.

## 📝 Block Content & Typography

**Universal Text Alignment**  
[#73111](https://github.com/WordPress/gutenberg/pull/73111), [#73732](https://github.com/WordPress/gutenberg/pull/73732), [#74068](https://github.com/WordPress/gutenberg/pull/74068), [#74269](https://github.com/WordPress/gutenberg/pull/74269), [#74383](https://github.com/WordPress/gutenberg/pull/74383), [#74599](https://github.com/WordPress/gutenberg/pull/74599), [#74720](https://github.com/WordPress/gutenberg/pull/74720), [#74760](https://github.com/WordPress/gutenberg/pull/74760), [#74945](https://github.com/WordPress/gutenberg/pull/74945), [#74724](https://github.com/WordPress/gutenberg/pull/74724), [#73201](https://github.com/WordPress/gutenberg/pull/73201), [#73854](https://github.com/WordPress/gutenberg/pull/73854)  
Nearly all text blocks now support the standardized text-align block support system, including Paragraph, Button, Comment blocks, Heading, and Verse. Plus, text justify alignment is now available.

**Custom CSS for Individual Blocks**  
[#73959](https://github.com/WordPress/gutenberg/pull/73959), [#74969](https://github.com/WordPress/gutenberg/pull/74969)  
Add custom CSS to individual block instances for precise styling control. The editor automatically adds a `has-custom-css` class for styling consistency.

**Block Content Fields**  
[#73863](https://github.com/WordPress/gutenberg/pull/73863), [#74486](https://github.com/WordPress/gutenberg/pull/74486)  
A new content tab in block inspectors uses DataForm to show relevant fields for all blocks, with block bindings support for dynamic content.

## 🧩 Enhanced Block Features

**Grid Block Responsiveness**  
[#73662](https://github.com/WordPress/gutenberg/pull/73662), [#73864](https://github.com/WordPress/gutenberg/pull/73864)  
Grid blocks are now responsive when columns are set, with simplified drag handles in auto mode.

**Cover Block Video Embeds**  
[#73023](https://github.com/WordPress/gutenberg/pull/73023), [#74600](https://github.com/WordPress/gutenberg/pull/74600)  
Cover blocks now support background videos from embeds and focal point picker for fixed backgrounds.

**HTML Block Enhancement**  
[#73108](https://github.com/WordPress/gutenberg/pull/73108)  
The HTML block now supports JavaScript and CSS editing for more powerful customizations.

**Math Block Improvements**  
[#72557](https://github.com/WordPress/gutenberg/pull/72557), [#73544](https://github.com/WordPress/gutenberg/pull/73544)  
LaTeX input now uses a monospaced font and style options are available for better mathematical expression editing.

**Query Loop Enhancements**  
[#73790](https://github.com/WordPress/gutenberg/pull/73790), [#74160](https://github.com/WordPress/gutenberg/pull/74160)  
Query loops now support excluding terms and intelligently hide design change options when blocks are locked.

**Comments & Social Features**  
[#72665](https://github.com/WordPress/gutenberg/pull/72665), [#67267](https://github.com/WordPress/gutenberg/pull/67267)  
Latest Comments block can display full comments, and Comments Pagination Numbers includes spacing controls for better layout control.

## 🎯 Navigation & Menu Improvements

**Navigation Overlays**  
[#74119](https://github.com/WordPress/gutenberg/pull/74119), [#74047](https://github.com/WordPress/gutenberg/pull/74047), [#74650](https://github.com/WordPress/gutenberg/pull/74650), [#74780](https://github.com/WordPress/gutenberg/pull/74780), [#74890](https://github.com/WordPress/gutenberg/pull/74890), [#74849](https://github.com/WordPress/gutenberg/pull/74849), [#74847](https://github.com/WordPress/gutenberg/pull/74847), [#74861](https://github.com/WordPress/gutenberg/pull/74861), [#74862](https://github.com/WordPress/gutenberg/pull/74862)  
Navigation blocks now support custom overlays with multiple built-in patterns including centered navigation, accent backgrounds, and black backgrounds. New blocks default to "always" show overlays.

**Enhanced Navigation Controls**  
[#74653](https://github.com/WordPress/gutenberg/pull/74653), [#74544](https://github.com/WordPress/gutenberg/pull/74544), [#74495](https://github.com/WordPress/gutenberg/pull/74495), [#74305](https://github.com/WordPress/gutenberg/pull/74305)  
Toggle submenus to stay always open, improved color handling for overlays, and better autocomplete prevention in navigation link searches.

**Page Creation in Navigation**  
[#72627](https://github.com/WordPress/gutenberg/pull/72627), [#73836](https://github.com/WordPress/gutenberg/pull/73836)  
Create pages directly from the Navigation block with helpful snackbar notices and improved parent page search using relevance matching.

## 📊 Data Views & Forms Revolution

**Advanced Data Form Layouts**  
[#72355](https://github.com/WordPress/gutenberg/pull/72355), [#72514](https://github.com/WordPress/gutenberg/pull/72514), [#72540](https://github.com/WordPress/gutenberg/pull/72540), [#74547](https://github.com/WordPress/gutenberg/pull/74547), [#74995](https://github.com/WordPress/gutenberg/pull/74995)  
DataForm now supports details, borderless card layouts, collapsible sections, and comprehensive validation with error display.

**Enhanced Form Controls**  
[#73156](https://github.com/WordPress/gutenberg/pull/73156), [#73465](https://github.com/WordPress/gutenberg/pull/73465), [#74891](https://github.com/WordPress/gutenberg/pull/74891), [#74704](https://github.com/WordPress/gutenberg/pull/74704)  
Pattern validation, min/max validation for inputs, new combobox control, and custom validation support.

**DataViews Interface Improvements**  
[#72780](https://github.com/WordPress/gutenberg/pull/72780), [#71050](https://github.com/WordPress/gutenberg/pull/71050), [#73491](https://github.com/WordPress/gutenberg/pull/73491), [#74161](https://github.com/WordPress/gutenberg/pull/74161)  
Activity layout, density picker, total items count in footer, and configurable group header labels.

## 🎨 Pattern & Template Editing

**Content-Only Pattern Editing**  
[#72988](https://github.com/WordPress/gutenberg/pull/72988), [#73375](https://github.com/WordPress/gutenberg/pull/73375), [#71982](https://github.com/WordPress/gutenberg/pull/71982), [#73425](https://github.com/WordPress/gutenberg/pull/73425)  
Patterns marked as content-only get special editing treatment with color panels and support for content block insertion.

**Section Block Improvements**  
[#73199](https://github.com/WordPress/gutenberg/pull/73199), [#73203](https://github.com/WordPress/gutenberg/pull/73203), [#73183](https://github.com/WordPress/gutenberg/pull/73183), [#73195](https://github.com/WordPress/gutenberg/pull/73195)  
Section blocks now use pattern icons and names in list view, remove confusing ungroup options, and have clearer editing button labels.

**Pattern Override Enhancements**  
[#73889](https://github.com/WordPress/gutenberg/pull/73889), [#73105](https://github.com/WordPress/gutenberg/pull/73105)  
Synced patterns now infer partial syncing support from the server and use clearer "Disconnect pattern" language instead of "Detach".

## 👁️ Block Visibility Controls

**Viewport-Based Visibility**  
[#74379](https://github.com/WordPress/gutenberg/pull/74379), [#74249](https://github.com/WordPress/gutenberg/pull/74249), [#74180](https://github.com/WordPress/gutenberg/pull/74180), [#74517](https://github.com/WordPress/gutenberg/pull/74517), [#74679](https://github.com/WordPress/gutenberg/pull/74679), [#74025](https://github.com/WordPress/gutenberg/pull/74025)  
Hide blocks based on screen size with a complete visibility system including modal controls, inspector notices, and smart rendering for different viewports.

## 🛠️ Interface & User Experience

**List View Enhancements**  
[#74120](https://github.com/WordPress/gutenberg/pull/74120), [#74164](https://github.com/WordPress/gutenberg/pull/74164), [#74163](https://github.com/WordPress/gutenberg/pull/74163), [#74794](https://github.com/WordPress/gutenberg/pull/74794), [#74574](https://github.com/WordPress/gutenberg/pull/74574), [#74798](https://github.com/WordPress/gutenberg/pull/74798)  
Buttons, List, and Social Icons blocks now have list view tabs, improved block cards with parent navigation, better button labels, and full block titles display.

**Component Improvements**  
[#73041](https://github.com/WordPress/gutenberg/pull/73041), [#74036](https://github.com/WordPress/gutenberg/pull/74036), [#74548](https://github.com/WordPress/gutenberg/pull/74548), [#74082](https://github.com/WordPress/gutenberg/pull/74082), [#73814](https://github.com/WordPress/gutenberg/pull/73814)  
Busy state for confirm dialogs, updated ToggleGroupControl design, smoother menu animations, improved popover animations, and shorter snackbar timeouts.

**Enhanced Editing Features**  
[#73737](https://github.com/WordPress/gutenberg/pull/73737), [#74339](https://github.com/WordPress/gutenberg/pull/74339), [#74251](https://github.com/WordPress/gutenberg/pull/74251)  
Editor back button scrolls to previous location, preview editing aligns with common breakpoints, and improved block variation transformation positioning.

## 🆕 New UI Components

**WordPress UI Package Components**  
[#74415](https://github.com/WordPress/gutenberg/pull/74415), [#74625](https://github.com/WordPress/gutenberg/pull/74625), [#74661](https://github.com/WordPress/gutenberg/pull/74661), [#74189](https://github.com/WordPress/gutenberg/pull/74189), [#73875](https://github.com/WordPress/gutenberg/pull/73875)  
New primitive components including Button, Tooltip, Select, VisuallyHidden, and Badge components for consistent interface development.

## 📝 Content Creation & Management

**Notes System**  
[#72868](https://github.com/WordPress/gutenberg/pull/72868), [#73136](https://github.com/WordPress/gutenberg/pull/73136), [#73645](https://github.com/WordPress/gutenberg/pull/73645), [#74577](https://github.com/WordPress/gutenberg/pull/74577), [#73609](https://github.com/WordPress/gutenberg/pull/73609)  
Collaborative notes with keyboard shortcuts, tree navigation, email notifications, floating notes in template lock mode, and notes count in the site editor.

**Form Field Enhancements**  
[#73996](https://github.com/WordPress/gutenberg/pull/73996), [#74297](https://github.com/WordPress/gutenberg/pull/74297), [#74595](https://github.com/WordPress/gutenberg/pull/74595)  
Form field blocks now use modern SVG icons instead of dashicons and include autocomplete prevention.

**Content Transformation**  
[#73068](https://github.com/WordPress/gutenberg/pull/73068), [#70771](https://github.com/WordPress/gutenberg/pull/70771), [#63654](https://github.com/WordPress/gutenberg/pull/63654)  
Transform between Verse and Quote blocks, improved Word Online heading support while pasting, and simplified shortcut entry for Separator and Code blocks.

This release represents a significant step forward in making WordPress editing more powerful, intuitive, and flexible for users of all skill levels. The improvements span from basic content creation to advanced design control, ensuring everyone benefits from these enhancements.