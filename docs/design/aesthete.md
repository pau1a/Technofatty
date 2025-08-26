# Technofatty — Aesthetic Master Directive

This document defines the locked aesthetic rules for TF.  
It is non-negotiable without stakeholder sign-off.  
GED must implement according to these specifications.

---

## 1. Typography System

**Headings**  
- Typeface: **IBM Plex Sans** (open source).  
- Usage: H1–H4, hero copy, primary CTAs.  
- Letter-spacing:  
  - H1/H2: −0.01em to −0.02em (tight).  
  - H3/H4: −0.005em (slight).  
  - H5/H6/UI labels: neutral or +0.02em to +0.05em (open).  
- Weight:  
  - H1/H2: 700.  
  - H3/H4: 600.  
  - UI labels: 500.

**Body & UI Text**  
- Typeface: **System UI stack** (San Francisco, Segoe UI, Roboto, etc.).  
- Letter-spacing: untouched (native defaults).  
- Weight: 400–500 as needed.  

**Rules**  
- No other fonts permitted without approval.  
- No inconsistent tracking between headings of the same tier.  
- GED must ensure SCSS variables reflect these rules.

---

## 2. Motifs

**Primary Motif: Grid**  
- Constructed in-house.  
- Implementation: CSS background or 1×1 SVG tile.  
- Must reference `$space` tokens.  
- Colours: inherited from SCSS tokens.  
- Role: backbone motif, subtle background texture across the site.

**Secondary Accents**  
- **Node-field**: minimal points + optional connecting lines.  
- **Waveform**: smooth sine/contour lines, no psychedelic shapes.  
- Max 2–3 static SVGs each.  
- Stored under `/static/coresite/svg/motifs/`.  

**Sanitisation**  
- All SVGs processed through SVGO.  
- No inline `style`, no hardcoded hex, no `id` collisions.  
- Only class hooks and token references allowed.  
- File size target: single-digit KB.  

**Rules**  
- Grid is always the default motif.  
- Node-field and Waveform only as deliberate accents.  
- No motifs outside these families permitted.

---

## 3. Imagery Style

**Abstracts**  
- Derived directly from motif families.  
- Applied in heroes, section dividers, and background bands.  
- Always token-coloured, never freehand gradients.

**Photography**  
- Only generated photo-real images via TF’s MidJourney pipeline.  
- Style must remain consistent (lighting, tone, framing).  
- Usage: people, customer stories, product context.  

**Illustration**  
- Not part of TF’s aesthetic system at this stage.  
- No illustration packs, no startup-style flat vectors.  

**Rules**  
- Abstracts + controlled AI-assisted photography define TF’s visual voice.  
- GED must not introduce external stock or unapproved visuals.  
- All assets checked for consistency against this directive before merge.

---

## Enforcement

- This directive overrides any legacy SCSS, templates, or assets.  
- GED must not improvise beyond these rules.  
- Deviations require explicit stakeholder sign-off, logged in writing.
