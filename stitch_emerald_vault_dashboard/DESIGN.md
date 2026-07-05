---
name: Obsidian Sentinel
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#393939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#bacbb9'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#859585'
  outline-variant: '#3b4a3d'
  surface-tint: '#00e475'
  primary: '#75ff9e'
  on-primary: '#003918'
  primary-container: '#00e676'
  on-primary-container: '#00612e'
  inverse-primary: '#006d35'
  secondary: '#45fec9'
  on-secondary: '#003829'
  secondary-container: '#00e1ae'
  on-secondary-container: '#005e47'
  tertiary: '#ffdec4'
  on-tertiary: '#4b2800'
  tertiary-container: '#ffba79'
  on-tertiary-container: '#794810'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#62ff96'
  primary-fixed-dim: '#00e475'
  on-primary-fixed: '#00210b'
  on-primary-fixed-variant: '#005226'
  secondary-fixed: '#45fec9'
  secondary-fixed-dim: '#00e1ae'
  on-secondary-fixed: '#002117'
  on-secondary-fixed-variant: '#00513d'
  tertiary-fixed: '#ffdcbf'
  tertiary-fixed-dim: '#fdb878'
  on-tertiary-fixed: '#2d1600'
  on-tertiary-fixed-variant: '#6a3c03'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-data:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  sidebar_width: 260px
  container_max_width: 1440px
  gutter: 24px
  margin_mobile: 16px
  margin_desktop: 40px
---

## Brand & Style
The design system is engineered to evoke an immediate sense of impenetrable security and high-performance utility. It targets tech-savvy professionals and security-conscious individuals who require a tool that feels both advanced and effortless.

The aesthetic follows a **Modern Minimalism** approach with **Cyber-Tech** influences. By utilizing a deep charcoal base, the interface recedes into the background, allowing high-contrast neon emerald accents to guide the user's eye to critical actions and security statuses. The emotional response is one of calm control: the UI doesn't shout; it whispers authority through precision, spaciousness, and a lack of visual clutter. Visual hierarchy is established through luminous accents and soft elevation rather than aggressive borders.

## Colors
The palette is rooted in a "True Dark" philosophy to minimize eye strain and maximize the vibrance of the primary accent.

- **Primary (#00E676):** Used exclusively for primary buttons, active toggle states, and "Secure" status indicators.
- **Secondary (#1DE9B6):** A cool-toned teal used for secondary data visualizations and subtle highlights.
- **Neutral/Background (#121212):** The base canvas.
- **Surface (#1E1E1E):** Used for cards, sidebar, and elevated containers to create depth against the background.
- **Text:** High-emphasis text uses `#FFFFFF` (95% opacity), while secondary metadata uses a muted slate `#94A3B8`.

## Typography
This design system utilizes **Inter** for its exceptional legibility in digital interfaces and its neutral, systematic feel. 

For sensitive data like passwords or recovery keys, the system introduces **JetBrains Mono** to ensure character clarity (distinguishing between 'l', '1', and 'I'). Use `label-caps` for section headers in the sidebar and widget titles to create a structured, professional cadence. Large headlines should use tighter letter spacing to maintain a "sleek" technical appearance.

## Layout & Spacing
The layout employs a **Fixed Sidebar** with a **Fluid Content Area**. 

- **Sidebar:** Remains fixed at 260px. It uses a slightly lighter surface color than the background to establish a vertical anchor.
- **Grid:** A 12-column grid is used for the main dashboard content. Security widgets typically span 3 or 4 columns, while the primary password list spans the remainder.
- **Rhythm:** An 8px linear scale governs all padding and margins. Use generous whitespace (24px - 32px) between cards to prevent the interface from feeling "heavy" or cramped.
- **Sticky Search:** The top search bar remains docked during scroll, using a subtle backdrop-blur (10px) to maintain context.

## Elevation & Depth
Depth is created through **Tonal Layering** rather than traditional drop shadows. 

1. **Level 0 (Background):** `#121212` - The base layer.
2. **Level 1 (Cards/Sidebar):** `#1E1E1E` - Softly elevated surfaces.
3. **Level 2 (Hover/Active):** `#2A2A2A` - Used for active row states or hovered cards.

Shadows, when used (e.g., on modals), should be extremely diffused: `0px 8px 32px rgba(0, 0, 0, 0.8)`. For the neon accent elements, a subtle "outer glow" using the primary color at 20% opacity can be applied to simulate a technical, illuminated display.

## Shapes
The shape language is defined by "Soft Precision." 

Standard components (buttons, input fields, cards) use a **0.5rem (8px)** corner radius. This creates a modern, approachable feel that isn't as aggressive as sharp corners nor as casual as pill shapes. Progress rings and favicons within account cards should remain circular to provide a geometric contrast to the rectangular grid of the dashboard.

## Components
- **Primary Buttons:** Solid `#00E676` background with `#121212` text for maximum contrast. No borders.
- **Account Cards:** Feature a prominent 32px circular favicon on the left, followed by the account name and a masked password preview in `mono-data` font.
- **Security Widgets:** Incorporate circular progress rings with a 4px stroke width. The "unused" portion of the ring should be `#2A2A2A`, while the "active" portion uses the primary green.
- **Data Rows:** For the main list, use horizontal rows with a 1px border-bottom in `#2A2A2A`. On hover, the entire row background transitions to `#252525`.
- **Input Fields:** Use a dark-filled style (`#1E1E1E`) with a subtle `#333333` border. On focus, the border changes to the primary `#00E676` with no inner glow, only a crisp color change.
- **Chips/Badges:** Small, low-profile indicators for "Weak," "Reused," or "Compromised" status. These should use a ghost-style (border only) or a 10% opacity background of the semantic color (e.g., Red for Weak).