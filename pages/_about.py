import streamlit as st
import os

from usecases.common.common import page_config, get_params

page_config(__file__)

st.title("🌟 About")


with st.expander("Licence", expanded=False, icon="🗣️"):
    # Get the absolute path to the main directory where main.py is located
    MAIN_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))

    # Construct the correct path to the licence.md file in the main directory
    licence_file = os.path.join(MAIN_DIR, "licence.md")

    try:
        with open(licence_file, "r", encoding="utf-8") as f:
            licence_text = f.read()
            st.markdown(licence_text)
    except FileNotFoundError:
        st.error("Licence file not found. Please ensure 'licence.md' is in the main directory.")
    except Exception as e:
        st.error(f"An error occurred while reading the licence file: {e}")


with st.expander("More"):
    import psutil, os

    if st.button("Show psutil"):
        process = psutil.Process(os.getpid())
        ram_mb = process.memory_info().rss / 1024 / 1024
        st.metric("RAM used (MB)", f"{ram_mb:.0f}")