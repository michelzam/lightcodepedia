# 🐍 Python Tutor

Step-by-step code visualizer — shows variables, the call stack, and heap objects as your program runs. Powered by [pythontutor.com](https://pythontutor.com).

## Basic example

```python
x = [1, 2, 3]
for i in x:
    print(i * 2)
```
{: .pytutor height="420" }

## Recursive function

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
print(result)
```
{: .pytutor height="500" }

## Side by side — code and visualizer

````
### 📝 Edit the code

```python
a = 10
b = 20
c = a + b
print(c)
```
{: .run }

### 🔬 Step through it

```python
a = 10
b = 20
c = a + b
print(c)
```
{: .pytutor }
````
{: .blocks cols="2" }

## Live-bound to a `.run` editor

Use `bound-to` to link a `.pytutor` block to a `.run` editor. Every time you edit the code, the visualizer refreshes after a short pause.

````
### 📝 Edit the code

```python
for i in range(3):
    print(i * 2)
```
{: .run #live-demo }

### 🔬 Visualizer (updates as you type)

```python
for i in range(3):
    print(i * 2)
```
{: .pytutor bound-to="live-demo" height="450" }
````
{: .blocks cols="2" }

## Syntax

~~~markdown
```python
your code here
```
{: .pytutor }
~~~

| Attribute | Default | Description |
|-----------|---------|-------------|
| `height` | `400` | iframe height in px |
| `bound-to` | — | ID of a `.run` block (without `#`). Reloads the visualizer on every keystroke (debounced 600 ms). |

Always runs on the latest Python 3 available in the Python Tutor embed.
