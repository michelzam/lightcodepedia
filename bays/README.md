# 🚀 Bays — deployment spike

Public shipping target for Lightcodepedia PoCs. Each folder is `app_sha`
(immutable, provenance-pinned); `manifest.json` records the latest sha per
app. Links are the protection: nothing lists or indexes these folders.

This folder is OUTSIDE the publish gate's rsync paths (docs/, packages/,
tests/, workflows) — publishes never touch it.
