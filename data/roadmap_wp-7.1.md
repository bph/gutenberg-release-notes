# WP 7.1 Roadmap (parsed)

_Source: https://make.wordpress.org/core/2026/06/19/roadmap-to-7-1/_

## AI generation streaming support
WordPress is adding the ability for AI features to stream their responses in real-time, so instead of waiting for the entire AI-generated text to appear at once, you'll see it written word-by-word as it's created—similar to ChatGPT's typing effect. This first arrives in the PHP AI Client as groundwork for fuller integration in a future release. For users, it makes AI tools feel faster and more responsive, letting you start reading or editing generated content before the AI has finished its full response.

## AI embeddings for content search
Embeddings let WordPress represent your content as numerical vectors so AI can understand the meaning behind posts, pages, and other content—not just match keywords. This enables 'semantic search' where you can find content based on what it means rather than exact words, making search across your site smarter and more intuitive. The feature lays the foundation for future AI-powered discovery tools that understand context and intent.

## Username and password authentication for Connectors — tracking #78647
The Connectors framework, introduced in 7.0, currently lets plugins register connections to external services using API keys. This update adds username and application-password authentication as an alternative, giving site owners more flexible ways to authenticate with third-party services. Eventually, the plan includes richer connection forms in PHP with fields like URLs and dropdowns, making it easier to set up integrations without writing code.

## Guidelines for AI and humans — tracking #75171
Guidelines is a new feature that lets you write down your site's editorial rules, brand voice, and content standards in a structured way that both humans and AI tools can follow. You can define what tone to use, what topics to cover, and how content should be formatted, then import and export these guidelines between sites. As more collaboration happens in WordPress—especially with AI assistance—Guidelines help maintain consistency and ensure your preferences are respected no matter who (or what) is writing.

## Organized command palette with history
The command palette now organizes its results into sections: recently used commands, suggested actions, and matching results. Your recently used commands are saved to your user preferences and persist across sessions, so the tools you reach for most often are always easy to find. The visual design has also been refreshed to make the list easier to scan and understand at a glance.

## Admin color scheme in Site Editor
The Site Editor sidebar and overall interface now respect the WordPress admin color scheme you've chosen in your profile settings, instead of always using a dark background. If you've personalized your admin area with a specific color scheme—like Ocean or Sunrise—that choice now extends into the Site Editor for a consistent look and feel everywhere you work.

## DataViews and DataForms improvements — tracking #76045
DataViews (the modern interface for lists of posts, pages, and patterns) is being updated to use the new Design System components for a more polished, consistent look. Quick Edit is being consolidated with the editor inspector so editing a post's details—like title, author, or publish date—feels the same whether you do it from the list view or the editor sidebar. A new server-side REST endpoint also lets plugin authors register custom views and forms for their own post types or data.

## Dedicated Identity section in Site Editor
A new Design → Identity screen brings your site's core identity settings—logo, favicon, site title, and tagline—into one place in the Site Editor. You can edit your logo and favicon inline with a built-in media editor, and quickly update your site title and tagline without hunting through templates or the Settings menu. It's designed to make foundational site setup simple and discoverable.

## Design System theming and components — tracking #76941
WordPress is building a shared component library and theming system that ensures buttons, menus, and other interface elements look and behave consistently throughout the editor. This cycle graduates ThemeProvider from experimental to a stable API, finalizes naming for design tokens like background, foreground, and stroke, and adds tokens for corner radius and element sizing. Key editor menus—transforms, style variations, and block options—are being migrated to these improved components for a more polished experience.

## On This Day dashboard widget
A new dashboard widget called 'On This Day' surfaces posts and content you published on this date in past years—a nostalgic feature popularized by many social platforms. It's designed to motivate you by reminding you of what you've written before and inspire you to create more content today that will appear as a memory in the future.

## Persistent admin bar in editors (omnibar) — tracking #79036
The familiar WordPress admin bar—with your site name, profile, and quick links—now stays visible inside the Block Editor and Site Editor, rather than disappearing when you enter the editing canvas. The design has been refreshed: the 'Howdy' greeting is removed, the site icon replaces the home icon, the profile avatar is now circular, and old Dashicons icons are replaced with modern SVGs. This keeps navigation consistent and accessible no matter where you are in WordPress.

## Visual revisions improvements — tracking #79120
Visual revisions, introduced in 7.0, are getting easier to read and navigate. Planned improvements include a sparkline view in the revision toolbar that visualizes the density of changes over time, persistent URLs so you can share a link to a specific revision with a colleague, and other polish to make the revision history more useful and navigable.

## Abilities API expansion
The Abilities API gives developers and AI tools a structured way to ask 'what can this WordPress site do?' This cycle advances the API with better querying and filtering, and implements a core set of abilities like managing site settings, retrieving current user info, and general site awareness. For users, this means AI and plugin features can adapt to what your site is capable of, providing smarter, context-aware assistance.

## Block Bindings for list items and inner blocks — tracking #77199
Block Bindings, which connect blocks to dynamic data sources like custom fields or API endpoints, now support binding list-item blocks and inner blocks within a parent. This expands what you can do with dynamic content: for example, you can bind each item in a list to a repeating field, or bind nested blocks inside a Group to different data sources, all without writing code.

## Enforced iframe editor for block themes
The post editor is transitioning to always run inside an iframe, which isolates the editing canvas from the admin's styles and makes viewport units and media queries work correctly. In 7.1, iframe mode will be enforced for block-based themes (classic themes will follow in a future release). Blocks using the older Block API version 2 or lower will need to be updated to version 3. For users, this means a more accurate preview of how content will look on the front end, without interference from admin styles.

## Extended Unicode support for email addresses
WordPress is expanding support for Unicode characters in email addresses, so people around the world can use email addresses with non-ASCII characters (like accented letters or non-Latin scripts) that better reflect their language. Behind the scenes, functions like is_email() and sanitize_email() are being updated to handle these addresses correctly, making WordPress more inclusive for its global audience.

## React 19 upgrade — tracking #71336
WordPress is upgrading from React 18 to React 19, the JavaScript library that powers the block editor. This brings new APIs, improved TypeScript types, and behavior changes. The upgrade will first land in the Gutenberg plugin as an opt-in experiment (turn on 'React 19' in the experiments page) so plugin and theme developers can test their code and report issues before it merges into Core. For users, the upgrade enables future editor improvements and keeps WordPress on a modern, supported foundation.

## Icon API expansion and icon set refresh — tracking #75715
The Icon API, introduced in 7.0, is opening up to third parties. Plugin and theme developers can now register their own icon sets with functions like register_icon() and unregister_icon(), similar to how the Font Library works for typography. The API includes SVG sanitization, namespace validation, and a reusable icon picker modal that any block can use. Core icons in blocks like Navigation, Breadcrumbs, and Details become selectable through the API. WordPress's core icon set is also getting a visual refresh with prominent icons redrawn as stroke-based designs for a cleaner, more modern look.

## Classic block deprecation — tracking #78067
As a first step toward making the Classic block and TinyMCE editor opt-in, the Classic block will be hidden from the block inserter in 7.1—you won't see it when adding new blocks. Existing Classic blocks in old posts continue to work, and migration and conversion paths are being improved. The goal is to lighten the editor for sites that don't rely on the classic editing experience, making WordPress faster and more focused on the modern block editor.

## Playlist block with waveform visualization — tracking #77421
A new Playlist block lets you add a collection of audio files to a post or page, with an optional waveform visualization that shows the audio's shape as it plays. It's a richer, more visual way to present podcasts, music, or audio content directly in WordPress without needing a third-party embed or plugin.

## Table of Contents block — tracking #42229
The Table of Contents block automatically scans your post or page for headings and generates a list of navigable links at the top. Visitors can click a heading in the table of contents to jump straight to that section, making long-form content easier to navigate and improving accessibility and user experience.

## Tabs block — tracking #73230
The Tabs block lets you organize content into separate tabbed panels that visitors can click through. Instead of showing everything at once, you can split information into logical sections—like 'Overview,' 'Features,' and 'Pricing'—and let users choose what they want to read. It's a cleaner, more compact way to present related content without overwhelming the page.

## Gallery lightbox refinements — tracking #56587
The Gallery block's lightbox feature, which displays images in a full-screen overlay when clicked, is getting refinements including swipe indicators on mobile to show visitors they can swipe between images, and opt-in captions so image descriptions appear in the lightbox view. These improvements make galleries more intuitive and accessible on touch devices.

## Editable blocks inside HTML block
The HTML block now supports having editable blocks nested inside custom HTML code. This is especially useful when AI generates sites with custom HTML layouts—you can keep the custom structure while still editing individual blocks normally. It bridges the gap between code-based and visual editing.

## Mark as decorative toggle for images
The Image block now has a 'Mark as decorative' toggle that hides purely decorative images from screen readers. When turned on, assistive technology will skip the image, preventing unnecessary clutter for people using screen readers and improving the accessibility of your content by focusing attention on meaningful images.

## Embed shortcode transform
If you paste or convert an old [embed] shortcode, WordPress now automatically transforms it into a proper Embed block instead of leaving raw shortcode text on the page. This makes migrating content from older WordPress versions smoother and ensures embeds from YouTube, Twitter, and other services display correctly in the block editor.

## Shortcode block auto-transforms
When you paste a shortcode into the Shortcode block, WordPress now detects if that shortcode has a corresponding block and offers to transform it automatically. This makes it easier to convert legacy shortcodes—like galleries or contact forms—into their modern block equivalents with one click.

## Background gradients for Group block
The Group block now supports background gradients alongside background images, thanks to a new background.gradient block support. You can layer a gradient over an image without conflicts, opening up richer design possibilities. While currently limited to the Group block, other blocks can adopt this support via a filter, and it will expand to more Core blocks over time.

## Writing flow and drag-and-drop improvements — tracking #63255
A dedicated effort is underway to smooth out everyday friction in the writing experience. This includes improvements to drag-and-drop (making it easier to rearrange blocks by dragging them), better multi-selection on touch devices so you can select and move multiple blocks on a tablet, and other small fixes that make writing and arranging content feel more intuitive and responsive.

## Enhanced Notes features — tracking #76316
Notes—the collaboration tool for leaving feedback on content—is getting a major upgrade. You'll be able to leave notes on specific text within a block or across multiple blocks, use rich text formatting in your notes, get notifications when someone replies or follows a thread, react with emojis, and apply suggestions directly to the content. There's also a 'minified' view to keep notes compact when you're focused on editing. All of this makes asynchronous collaboration richer and more interactive.

## Real-time collaboration progress — tracking #76377
Real-time collaboration—the vision of multiple people (and AI) editing the same post simultaneously without post locks—continues forward, but with big strategic decisions still open: whether to ship the full feature or just the underlying architecture in 7.1, and which storage mechanism to use. A dedicated outreach effort is underway to test collaborative editing with real users. If it lands, you'll see live updates as others type, no more locked-out editing screens, and a fundamentally more collaborative WordPress.

## Display inherited styles in sidebar — tracking #77595
When styling a block, it's not always obvious which styles come from your theme, from Global Styles, or from a parent block. This work explores showing inherited styles clearly in the block sidebar, so you can see where each style originates and decide whether to override it locally or edit the global or theme-level style. It helps you style with confidence and understand the cascade of design decisions.

## Interactive states styling (hover, focus, active) — tracking #38277
You can now style how blocks respond to user interaction—like buttons changing color on hover, links underlining on focus, or elements shifting on active click—directly in the Site Editor and block settings, without writing any CSS. Support for pseudo-states like :hover, :focus, and :active is available for both Global Styles (applying to all instances of a block) and individual block instances. Future work will add custom states like styling the current menu item.

## Pattern editing iterations — tracking #75717
In 7.0, the pattern editing experience shifted to focus on content changes rather than exposing every block tool, making patterns feel more like editing a single cohesive unit. This cycle focuses on refining that experience based on user feedback: UX improvements, bug fixes, and general maintenance to make working with patterns smoother and more predictable.

## Responsive styling for blocks — tracking #77817
Responsive styling lets you define how a block looks at different screen sizes—for example, a larger font size on desktop and a smaller one on mobile—directly in the editor without writing custom CSS or media queries. You can apply responsive styles both globally (to all instances of a block) and to individual block instances. This makes responsive design a built-in, first-class part of the editing experience, so your site looks great on every device.

## Viewport breakpoint customization — tracking #75707
After adding the ability to hide or show blocks at different screen sizes, WordPress is now letting themes define custom breakpoints in theme.json—the specific screen widths where responsive styles kick in. This gives theme developers and site builders more control over responsive behavior, ensuring breakpoints match a theme's design rather than relying on one-size-fits-all defaults.

## Client-side media processing improvements — tracking #76756
Media processing is moving to the browser to support more formats and add resilience. This includes HEIC image support (iPhone photos), Ultra HDR support for high-quality images, automatic GIF-to-video conversion for smaller file sizes, uploads that retry on failure and resume after a crash or going offline, video transcoding to web-safe formats, and local poster (thumbnail) generation for videos so pages render before the video fully loads. All of this happens in your browser, making uploads faster and more reliable.

## Media editor modal with freeform cropping — tracking #73771
A new Media editor modal replaces the inline cropping tool in the Block Editor. You still click the familiar Crop button, but now you get a dedicated modal with freeform cropping (not locked to preset aspect ratios), flip and rotation controls with fine-grained and snap options, and the ability to edit image metadata all in one place. It gives you more control to get your images just right before inserting them.

## Media gallery improvements — tracking #77117
Galleries are getting smarter and easier to build. Improvements include better handling when converting the legacy [gallery] shortcode to a Gallery block, dynamic galleries that can automatically pull or sort media attached to the current post, and a quicker path in the block inserter to add images attached to the post with thumbnails shown directly. These changes make building image galleries faster and more intuitive.

## Speculative loading performance update
WordPress's speculative loading feature—which prefetches and prerenders pages to make navigation feel instant—is getting smarter. When both object caching and page caching are detected on a site, the default eagerness will shift from 'conservative' to 'moderate,' prefetching and prerendering more readily. For users on well-equipped sites, this means faster navigation as pages load in the background before you click.

## View Transitions plugin iteration
The View Transitions feature plugin brings smooth, animated transitions between pages on the front end of your site—think fade-ins, slide-outs, or other cinematic effects when navigating. The plugin is in active development and available to install today. Contributors are welcome to help move it toward eventual inclusion in Core.

## Enhanced Responsive Images plugin iteration
The Enhanced Responsive Images plugin automatically calculates more accurate 'sizes' attribute values for images in block themes, so browsers download appropriately sized images for each device—saving bandwidth and improving load times. The plugin is available now and being actively developed, with the goal of eventually merging into Core.
