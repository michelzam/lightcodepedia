{% assign _lang = include.lang | default: "text" %}
{% assign _title = include.title | default: "" %}

<style>
.lc-code { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: #fafafa; }
.lc-code-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-code-title .lc-code-lang { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: #888; letter-spacing: 0.05em; }
.lc-code .highlight, .lc-code pre { margin: 0 !important; background: transparent !important; }
.lc-code .highlight pre, .lc-code > pre { padding: 0.9em 1em !important; overflow-x: auto; font-size: 0.85em; line-height: 1.5; }
</style>

<div class="lc-code" markdown="0">
{% if _title != "" %}<div class="lc-code-title">📄 <span>{{ _title }}</span><span class="lc-code-lang">{{ _lang }}</span></div>{% endif %}
{% if _lang == "yaml" %}{% highlight yaml %}{{ include.content }}{% endhighlight %}
{% elsif _lang == "python" %}{% highlight python %}{{ include.content }}{% endhighlight %}
{% elsif _lang == "javascript" or _lang == "js" %}{% highlight javascript %}{{ include.content }}{% endhighlight %}
{% elsif _lang == "json" %}{% highlight json %}{{ include.content }}{% endhighlight %}
{% elsif _lang == "html" %}{% highlight html %}{{ include.content }}{% endhighlight %}
{% elsif _lang == "css" %}{% highlight css %}{{ include.content }}{% endhighlight %}
{% elsif _lang == "bash" or _lang == "sh" %}{% highlight bash %}{{ include.content }}{% endhighlight %}
{% elsif _lang == "ruby" %}{% highlight ruby %}{{ include.content }}{% endhighlight %}
{% elsif _lang == "liquid" %}{% highlight liquid %}{{ include.content }}{% endhighlight %}
{% else %}<pre><code>{{ include.content | strip | escape }}</code></pre>
{% endif %}
</div>
