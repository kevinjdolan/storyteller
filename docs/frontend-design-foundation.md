# Frontend Design Foundation

This note documents the shared visual and accessibility baseline introduced for
prompt 24 so later workflow screens can build on one calm, consistent layer.

## Token categories

- Typography: body, display, and mono font stacks plus label and body text sizes.
- Spacing: `--space-1` through `--space-10` cover compact labels through large
  panel gaps.
- Radius: small, medium, large, extra-large, and pill radii keep cards,
  controls, and badges visually related.
- Color: bedtime-friendly ink, surface, brand, moss, gold, and rose tones are
  centralized in CSS variables instead of being repeated inline.
- Depth: shared surface and button shadows support the soft, paper-like panel
  treatment.

## Accessibility checklist

- Keyboard focus is globally visible through `:focus-visible`, including links,
  buttons, and form controls.
- A skip link lands on the main content region before the app header and utility
  rail.
- Motion-heavy effects are wrapped in `prefers-reduced-motion` handling.
- Text inputs require labels and wire descriptions and errors through
  `aria-describedby`.
- Progress bars expose `role="progressbar"` plus value metadata.
- Route layouts keep semantic headings in the page content rather than relying
  on decorative branding alone.

## Primitive usage

```tsx
import {
  Badge,
  Button,
  Panel,
  ProgressBar,
  TextInput,
} from '../shared/ui/primitives.tsx'

<Panel
  eyebrow="Story setup"
  headingLevel={2}
  title="Planning preferences"
  description="Soft targets for length and pacing."
>
  <TextInput
    label="Target runtime"
    description="Guides narration length without forcing a hard cap."
    placeholder="About 12 minutes"
  />
  <ProgressBar
    aria-label="Planning completion"
    label="Planning completion"
    value={60}
    valueText="6 of 10 steps complete"
  />
  <Button>Continue</Button>
  <Badge tone="brand">Draft</Badge>
</Panel>
```
