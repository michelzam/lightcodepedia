# 📰 Hacker News front page (API)

The current Hacker News front page, pulled **live** from the free [HN Algolia](https://hn.algolia.com/api) API — no key. `path="hits"` lifts the array of stories out of the response; a query trims the (very wide) raw rows down to the columns worth seeing, and the `url` column makes each row a clickable link.

[HN front page](https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=15)
{: .dataset #news path="hits" }

```sql
SELECT title, points, num_comments AS comments, author, url
FROM news ORDER BY points DESC
```
{: .query source="news" #top_news }

[Top stories — click a row to open it](#)
{: .datagrid source="top_news" rows="15" }

## How it works

- `{: .dataset #news path="hits" }` on a link fetches the API and extracts the `hits` array.
- `{: .query source="news" }` runs SQL **in the browser** to keep five columns and sort by points.
- The grid binds with `source="top_news"`. Because the rows carry a `url`, that column is hidden and each row becomes a clickable link.

````markdown
[HN front page](https://hn.algolia.com/api/v1/search?tags=front_page)
{: .dataset #news path="hits" }

```sql
SELECT title, points, author, url FROM news ORDER BY points DESC
```
{: .query source="news" #top_news }

[Top stories](#)
{: .datagrid source="top_news" }
````

> Live data — the list is whatever's actually on the HN front page right now. The API is a free public service that can rate-limit or change.
{: .speaker-note }
