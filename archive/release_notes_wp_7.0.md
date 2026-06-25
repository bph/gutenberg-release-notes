# WordPress Gutenberg Plugin: Release Notes for v22.0.0 - v22.6.0

## Major New Features & Packages

### Real-Time Collaboration
WordPress now supports real-time collaborative editing, allowing multiple users to work on the same content simultaneously. You'll see other editors' cursors and changes as they type, making team content creation seamless and efficient. [#75398](https://github.com/WordPress/gutenberg/pull/75398), [#75286](https://github.com/WordPress/gutenberg/pull/75286), [#74564](https://github.com/WordPress/gutenberg/pull/74564)

### Block Custom CSS Support
Individual blocks can now have custom CSS applied directly to them, giving you precise control over styling without affecting your entire site. The editor automatically adds a `has-custom-css` class to blocks with custom styles. [#73959](https://github.com/WordPress/gutenberg/pull/73959), [#74969](https://github.com/WordPress/gutenberg/pull/74969), [#75052](https://github.com/WordPress/gutenberg/pull/75052)

### New Theme Package & Design System
A new theme system provides consistent colors, spacing, and typography across WordPress. This includes updated design tokens, improved contrast handling, and a new caution color palette for better accessibility. [#72305](https://github.com/WordPress/gutenberg/pull/72305), [#72782](https://github.com/WordPress/gutenberg/pull/72782), [#75054](https://github.com/WordPress/gutenberg/pull/75054)

### Image Cropping & Editing
Built-in image cropping tools let you resize and adjust images directly in the editor without external software. The new MediaEdit component supports drag-and-drop functionality and expanded editing views. [#72414](https://github.com/WordPress/gutenberg/pull/72414), [#73277](https://github.com/WordPress/gutenberg/pull/73277), [#74455](https://github.com/WordPress/gutenberg/pull/74455)

## Navigation & Site Building

### Navigation Overlays
Create custom mobile menu overlays for your navigation with pre-built patterns like centered navigation, accent backgrounds, and black overlays. The system includes a sidebar preview and automatic pattern insertion for new overlays. [#74971](https://github.com/WordPress/gutenberg/pull/74971), [#74780](https://github.com/WordPress/gutenberg/pull/74780), [#74862](https://github.com/WordPress/gutenberg/pull/74862), [#75564](https://github.com/WordPress/gutenberg/pull/75564)

### Enhanced Navigation Links
Navigation links now show preview information in the inspector, making it easier to understand where links point. You can create new pages directly from the navigation editor with improved help text and pre-populated titles from your search text. [#75399](https://github.com/WordPress/gutenberg/pull/75399), [#75154](https://github.com/WordPress/gutenberg/pull/75154), [#75349](https://github.com/WordPress/gutenberg/pull/75349)

### Breadcrumbs Block Improvements
The Breadcrumbs block now supports archives, search results, paginated content, attachments, and 404 pages. You can control alignment and choose whether to show the last breadcrumb item. [#72478](https://github.com/WordPress/gutenberg/pull/72478), [#72714](https://github.com/WordPress/gutenberg/pull/72714), [#73794](https://github.com/WordPress/gutenberg/pull/73794), [#74808](https://github.com/WordPress/gutenberg/pull/74808)

## Block Editor Experience

### Pattern Editing (Stabilized)
Content-only pattern editing is now stable, allowing you to edit reusable patterns without affecting their structure. The editor shows pattern names in the document toolbar and provides dedicated editing controls for synced patterns. [#74843](https://github.com/WordPress/gutenberg/pull/74843), [#73208](https://github.com/WordPress/gutenberg/pull/73208), [#75602](https://github.com/WordPress/gutenberg/pull/75602)

### Block Visibility Controls
Hide blocks on specific screen sizes (desktop, tablet, mobile) with new viewport-based visibility controls. Hidden blocks show helpful indicators in the editor and list view, making responsive design more intuitive. [#74379](https://github.com/WordPress/gutenberg/pull/74379), [#74839](https://github.com/WordPress/gutenberg/pull/74839), [#75404](https://github.com/WordPress/gutenberg/pull/75404)

### Improved List View
List view now shows actual block content instead of generic names, making navigation easier. Blocks like Button, List Item, and others display their text content, and you can see full block titles for better organization. [#74163](https://github.com/WordPress/gutenberg/pull/74163), [#74794](https://github.com/WordPress/gutenberg/pull/74794), [#74798](https://github.com/WordPress/gutenberg/pull/74798)

### Enhanced Toolbar & Inspector
Block toolbars now show custom block names, and the inspector includes new Content tabs with field-based editing for supported blocks. Pattern controls appear in popovers for cleaner interfaces. [#73690](https://github.com/WordPress/gutenberg/pull/73690), [#73863](https://github.com/WordPress/gutenberg/pull/73863), [#75194](https://github.com/WordPress/gutenberg/pull/75194)

## Individual Block Improvements

### Typography & Text Blocks
- **Text Alignment**: Paragraph, Button, Heading, and many other blocks now support text alignment through standardized block supports [#73111](https://github.com/WordPress/gutenberg/pull/73111), [#73732](https://github.com/WordPress/gutenberg/pull/73732), [#74383](https://github.com/WordPress/gutenberg/pull/74383)
- **Text Columns**: Paragraph and Post Excerpt blocks support multi-column text layouts [#74656](https://github.com/WordPress/gutenberg/pull/74656), [#75587](https://github.com/WordPress/gutenberg/pull/75587)
- **Verse to Poetry**: The Verse block has been renamed to Poetry for clarity [#74121](https://github.com/WordPress/gutenberg/pull/74121)
- **Text Indentation**: New line indent support with configurable settings [#74889](https://github.com/WordPress/gutenberg/pull/74889)

### Media Blocks
- **Gallery Lightbox**: View gallery images in an overlay lightbox for better user experience [#62906](https://github.com/WordPress/gutenberg/pull/62906)
- **Image Enhancements**: Focal point controls, aspect ratio support for wide/full alignment, and automatic protocol handling for URLs [#73115](https://github.com/WordPress/gutenberg/pull/73115), [#74519](https://github.com/WordPress/gutenberg/pull/74519), [#75135](https://github.com/WordPress/gutenberg/pull/75135)
- **Cover Block**: Support for embedded background videos and focal point picker for fixed backgrounds [#73023](https://github.com/WordPress/gutenberg/pull/73023), [#74600](https://github.com/WordPress/gutenberg/pull/74600)

### Layout Blocks
- **Tabs Block (Stabilized)**: Full tab functionality with color support, simplified editing, and improved icons [#75424](https://github.com/WordPress/gutenberg/pull/75424), [#75482](https://github.com/WordPress/gutenberg/pull/75482), [#75416](https://github.com/WordPress/gutenberg/pull/75416)
- **Grid Improvements**: Responsive column settings and cleaner drag handles in stable mode [#73662](https://github.com/WordPress/gutenberg/pull/73662), [#73864](https://github.com/WordPress/gutenberg/pull/73864)
- **Accordion Block**: Enhanced list view support and better icon integration [#75271](https://github.com/WordPress/gutenberg/pull/75271), [#75380](https://github.com/WordPress/gutenberg/pull/75380)

### Form & Interactive Blocks
- **HTML Block**: Now supports JavaScript and CSS editing for advanced users [#73108](https://github.com/WordPress/gutenberg/pull/73108)
- **Math Block**: Monospaced font for LaTeX input and new style options [#72557](https://github.com/WordPress/gutenberg/pull/72557), [#73544](https://github.com/WordPress/gutenberg/pull/73544)
- **Form Blocks**: Updated with SVG icons replacing dashicons and improved field controls [#73996](https://github.com/WordPress/gutenberg/pull/73996), [#74297](https://github.com/WordPress/gutenberg/pull/74297)

## DataViews & Site Management

### Enhanced Data Management
New DataViews system provides better data visualization with table, list, and grid layouts. Features include density controls, grouping options, validation support, and improved field rendering. [#71050](https://github.com/WordPress/gutenberg/pull/71050), [#73156](https://github.com/WordPress/gutenberg/pull/73156), [#74161](https://github.com/WordPress/gutenberg/pull/74161)

### Page Management Improvements
The Pages interface now includes quick edit modals, notes counting, unified view persistence, and sticky footer controls for better content management workflows. [#75173](https://github.com/WordPress/gutenberg/pull/75173), [#73609](https://github.com/WordPress/gutenberg/pull/73609), [#75297](https://github.com/WordPress/gutenberg/pull/75297)

### Media Library Enhancements
Updated media modal with DataViews, new field types (date added, date modified, attached to), thumbnail fallbacks, and automatic file selection after upload. [#74401](https://github.com/WordPress/gutenberg/pull/74401), [#75597](https://github.com/WordPress/gutenberg/pull/75597), [#74024](https://github.com/WordPress/gutenberg/pull/74024)

## User Interface & Components

### Design System Updates
- **Consistent Spacing**: 24px padding system and updated menu item heights (32px) for better consistency [#73334](https://github.com/WordPress/gutenberg/pull/73334), [#73429](https://github.com/WordPress/gutenberg/pull/73429)
- **Typography**: Font weight changes from 500 to 499 and updated tab styling [#72473](https://github.com/WordPress/gutenberg/pull/72473), [#72455](https://github.com/WordPress/gutenberg/pull/72455)
- **Mobile Improvements**: Icon-only buttons retained on mobile with better primary action handling [#72761](https://github.com/WordPress/gutenberg/pull/72761), [#72597](https://github.com/WordPress/gutenberg/pull/72597)

### New UI Components
A new `@wordpress/ui` package introduces modern components like Button, Dialog, Select, Tabs, Tooltip, and IconButton with improved styling and functionality. [#74415](https://github.com/WordPress/gutenberg/pull/74415), [#75183](https://github.com/WordPress/gutenberg/pull/75183), [#74661](https://github.com/WordPress/gutenberg/pull/74661)

### Enhanced Controls
- **Color Picker**: Support for pasting complete color values [#73166](https://github.com/WordPress/gutenberg/pull/73166)
- **Toggle Groups**: Visual emphasis for selected items [#75138](https://github.com/WordPress/gutenberg/pull/75138)
- **Notices**: Enhanced with action support and better spacing [#74094](https://github.com/WordPress/gutenberg/pull/74094), [#73905](https://github.com/WordPress/gutenberg/pull/73905)

## Developer & Technical Improvements

### Block Support System
New dimension supports for width and height, anchor support for dynamic blocks, and improved serialization controls give developers more flexibility in block creation. [#71905](https://github.com/WordPress/gutenberg/pull/71905), [#71914](https://github.com/WordPress/gutenberg/pull/71914), [#74183](https://github.com/WordPress/gutenberg/pull/74183)

### Performance & Architecture
- **PHP-Only Block Registration**: Stabilized for server-side rendering [#75543](https://github.com/WordPress/gutenberg/pull/75543)
- **Queue System**: Enhanced for better performance [#74501](https://github.com/WordPress/gutenberg/pull/74501)
- **WebAssembly Support**: Detection and fallbacks for advanced features [#74827](https://github.com/WordPress/gutenberg/pull/74827)

### Development Tools
- **Design Token Linting**: Automatic validation for consistent design system usage [#74226](https://github.com/WordPress/gutenberg/pull/74226), [#74325](https://github.com/WordPress/gutenberg/pull/74325)
- **wp-env Improvements**: New cleanup commands, status reporting, and testing environment options [#75045](https://github.com/WordPress/gutenberg/pull/75045), [#75341](https://github.com/WordPress/gutenberg/pull/75341)

These updates represent significant improvements to WordPress's block editor, making it more powerful, accessible, and user-friendly while maintaining the flexibility developers need to create custom solutions.