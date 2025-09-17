import traceback

import streamlit as st
from streamlit_javascript import st_javascript
from streamlit_js_eval import streamlit_js_eval
# from gevent.testing.monkey_test import module_code
from streamlit_extras.row import row
from contextlib import redirect_stdout
import lightcode
import io
import os
import time
import difflib
from streamlit_ace import st_ace
import qrcode
from PIL import Image

from lightcode import page_config, import_module, set_next_page
from usecases.common.backend.module_importer import preview_module, get_loader
from usecases.module_manager.backend.module_decorator import ModuleDecorator
from usecases.module_manager.backend.module_dumper import ModuleDumper

page_config(__file__)

try:
    import_module(st.session_state.next_page)

except Exception as e:
    st.warning(f"🧐 Something's wrong. Please go back to the main page.")
    st.caption(f"⚠️Refreshing your browser would lead to a new session, and you will lose all unsaved changes.")
    st.caption(f"👇 You can also click on the link below go back to the main page.")
    st.page_link("main.py", label="Lightcode", help="", icon="💡")  # , use_container_width=True)
    with st.expander("Show errors"):
        st.warning(f"Error: {e}")

