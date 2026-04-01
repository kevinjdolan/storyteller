# 97 — Security Review and Secret Handling Pass

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Perform a targeted security pass around secrets, downloads, storage access, and user-provided content.

## Build
- Review how `secrets.yaml`, environment variables, download endpoints, and storage paths are handled and tighten anything too loose.
- Make sure the frontend never receives sensitive provider credentials.
- Review obvious injection and unsafe rendering surfaces in chat, story text, and generated metadata.

## Deliverables

- Security review notes
- Any code fixes for secret handling or unsafe rendering
- Updated docs where needed

## Acceptance checks

- The project’s secret-handling story is clear and reasonably safe for local development.
- Artifact access stays mediated through the backend.
- User and model text is rendered safely.

## Notes

Aim for practical hardening, not ceremony.

## Suggested commit label

`feat(prompt-97): security review`
