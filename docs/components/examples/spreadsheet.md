---
title: "Reactive table — computed columns"
---

# 🧮 Reactive table — computed columns

A spreadsheet is a grid where some cells are **formulas** that recompute when
their inputs change. You already have the grid (`.datagrid`, AG Grid) and the
formula engine (the `= expr` we use for reactive cells) — this wires them
together: a **`compute`** knob declares columns whose value is a Python
expression evaluated **per row**, live.

## 🐕 Edit a number, watch the ƒ columns recalc {#sheet}

`top_speed_kmh` and `cute` are inputs — **click a cell and type**. The two **ƒ**
columns are derived and read-only; they recompute the instant you edit:

```csv
breed,top_speed_kmh,cute
Greyhound,72,70
Saluki,68,72
Vizsla,64,78
Border Collie,48,82
Labrador,40,92
Beagle,40,88
Corgi,35,95
Pug,15,98
```
{: .datagrid #dogs format="csv" editable="true" height="330" compute="score = round(top_speed_kmh * cute / 100, 1); tier = '🔥 fast' if score >= 40 else '🐢 chill'" }

Try it: drop **Pug**'s `top_speed_kmh` or bump its `cute` — `score` follows, and
`tier` flips when `score` crosses 40.

## ✍️ How it's written {#how}

One knob, one formula per column, separated by `;`:

```markdown
{: .datagrid editable="true" compute="score = round(top_speed_kmh * cute / 100, 1); tier = '🔥 fast' if score >= 40 else '🐢 chill'" }
```

| Piece | Meaning |
|---|---|
| `score = …` | a **computed column** — its value is the expression, evaluated for each row |
| `top_speed_kmh`, `cute` | the row's other columns, read **by name** (bare, spreadsheet-style) |
| `score >= 40 else …` | the row's *own* computed columns are available too — `tier` reads `score` (declared earlier) |
| `round(…)`, `… if … else …` | any Python **expression** — comprehensions and ternaries included |

- **Formulas are `eval`'d, never `exec`'d.** A statement can't be typed into a
  column, and a bad formula shows **⚠** in *its own cell* — never a frozen grid.
- **Columns compute in declaration order**, so a later column may build on an
  earlier one (`tier` uses `score`).
- Computed columns are **read-only** and marked **ƒ**; the input columns stay
  editable.

## 🔗 Same engine as reactive cells {#same_engine}

This is the exact `= formula` model from the [reactive cells](/components/examples/reactive)
page, applied to a grid instead of prose: the same shared page runtime, so a
column formula can even call a helper defined in a hidden `{: .run silent="true" }`
model. Grid cells that hold formulas and recompute on edit — that's the
spreadsheet, built from parts you already had.
