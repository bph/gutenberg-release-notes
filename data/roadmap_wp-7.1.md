# WP 7.1 Roadmap (parsed)

_Source: https://make.wordpress.org/core/2026/06/19/roadmap-to-7-1/_

## AI Client generation streaming
Generation streaming introduced in the PHP AI Client as an initial effort to unlock full usage in a future release.

## AI Client embeddings support
Embeddings represent content as vectors to enable meaning-based search across a site.

## Connectors authentication expansion — tracking #78647
Connectors gain more ways to authenticate beyond API keys, starting with username/application password support.

## Guidelines feature — tracking #75171
A new Guidelines feature lets you define writing and content guidelines that tie into AI tooling, with the ability to import/export guidelines between sites.

## Command palette organization improvements
The command palette now groups results into clear sections for recent, suggested, and matching commands.

## Admin color scheme in Site Editor
The Site Editor sidebar and overall shell now follow the set WordPress admin color scheme instead of always using a fixed dark background.

## DataViews and DataForms iterations — tracking #76045
Work is underway to migrate DataViews onto the new Design System primitives and consolidate Quick Edit with the editor inspector.

## Dedicated Identity section
A dedicated Design → Identity screen brings the essentials of your site's identity into one place, with an inline media editor for your logo and favicon.

## Design System ThemeProvider graduation — tracking #76941
A highlight of this cycle is graduating ThemeProvider from experimental to a stable, public API, alongside finalizing the public token names.

## On This Day dashboard widget
The dashboard is getting a new "On This Day" widget that resurfaces past content, a popular feature across many different platforms.

## Persistent admin bar (omnibar) — tracking #79036
The admin bar is getting some nice polish ahead of being easily accessible in the Site Editor and Block Editor.

## Revisions improvements — tracking #79120
Planned improvements include a spark line view in the scrubbing toolbar to better visualize the history of changes, persistent URLs to allow sharing a link to a particular revision, and more.

## Abilities API iteration
This cycle advances querying and filtering of abilities and implements a curated set of core abilities (including site settings, current-user info management, and general site awareness).

## Block Bindings for list items — tracking #77199
Block Bindings expands with new support for binding list-item blocks and inner blocks, letting more of your content connect to dynamic data sources.

## Enforced iframed editor
The current plan is to enforce iframing for block-based themes in this release, then extend it to all themes in a future release.

## Extended Unicode support
This release is looking to broaden Unicode support so email addresses, usernames, and slugs better reflect WordPress' global audience.

## React 19 Upgrade — tracking #71336
WordPress is upgrading from React 18 to React 19.

## Icon API expansion — tracking #75715
7.1's iteration centers on opening the API up to third parties with new public functions like register_icon() and unregister_icon(), core-icons theme support, SVG sanitization and namespace validation.

## Classic block deprecation — tracking #78067
The Classic block is planned for deprecation in 7.1, and will no longer appear in the block inserter.

## Playlist block — tracking #77421
Playlist block, with additional waveform audio visualization.

## Table of Contents block — tracking #42229
Table of Contents block, automatically generating navigable links to the headings in your content.

## Tabs block — tracking #73230
Tabs block, organizes content into tabbed panels.

## Gallery block lightbox refinements — tracking #56587
Gallery block lightbox refinements, including swipe indication and opt-in captions on mobile.

## HTML block new block support
New block support for the HTML block, making it possible to have editable blocks inside of a custom HTML block.

## Image block decorative toggle
"Mark as decorative" toggle for the Image block to hide decorative images from screen readers for an improved experience.

## Embed shortcode transform
An [embed] shortcode transform was added to the Embed block, so converting or pasting [embed] shortcodes now creates a proper Embed block.

## Shortcode block transforms
Block specific transforms were added to the Shortcode block when text matches a registered shortcode.

## Group block background gradients
The Group block added support for background gradients through a new background.gradient block support, allowing gradients and background images to work together without conflicts.

## Dialog block — tracking #61297
Dialog block for transcripts and conversations.

## Marquee block — tracking #41730
Marquee block for scrolling, animated content.

## Writing flow improvements — tracking #63255
A dedicated focus is on chipping away at everyday pain points in the writing experience, from improving drag and drop to ensuring multi-selection works on touch devices.

## Notes features expansion — tracking #76316
Notes have a range of planned improvements that include notes on specific content within a block and across multiple blocks, rich text in notes, notifications for replies and follows, emoji reactions, a minified notes experience, and an "apply suggestions" feature.

## Real-time collaboration — tracking #76377
Real-time collaboration marches ahead with big, open strategy questions around what to land in this release and what storage mechanism to use.

## Display inherited styles — tracking #77595
This work explores surfacing inherited styles clearly in the sidebar so you can understand where a block's styles are coming from and edit at the right layer of styling.

## Interactive states styling — tracking #38277
Support for pseudo-state styling such as hover, focus, and active has landed for both Global Styles and individual block instances.

## Pattern editing iterations — tracking #75717
For this cycle, work will focus on UX improvements based on feedback around this change, bug fixes, and general maintenance.

## Responsive styling — tracking #77817
This work lets you define how a block looks at different screen sizes, applying responsive styles directly in the editor without writing custom CSS.

## Viewport breakpoint customization — tracking #75707
Theme-configurable breakpoints defined in theme.json are being added to provide more flexible, customizable responsive styling.

## Client-side media iterations — tracking #76756
The work spans HEIC image support, Ultra HDR support, GIF-to-video conversion, more resilient uploads that retry on failure and resume after a crash or going offline, video transcoding to web-safe formats.

## Media editor modal — tracking #73771
The Media editor modal replaces the existing inline cropping tool in the Block Editor, bringing freeform and aspect-ratio cropping, flip, fine-grained and snap rotation, and metadata editing into one dedicated workflow.

## Media gallery improvements — tracking #77117
Galleries are becoming more dynamic and easier to build, with better handling of the legacy gallery shortcode on conversion, dynamic galleries that can sort or pull media attached to a post.

## Speculative loading update
When both object caching and page caching are detected, the default eagerness would move from conservative to moderate, prefetching and prerendering more readily.

## View Transitions plugin
Work centers around bringing smooth, animated transitions between pages on the front end.

## Enhanced Responsive Images plugin
Work computes more accurate sizes values in block themes so browsers download appropriately sized images.
