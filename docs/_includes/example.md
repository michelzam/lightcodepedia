{% assign module = include.module | default: "welcome" %}

<p>
  <iframe
    src="https://lightcodepedia1.streamlit.app/?embed=true&embed_options=hide_toolbar&module={{ module | uri_escape }}"
    width="100%"
    height="1600"
    loading="lazy"
    allowfullscreen
    style="border:none;">
  </iframe>
</p>