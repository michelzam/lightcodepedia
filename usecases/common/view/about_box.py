import streamlit as st
import streamlit.components.v1 as components

def about():
    components.html("""
    <script>
    (function () {
      const observer = new MutationObserver(() => {
        const popover = window.parent.document.querySelector('[data-testid="stMainMenuPopover"]');
        if (!popover) return;

        const spans = popover.querySelectorAll("span");
        for (const span of spans) {
          if (span.textContent.trim() === "About" && !span.dataset.michelHacked) {
            span.textContent = "About ...";
            span.dataset.michelHacked = "true";

            const li = span.closest("li");
            if (li) {
              li.addEventListener("click", (e) => {
                e.preventDefault();
                e.stopPropagation();
                alert(
                  "💡 LightCode 2026\\n" +
                  "-----------------------------\\n" +
                  "Made with:\\n" +
                  "- Streamlit v1.41.0\\n" +
                  "  https://streamlit.io\\n" +
                  "  Copyright 2026 Snowflake Inc. All rights reserved.\\n\\n" +
                  "- Smalljects v2.2.0\\n" +
                  "  https://www.karmicsoft.com\\n" +
                  "  Copyright 2021-2026 KarmicSoft. All rights reserved.\\n"
                );
              }, { once: false });
            }
          }
        }
      });

      observer.observe(window.parent.document.body, {
        childList: true,
        subtree: true
      });
    })();
    </script>
    """, height=0)