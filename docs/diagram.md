This is a diagram:

{% raw %}
```mermaid
graph TD
  A[Start] --> B{Decision}
  B -->|Yes| C[Do something]
  B -->|No| D[Do something else]
```
{% endraw %}

```python
print("Hello world!")
