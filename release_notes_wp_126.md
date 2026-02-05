# Gutenberg Plugin Enhancements: Versions 22.3.0 - 22.5.0

## Major New Features

### 🖼️ Image Cropping Tools
A complete image cropping system has been introduced to help you edit images directly in WordPress. The new image cropper package provides basic functionality ([#72414](https://github.com/WordPress/gutenberg/pull/72414)) and is now integrated into the editor ([#73277](https://github.com/WordPress/gutenberg/pull/73277)). You can now crop, adjust, and perfect your images without leaving WordPress or needing external image editing software.

### 📱 Block Visibility Controls
You can now show or hide blocks based on screen size, giving you precise control over responsive design. This includes:
- Viewport-based visibility rules ([#74379](https://github.com/WordPress/gutenberg/pull/74379), [#74025](https://github.com/WordPress/gutenberg/pull/74025))
- Visual controls and modal interface ([#74249](https://github.com/WordPress/gutenberg/pull/74249))
- Clear visibility notices in the block inspector ([#74180](https://github.com/WordPress/gutenberg/pull/74180))
- Full stabilization of the feature ([#74839](https://github.com/WordPress/gutenberg/pull/74839))

This means you can create truly responsive designs where certain content appears only on mobile, desktop, or tablet devices.

### 🎨 Custom CSS for Individual Blocks
Every block now supports custom CSS, allowing advanced users to add personalized styling to specific block instances ([#73959](https://github.com/WordPress/gutenberg/pull/73959)). The system automatically adds appropriate class names ([#74969](https://github.com/WordPress/gutenberg/pull/74969)) so your custom styles work correctly on both the front-end and in the editor.

### ✏️ Stabilized Pattern Editing
Pattern editing has been fully stabilized and the experimental flag removed ([#74843](https://github.com/WordPress/gutenberg/pull/74843)). This powerful feature allows you to create reusable design patterns and content blocks that can be used across your site while maintaining the ability to customize individual instances.

## Navigation Improvements

### Mobile Menu Overlays
Navigation blocks now include comprehensive overlay support for mobile menus:
- Multiple pre-built overlay patterns including centered navigation ([#74861](https://github.com/WordPress/gutenberg/pull/74861)), accent backgrounds ([#74849](https://github.com/WordPress/gutenberg/pull/74849)), and black backgrounds ([#74847](https://github.com/WordPress/gutenberg/pull/74847))
- Default overlay patterns are automatically inserted ([#74650](https://github.com/WordPress/gutenberg/pull/74650))
- New navigation blocks default to "always show" overlays ([#74890](https://github.com/WordPress/gutenberg/pull/74890))
- Sidebar preview for overlay patterns ([#74780](https://github.com/WordPress/gutenberg/pull/74780))
- Improved overlay control labels ([#74690](https://github.com/WordPress/gutenberg/pull/74690))

### Enhanced Navigation Features
- Option to keep submenus always open ([#74653](https://github.com/WordPress/gutenberg/pull/74653))
- Better handling of deleted navigation overlays ([#74766](https://github.com/WordPress/gutenberg/pull/74766))
- Improved color handling for custom overlays ([#74544](https://github.com/WordPress/gutenberg/pull/74544))
- Link picker component for easier navigation link management ([#73830](https://github.com/WordPress/gutenberg/pull/73830))

## Text Alignment Standardization

A major effort to standardize text alignment across blocks has resulted in consistent text-align support for:
- Button blocks ([#73732](https://github.com/WordPress/gutenberg/pull/73732))
- Comment Author Name ([#74068](https://github.com/WordPress/gutenberg/pull/74068))
- Comment Content ([#74269](https://github.com/WordPress/gutenberg/pull/74269))
- Comment Date ([#74599](https://github.com/WordPress/gutenberg/pull/74599))
- Comment Edit Link ([#74720](https://github.com/WordPress/gutenberg/pull/74720))
- Comment Reply Link ([#74760](https://github.com/WordPress/gutenberg/pull/74760))
- Comments Title ([#74945](https://github.com/WordPress/gutenberg/pull/74945))
- Heading blocks ([#74383](https://github.com/WordPress/gutenberg/pull/74383))
- Verse blocks ([#74724](https://github.com/WordPress/gutenberg/pull/74724))

This means you'll have consistent text alignment options across all these blocks, making it easier to create cohesive designs.

## Enhanced Block Features

### Image Block Improvements
- Focal point controls for better image positioning ([#73115](https://github.com/WordPress/gutenberg/pull/73115))
- Focal point picker support for fixed backgrounds in Cover blocks ([#74600](https://github.com/WordPress/gutenberg/pull/74600))
- Aspect ratio controls now available for wide and full alignment ([#74519](https://github.com/WordPress/gutenberg/pull/74519))
- Reorganized Content tab and inspector controls ([#74201](https://github.com/WordPress/gutenberg/pull/74201))

### Grid and Layout Enhancements
- Grid blocks are now responsive when columns are set ([#73662](https://github.com/WordPress/gutenberg/pull/73662))
- Simplified grid editing with removed drag handles in stable mode ([#73864](https://github.com/WordPress/gutenberg/pull/73864))
- New flex layout wrap option ([#74493](https://github.com/WordPress/gutenberg/pull/74493))
- Height block support added to dimensions ([#71914](https://github.com/WordPress/gutenberg/pull/71914))

### Form and Query Improvements
- Query Loop blocks now support excluding specific terms ([#73790](https://github.com/WordPress/gutenberg/pull/73790))
- Form blocks switched from Dashicons to SVG icons for better performance ([#73996](https://github.com/WordPress/gutenberg/pull/73996), [#74297](https://github.com/WordPress/gutenberg/pull/74297))
- Enhanced form field validation with min/max support ([#73465](https://github.com/WordPress/gutenberg/pull/73465))

## List View and Navigation Improvements

### Better Block Identification
- Custom block names now appear in breadcrumbs ([#73690](https://github.com/WordPress/gutenberg/pull/73690))
- List Item blocks show actual content instead of generic "block name" ([#74794](https://github.com/WordPress/gutenberg/pull/74794))
- Button blocks display improved labels in List View ([#74163](https://github.com/WordPress/gutenberg/pull/74163))
- Full block titles are now shown in List View ([#74798](https://github.com/WordPress/gutenberg/pull/74798))

### Enhanced List View Access
List View tabs have been added to several block types ([#74120](https://github.com/WordPress/gutenberg/pull/74120), [#74574](https://github.com/WordPress/gutenberg/pull/74574)):
- Button blocks
- List blocks  
- Social Icons blocks
- Pattern editing

## Performance and Technical Improvements

### Component System Overhaul
A new UI component system has been introduced with modern primitives:
- Field primitives ([#74190](https://github.com/WordPress/gutenberg/pull/74190))
- VisuallyHidden component ([#74189](https://github.com/WordPress/gutenberg/pull/74189))
- Button component ([#74415](https://github.com/WordPress/gutenberg/pull/74415))
- Fieldset primitives ([#74296](https://github.com/WordPress/gutenberg/pull/74296))
- Icon component ([#74311](https://github.com/WordPress/gutenberg/pull/74311))
- Input primitives ([#74615](https://github.com/WordPress/gutenberg/pull/74615), [#74313](https://github.com/WordPress/gutenberg/pull/74313))
- Select primitive ([#74661](https://github.com/WordPress/gutenberg/pull/74661))
- Badge component ([#73875](https://github.com/WordPress/gutenberg/pull/73875))
- Tooltip component ([#74625](https://github.com/WordPress/gutenberg/pull/74625))

### Editor Performance
- Memoized canOverrideBlocks for better performance ([#74400](https://github.com/WordPress/gutenberg/pull/74400))
- HtmlRenderer component reduces extra div wrappers in multiple blocks ([#74255](https://github.com/WordPress/gutenberg/pull/74255), [#74273](https://github.com/WordPress/gutenberg/pull/74273), [#74271](https://github.com/WordPress/gutenberg/pull/74271))
- Improved cross-origin isolation support ([#74418](https://github.com/WordPress/gutenberg/pull/74418))
- Enhanced offline error handling ([#73874](https://github.com/WordPress/gutenberg/pull/73874))

## Data Management and User Experience

### Enhanced Data Views
- Density picker with related styles ([#71050](https://github.com/WordPress/gutenberg/pull/71050))
- Group header label visibility controls ([#74161](https://github.com/WordPress/gutenberg/pull/74161))
- DateTime formatting implementation ([#73924](https://github.com/WordPress/gutenberg/pull/73924))
- Total items count in footer ([#73491](https://github.com/WordPress/gutenberg/pull/73491))
- Improved field colorization in list layout ([#73884](https://github.com/WordPress/gutenberg/pull/73884))

### Media Management
- Drag and drop functionality in MediaEdit ([#74455](https://github.com/WordPress/gutenberg/pull/74455))
- Expanded media view ([#74336](https://github.com/WordPress/gutenberg/pull/74336))
- Additional media fields including dates, authors, and attachments ([#74401](https://github.com/WordPress/gutenberg/pull/74401), [#74484](https://github.com/WordPress/gutenberg/pull/74484), [#74432](https://github.com/WordPress/gutenberg/pull/74432))
- Improved thumbnail fallbacks ([#74024](https://github.com/WordPress/gutenberg/pull/74024))

## Collaborative Features

### Real-time Collaboration
Initial support for real-time collaboration has been introduced:
- HTTP polling sync provider ([#74564](https://github.com/WordPress/gutenberg/pull/74564))
- Collection syncing ([#74665](https://github.com/WordPress/gutenberg/pull/74665))
- Relative positions in undo stack ([#74878](https://github.com/WordPress/gutenberg/pull/74878))

### Revision System
Basic in-editor revisions functionality has been added ([#74771](https://github.com/WordPress/gutenberg/pull/74771)), laying the groundwork for better content version management directly in the editor.

## Quality of Life Improvements

### Better Visual Design
- Updated ToggleGroupControl design ([#74036](https://github.com/WordPress/gutenberg/pull/74036))
- Improved popover animations ([#74082](https://github.com/WordPress/gutenberg/pull/74082))
- Enhanced notice component with better spacing ([#73905](https://github.com/WordPress/gutenberg/pull/73905))
- Consistent 32px tall menu items ([#73429](https://github.com/WordPress/gutenberg/pull/73429))

### Enhanced User Interactions
- Autocomplete prevention in appropriate form fields ([#74595](https://github.com/WordPress/gutenberg/pull/74595), [#74305](https://github.com/WordPress/gutenberg/pull/74305))
- Improved keyboard shortcuts for Separator and Code blocks ([#63654](https://github.com/WordPress/gutenberg/pull/63654))
- Better block transformation positioning ([#74251](https://github.com/WordPress/gutenberg/pull/74251))
- Pattern name display in document toolbar when editing ([#73208](https://github.com/WordPress/gutenberg/pull/73208))

These enhancements represent a significant step forward in WordPress block editing, with improvements touching every aspect of the editing experience from basic text formatting to advanced layout controls and collaborative features.