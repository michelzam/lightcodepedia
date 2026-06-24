# 📜 Project History

Lightcodepedia has three generations. Only the third is the current platform.

| Generation | Stack | Status |
|---|---|---|
| **1. Karmicsoft origins** | YAML-driven app definitions | Historical inspiration |
| **2. Erasmus+ / Streamlit era** | Streamlit Cloud, server-side Python | Ended — architecture retired |
| **3. Serverless platform** | GitHub Pages + Jekyll + browser-side everything | **Active** |

## 1. Karmicsoft origins

The conceptual ancestor of today's declarative blocks: the idea that an
application can be *declared* in plain text rather than programmed. That
YAML-driven philosophy is the one continuous thread running from the first
generation through to today's IAL and YAML component blocks.

## 2. The Erasmus+ / Streamlit era

A server-based platform built on Streamlit Cloud, co-funded by the Erasmus+
programme of the European Union (Project Nr. 2022-1-FR01-KA220-HED-00086863).
This generation established the pedagogical mission and the community of
educators around it. The funding period has since closed and the architecture
has been retired.

Why the server-based approach was abandoned:

- It required a running server process — a cost, a dependency, a single point of failure
- Stateful sessions don't fork: an educator couldn't clone the platform in minutes
- Server-side Python meant contributors had to understand deployment, not just Markdown

## 3. The serverless platform (current)

A *sister* of the Erasmus branch, not its continuation: it shares the
repository and the pedagogical mission, but no code. Everything runs in the
visitor's browser — Python via Micropython, interactivity via the component
runtime — on a static GitHub Pages site. All state is client-side or flat
files committed to `main`.

No server, no cost to scale, forkable in minutes: each fork is a
[LightNode](/nodes), owned by an educator.

[ℹ️ About](/about) · [🚀 Start your own node](/start)
