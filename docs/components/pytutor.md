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

## Syntax

~~~markdown
```python
your code here
```
{: .pytutor }
~~~

| Attribute | Default | Description |
|-----------|---------|-------------|
| `py` | `3` | Python version: `2` or `3` |
| `height` | `400` | iframe height in px |
