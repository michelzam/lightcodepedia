# 🔬 Actually Relevant — science & technology (API)

The latest science and technology stories from [Actually Relevant](https://actuallyrelevant.news/issues/science-technology), pulled **live** from its public API — no key. Three readable views of one fetch: a **list** to scan, a **card** that fills when you click a story, and a **frame** that follows your click.

[Actually Relevant — science & technology](https://actually-relevant-api.onrender.com/api/stories?issueSlug=science-technology)
{: .dataset #stories path="data" }

```sql
SELECT titleLabel AS topic, title, datePublished AS published,
       summary, quote, quoteAttribution AS said_by,
       sourceTitle AS source, sourceUrl AS page
FROM stories ORDER BY datePublished DESC
```
{: .query source="stories" #readable }

## 📋 The list — click a story

[Stories — newest first](#)
{: .datagrid source="readable" #stories_grid columns="topic, title, published" height="260" }

## 🃏 The card — the story you clicked

[The story](#)
{: .form master="stories_grid" }

## 🖼️ The page — the issue, then the story you clicked

While the stories load, the issue as Actually Relevant lays it out. Then the source article of the selected story — the newest at first, the one you click after. A source that refuses to be framed leaves the box blank — the list and the card do not depend on it.

[Actually Relevant — Science & Technology](https://actuallyrelevant.news/issues/science-technology)
{: .embed master="stories_grid" height="600" }

`````
### 🧩 How it works
- `{: .dataset #stories path="data" }` on a link fetches the API and lifts the `data` array out of the envelope (`total`, `page`, `pageSize` stay behind).
- `{: .query source="stories" }` runs SQL **in the browser**: it keeps the eight readable fields, renames them pythonistically, and sorts newest first. The API's nested `issue` and `feed` objects and its long bullet fields are simply not selected.
- The grid binds with `source="readable"` and draws only `columns="topic, title, published"`; the row it publishes is still whole. Rows are not links on purpose: a `url` column would make every row open a tab instead of selecting it.
- `{: .form master="stories_grid" }` is the detail view: it fills with the row you click — title, summary, quote, who said it, the source. The list prints the stamp in your local time; the card keeps it as the API sent it.
- `{: .embed master="stories_grid" }` frames the link's page while the grid is empty, then the selected row's `page` field.

### 🥸 The whole page in markdown
````markdown
[Actually Relevant](https://actually-relevant-api.onrender.com/api/stories?issueSlug=science-technology)
{: .dataset #stories path="data" }

```sql
SELECT titleLabel AS topic, title, summary, quote, sourceUrl AS link
FROM stories ORDER BY datePublished DESC
```
{: .query source="stories" #readable }

[Stories](#)
{: .datagrid source="readable" #stories_grid columns="topic, title, published" height="260" }

[The story](#)
{: .form master="stories_grid" }

[Actually Relevant — Science & Technology](https://actuallyrelevant.news/issues/science-technology)
{: .embed height="600" }
````
`````
{: .accordion }

> Live data — the stories are whatever Actually Relevant published last. The API is a free service on a sleeping host: the first fetch of the day can take half a minute to wake up, and the shape can change. The summaries, quotes and labels are machine-written; the API says so in each record's `aiGenerated` field.
{: .speaker-note }
