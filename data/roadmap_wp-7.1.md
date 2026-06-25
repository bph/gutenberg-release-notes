# WP 7.1 Roadmap (parsed)

_Source: https://make.wordpress.org/core/2026/06/19/roadmap-to-7-1/_

## AI generation streaming
Generation streaming allows AI responses to appear word-by-word in real-time as they're generated, rather than all at once after a delay. This lands first in the PHP AI Client and makes AI feel more responsive and interactive, giving you immediate feedback instead of waiting for a complete response. For editors using AI assistance to draft or refine content, this means a faster, more natural workflow that feels like collaborating with another person.

## AI embeddings support
Embeddings convert your content into numerical vectors that capture meaning, enabling powerful semantic search across your entire site. Instead of matching exact keywords, visitors can search by concept—asking "how to improve engagement" would find relevant posts even if they use different words. For site owners with large content libraries, this makes finding related articles much easier and more intuitive.

## Connectors authentication improvements — tracking #78647
The Connectors framework, which manages connections to external services like AI providers, is gaining support for username and application password authentication beyond simple API keys. New declarative connection forms will let you configure URLs, select default models from dropdowns, and manage credentials more flexibly. This makes it easier for site owners to securely connect WordPress to third-party services without needing custom code.

## Guidelines for editorial rules — tracking #75171
Guidelines is a new feature that lets you define writing and content rules—your brand voice, style preferences, and editorial standards—directly in WordPress. These guidelines can be imported and exported between sites and are designed to guide both human editors and AI tools, ensuring consistency when collaborating. As more content work happens inside WordPress, Guidelines help you maintain your unique voice and standards across all contributors.

## Organized command palette
The command palette (the quick-access menu you open with keyboard shortcuts) now groups results into recent, suggested, and matching sections, and remembers your recently-used commands across sessions. The visual design has also been refreshed to make scanning results easier. This helps you navigate WordPress faster by surfacing the tools you use most often right at the top.

## Admin color schemes in Site Editor
The Site Editor's sidebar and interface now respect your chosen WordPress admin color scheme instead of always showing a dark background. This brings visual consistency across the post editor, Site Editor, and admin dashboard. If you've personalized WordPress with a color scheme you prefer, that choice now carries through everywhere you work.

## DataViews and DataForms improvements — tracking #76045
DataViews (the modern list interface for posts, pages, and templates) is moving to the new Design System for a more consistent look, and Quick Edit is being unified with the editor inspector so editing post details feels identical no matter where you do it. A new server-side REST endpoint also lets plugin developers add their own custom views and forms. For editors, this means a smoother, more predictable experience managing content and settings.

## Dedicated Identity section
A new Design → Identity screen consolidates your site's logo, favicon, title, and tagline into one easy-to-find location, with inline editing so you can crop and adjust images right there. This eliminates hunting through Settings or digging into templates just to update foundational branding. For new site builders especially, it makes setting up your site's identity quick and straightforward.

## Design System and ThemeProvider stabilization — tracking #76941
The shared component library (@wordpress/ui) continues evolving, with ThemeProvider graduating from experimental to stable and public token names being finalized (background, foreground, stroke). New customization tokens for corner radius and element sizing are added, and editor menus (transforms, style variations, block options) adopt the improved components. For users, this means a more polished, consistent interface throughout WordPress with smoother interactions.

## On This Day dashboard widget
The dashboard gains a new "On This Day" widget that surfaces past content you published on the same date in previous years, similar to memory features on social platforms. It's designed to motivate you by reminding you of what you've accomplished and encouraging you to write more. For content creators, it's a pleasant nudge to reflect on your archive and stay engaged with your site.

## Persistent admin bar (omnibar) — tracking #79036
The admin bar, which normally sits at the top of your site's front end, is now accessible inside the Site Editor and Block Editor. The design has been refreshed: the "Howdy" greeting is removed, your site icon replaces the home icon, the profile avatar becomes circular, and old Dashicons are replaced with modern SVG icons. This keeps familiar navigation with you wherever you're working, reducing the need to jump back to the dashboard.

## Visual revisions improvements — tracking #79120
Building on the visual revisions introduced in 7.0, this release adds a sparkline visualization in the scrubbing toolbar to show the history of changes at a glance, and persistent URLs so you can share a link to a specific revision with collaborators. These refinements make it easier to understand what changed when and navigate between versions, improving collaboration and content review workflows.

## Abilities API expansion
The Abilities API provides a structured way for developers and AI tools to query what your WordPress site can do—what settings exist, what the current user can manage, and general site capabilities. This cycle advances querying and filtering and implements a curated set of core abilities. For users, this mostly works behind the scenes but enables smarter AI assistance and better integration with external tools that need to understand your site's capabilities.

## Block Bindings for list-items and inner blocks — tracking #77199
Block Bindings, which connect blocks to dynamic data sources, now supports binding list-item blocks and inner blocks within containers. This means more of your content can be dynamically populated—for example, a list of team members pulled from custom fields or an external database. For site builders creating data-driven sites, this expands what you can accomplish without custom code.

## Enforced iframed editor
The post editor runs inside an iframe, which isolates your content from admin styles and makes viewport units and media queries work correctly against the editing canvas rather than the browser window. In 7.1, iframing becomes enforced for block-based themes (with classic themes following in a future release). For editors, this ensures the canvas behaves predictably and blocks render accurately, though plugin developers need to update older blocks to Block API version 3.

## Extended Unicode support
WordPress is broadening support for Unicode in email addresses, usernames, and slugs so they can include non-ASCII characters, better reflecting WordPress's global audience. Core functions like is_email(), sanitize_email(), and antispambot() are being updated to handle international characters. For users whose names or emails use non-Latin scripts, this removes frustrating barriers and makes WordPress more inclusive and accessible worldwide.

## React 19 upgrade — tracking #71336
WordPress is upgrading from React 18 to React 19, bringing new APIs, updated TypeScript types, and changed behaviors. This will first land in the Gutenberg plugin as an opt-in experiment for testing before merging to Core. For users, this is largely invisible but ensures WordPress stays modern and performant. Plugin and theme developers should test early to ensure compatibility.

## Icon API expansion and icon refresh — tracking #75715
The SVG Icon API, introduced in 7.0, is opening to third parties with functions like register_icon() and unregister_icon(), collection support (similar to the Font Library), and a reusable icon picker modal. Core blocks like Navigation, Breadcrumbs, and Details will let you choose icons, and the Icon block gains flip and rotate controls. The core icon set is also being visually refreshed with stroke-based designs. For editors and designers, this means far more flexibility to customize icons across your site without plugins.

## Classic block deprecation — tracking #78067
As a first step toward making the Classic block and TinyMCE editor opt-in, the Classic block will no longer appear in the block inserter by default in 7.1. Existing Classic blocks will continue to work, and migration and conversion paths are being improved. For most users, this means a lighter, faster editor; sites that still need the Classic block can opt back in.

## Playlist block — tracking #77421
The new Playlist block lets you create audio playlists with waveform visualization, making it easy to showcase multiple tracks or podcast episodes in a single interactive player. Visitors can browse and play through your audio content without leaving the page. For podcasters, musicians, and audio content creators, this provides a rich, modern listening experience built right into WordPress.

## Table of Contents block — tracking #42229
The new Table of Contents block automatically generates a clickable list of links to all the headings in your post or page, making long-form content easier to navigate. As you add or edit headings, the table updates automatically. For readers, this provides a quick overview and jump-to navigation; for writers, it encourages better content structure and improves accessibility.

## Tabs block — tracking #73230
The new Tabs block organizes content into separate tabbed panels that visitors click to reveal, letting you present information compactly without overwhelming the page. This is useful for FAQs, product features, or any content where you want to show options side-by-side. For editors, it's a familiar, flexible layout pattern now available natively in WordPress without needing a plugin.

## Gallery block lightbox refinements — tracking #56587
The Gallery block's lightbox feature gains swipe indicators and opt-in captions on mobile, improving the experience for visitors browsing image galleries on phones and tablets. Swipe indicators make it clear you can navigate by touch, and captions provide context without cluttering the gallery view. For photographers and visual storytellers, this makes mobile galleries more polished and user-friendly.

## HTML block editable blocks support
The HTML block now supports embedding editable blocks inside custom HTML markup, making it possible to mix hand-coded HTML with block-based content. This is especially useful when working with AI-generated sites, as AI models often produce custom HTML. For advanced users and developers, this bridges the gap between code and blocks, offering more flexibility without sacrificing editability.

## Mark as decorative toggle
The Image block gains a "Mark as decorative" toggle that hides decorative images from screen readers, improving accessibility. Decorative images (like design flourishes) don't convey essential information, so hiding them reduces noise for users relying on assistive technology. For content creators focused on accessibility, this provides an easy, built-in way to follow best practices.

## Embed block shortcode transform
Pasting or converting an [embed] shortcode now automatically creates a proper Embed block instead of leaving raw shortcode text behind. This makes migrating older content smoother and ensures embeds from YouTube, Twitter, and other services display correctly. For users importing content or working with legacy posts, this removes a common cleanup step.

## Shortcode block specific transforms
When you paste text matching a registered shortcode into a Shortcode block, WordPress now offers block-specific transforms to convert it into the equivalent block automatically. This makes it much easier to modernize old shortcode-based content into blocks. For editors working with older sites, this speeds up the transition to block-based editing.

## Group block background gradients
The Group block now supports background gradients through a new background.gradient block support, allowing gradients and background images to coexist without conflicts. You can apply rich, layered backgrounds to sections of your page directly in the editor. For designers, this opens up more creative possibilities without needing custom CSS, and the feature will expand to more blocks in future releases.

## Writing flow and drag-and-drop improvements — tracking #63255
A dedicated focus on everyday writing pain points brings improvements to drag-and-drop block reordering and multi-selection on touch devices. These refinements make arranging content smoother and more intuitive, especially on tablets. For writers and editors, this reduces friction in the day-to-day task of organizing posts and pages, making the editor feel more responsive and natural.

## Notes features: suggestions and reactions — tracking #76316
Notes (inline comments and feedback within the editor) gain major improvements: you can leave notes on specific content within or across multiple blocks, use rich text formatting, receive notifications for replies and follows, add emoji reactions, and apply suggestions directly. A minified notes view keeps feedback unobtrusive. For teams collaborating on content, this makes asynchronous feedback richer, more interactive, and easier to act on without leaving WordPress.

## Real-time collaboration — tracking #76377
Real-time collaboration aims to let multiple editors (human and AI) work on the same post simultaneously without post locks, seeing each other's changes as they happen. Strategic decisions around what to ship (full feature vs. underlying architecture) and storage mechanisms are still being finalized, with dedicated outreach and testing underway. For collaborative teams, this promises a Google Docs–style editing experience directly in WordPress, though the exact rollout and availability are still being determined.

## Display inherited styles — tracking #77595
When styling a block, it's often unclear whether styles come from the theme, a parent block, or global settings. This feature surfaces inherited styles clearly in the sidebar, showing you where each style originates and letting you edit at the right layer—global or local. For designers and site builders, this transparency makes styling more predictable and helps you avoid accidentally overriding the wrong settings.

## Interactive states styling (hover, focus) — tracking #38277
You can now style interactive pseudo-states like hover, focus, and active for blocks—both globally and per-instance—without writing any CSS. For example, change a button's color on hover directly in the editor. This makes interactive design accessible to non-coders and eliminates the need to add custom CSS snippets for common interactions. Future work will expand this to custom states like styling the current menu item.

## Pattern editing experience improvements — tracking #75717
WordPress 7.0 shifted pattern editing to focus on content changes rather than exposing every tool, treating patterns more like single blocks. In 7.1, work focuses on UX refinements based on feedback, bug fixes, and general maintenance. For users inserting and customizing patterns, this means a more polished, predictable experience with fewer rough edges.

## Responsive styling for blocks — tracking #77817
Responsive styling lets you define how a block looks at different screen sizes—for example, use a larger font on desktop and a smaller one on mobile—directly in the editor without custom CSS. This works for both global styles (affecting all instances of a block) and individual block instances. For designers and site builders, this makes responsive design a built-in, first-class part of the editing experience, ensuring your site looks great on all devices.

## Viewport breakpoint customization — tracking #75707
Building on the ability to hide or show blocks by viewport size, themes can now define custom breakpoints in theme.json, giving you more flexible, fine-grained control over responsive behavior. Instead of being locked to default breakpoints, you can tailor responsive styling to match your design system. For theme developers and designers, this provides the precision needed for modern, device-agnostic layouts.

## Client-side media processing improvements — tracking #76756
Client-side media processing (handling images and videos in your browser before upload) gains HEIC and Ultra HDR image support, GIF-to-video conversion, resilient uploads that retry on failure and resume after crashes or going offline, video transcoding to web-safe formats, optimization of previously uploaded media, and local poster generation for videos. For editors uploading media, this means faster, more reliable uploads, broader format support, and better-optimized files without manual intervention.

## Free-form media editor modal — tracking #73771
The new media editor modal replaces the inline cropping tool, accessed via the familiar Crop button, and brings together free-form and aspect-ratio cropping, flip, fine-grained rotation with snap guides, and metadata editing in one unified workflow. For editors preparing images, this provides a more powerful, streamlined editing experience without leaving WordPress or needing external tools.

## Media gallery improvements — tracking #77117
Galleries become more dynamic and easier to build with better handling of the legacy [gallery] shortcode on conversion, dynamic galleries that can automatically pull or sort media attached to the current post, and a quicker path in the inserter's media tab to attached images with thumbnails shown directly. For content creators, this makes assembling image galleries faster and more flexible, especially when working with post attachments.

## Speculative loading performance update
Speculative loading (prefetching and prerendering pages before visitors click) will shift from conservative to moderate eagerness on sites with both object caching and page caching detected, making navigation feel faster. The browser intelligently loads likely-next pages in the background, so clicking a link shows content almost instantly. For visitors, this means a snappier, app-like browsing experience on well-optimized sites.

## View Transitions plugin
The View Transitions feature plugin brings smooth, animated transitions between pages on the front end, similar to single-page app experiences. It's under active development as a plugin you can install today, with the goal of eventual Core inclusion. For site owners wanting a more polished, modern front-end experience, this adds visual continuity as visitors navigate your site.

## Enhanced Responsive Images plugin
The Enhanced Responsive Images plugin computes more accurate sizes attributes for images in block themes, ensuring browsers download appropriately sized images and improving performance. It's available as a plugin today with active development toward Core. For site owners, this means faster page loads and less wasted bandwidth, especially on mobile devices, with no manual image optimization needed.
