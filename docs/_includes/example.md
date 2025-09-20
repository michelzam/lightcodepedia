{% assign module = include.module | default: "welcome" %}

<p>
  <iframe
    src="https://lightcodepedia1.streamlit.app/?module={{ module | uri_escape }}&embed=true&embed_options=hide_toolbar"
    width="100%"
    height="1600"
    loading="lazy"
    allowfullscreen
    style="border:none;">
  </iframe>
</p>