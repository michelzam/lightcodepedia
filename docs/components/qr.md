---
---
# 📱 QR Code

Turn any URL or text into a scannable QR code — one fenced block, one tag.

## 👀 See it in action

```
https://lightcodepedia.org
Scan to visit Lightcodepedia
```
{: .qr }

Point your phone camera at it. It just works.

## 🛠️ How to make one

Put the URL (or any text) on the first line. An optional second line becomes a caption below the code.

````markdown
```
https://example.com
Your caption here
```
{: .qr }
````

Text-only QR — no caption:

````markdown
```
https://example.com
```
{: .qr }
````

## 🔧 Knobs

| Attribute | Default | What it does |
|-----------|---------|-------------|
| `size="N"` | `180` | Width and height in pixels |

**Larger code for easier scanning:**

```
https://lightcodepedia.org
```
{: .qr size="260" }

**Compact code for dense layouts:**

```
https://lightcodepedia.org
```
{: .qr size="120" }

## 💡 What can go inside

Any text works — URLs, email addresses, phone numbers, plain text, Wi-Fi credentials.

```
mailto:hello@example.com
Email us
```
{: .qr }

**Q:** What goes on the first line of the fenced block?

- [ ] The caption to display below the QR code.
- [x] The URL or text to encode into the QR code.
- [ ] The image format (png or svg).
- [ ] The error-correction level.
{: .quiz }

**Q:** You want a QR code 240 px wide. Which IAL do you use?

- [ ] `{: .qr width="240" }`
- [x] `{: .qr size="240" }`
- [ ] `{: .qr height="240" }`
- [ ] `{: .qr px="240" }`
{: .quiz }
