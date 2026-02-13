import sys
import time
from typing import Dict
import inspect

import streamlit
import streamlit as st
from streamlit_float import float_init
from streamlit_extras.row import row
from streamlit_extras.bottom_container import bottom
import re
from dataclasses import dataclass
from usecases.common.backend.services import ScriptManager
from usecases.common.backend.tracing import trace_execution_time
from PIL import ImageFont
from config.settings import ACTIVE_SESSIONS, SESSION_TTL
import uuid, time


@dataclass
class LayoutMaker:
    script_manager: ScriptManager = None
    show_header: bool = True

    # @trace_execution_time
    def __post_init__(self):
        float_init()
        self.header_container = st.container()
        self.footer_container = st.container()

    def build(self):
        self._build_header()
        self._build_footer()
        self._reset_page_config()

    def _build_header(self):
        self.header_container.float("top: 0; z-index: 997; height: 120px;")

        with self.header_container:
            # Insert the blur-only header background (no gradient)
            st.markdown("""
                <style>
                .header-blur-underlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 118px;
                    backdrop-filter: blur(6px);
                    -webkit-backdrop-filter: blur(6px);
                    background-color: rgba(255, 255, 255, 0.05);  /* subtle gray tint to soften background */
                    z-index: 0;
                    pointer-events: none;
                }
                </style>
                <div class="header-blur-underlay"></div>
            """, unsafe_allow_html=True)

            #st.markdown("## ")
            st.caption("## ")
            disabled, extracted_details, help = self._scan_pages(directory="pages")

            widths = [10] * (len(extracted_details) + 1)
            widths.append(1)
            row_menu = row(widths)

            row_menu.page_link("main.py", label="Lightcode", help="", icon="💡")
            disabled = st.session_state.get("status", "unverfied") != "verified"

            for detail in extracted_details:
                row_menu.page_link(
                    f"pages/{detail[0]}_{detail[1]}_{detail[2]}.py",
                    label=f"{detail[2]}",
                    icon=detail[1],
                    help=help,
                    disabled=disabled
                )

            row_menu.page_link("pages/_about.py", label="", help="", icon="ℹ️")
            st.markdown("<hr style='border:0.1px solid lightgray; margin:0; padding:0; ' />", unsafe_allow_html=True)

    def xx_build_header(self):
        self.header_container.float("top: 0; z-index: 997; height: 150px;")

        with self.header_container:
            st.markdown("""
                <style>
                header[data-testid="stHeader"] {
                    background-color: transparent !important;
                    box-shadow: none !important;
                }

                .block-container {
                    background: transparent !important;
                    padding-top: 0rem !important;
                    margin-top: 0rem !important;
                }

                .main {
                    background-color: transparent !important;
                }

                html, body, [data-testid="stAppViewContainer"] {
                    background-color: transparent !important;
                }
                </style>
            """, unsafe_allow_html=True)

            st.markdown("# ")
            disabled, extracted_details, help = self._scan_pages(directory="pages")

            widths = [10] * (len(extracted_details) + 1)
            widths.append(1)
            row_menu = row(widths)
            row_menu.page_link("main.py", label="Lightcode", help="", icon="💡")
            disabled = st.session_state.get("status", "unverfied") != "verified"

            for detail in extracted_details:
                row_menu.page_link(
                    f"pages/{detail[0]}_{detail[1]}_{detail[2]}.py",
                    label=f"{detail[2]}",
                    icon=detail[1],
                    help=help,
                    disabled=disabled
                )

            row_menu.page_link("pages/_about.py", label="", help="", icon="ℹ️")
            st.markdown("<hr style='border:0.1px solid lightgray; margin:0; padding:0; ' />", unsafe_allow_html=True)


    # @trace_execution_time
    def _scan_pages(self, directory=None):
        pattern = r'(\d{2})_(.*)_([A-Za-z]+)\.py'

        # file_paths = glob(os.path.join(pages_directory, '*.py'))
        self.script_manager = ScriptManager()
        file_names = self.script_manager.scan(directory=directory)

        extracted_details = []
        disabled = False
        help = "Please be sure you're logged in" if disabled else ""

        for filename in file_names:
            # filename = os.path.basename(file_path)
            if filename.startswith("_"):
                continue
            match = re.match(pattern, filename)
            if match:
                number, icon, name = match.groups()
                extracted_details.append((number, icon, name))
        extracted_details.sort(key=lambda x: x[0])
        return disabled, extracted_details, help

    def _build_footer(self):
        # Inject blur background behind the footer content (underlay)
        st.markdown("""
        <style>
        .footer-blur-underlay {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 45px;
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            background-color: rgba(255, 255, 255, 0.05);  /* light gray tint, keeps light footer white, softens dark background only */
            z-index: 998;
            pointer-events: none;
        }
        </style>
        <div class="footer-blur-underlay"></div>
        """, unsafe_allow_html=True)

        # Actual footer content (above the blur)
        self.footer_container.float("bottom: 0; z-index: 1001;")
        with (self.footer_container):
            #st.markdown("---")
            st.caption("  ")
            row_footer = row(2)
            row_footer.caption("Copyright © 2025 KarmicSoft - All Rights Reserved.")
            try:
                first_name = st.session_state.user_name
            except Exception:
                first_name = " "
            row_footer.markdown(
                f"<div style='text-align: right; color: inherit; font-size: 14px;'>{first_name}</div>",
                unsafe_allow_html=True
            )
            #
            st.caption(" ")


    def _reset_page_config(self):

        if True:
            st.markdown("""
                <style>
                div[data-testid="stAppDeployButton"] {
                    display: none;
                }
                </style>
            """, unsafe_allow_html=True)

            st.markdown("""
                <style>
                footer {
                    display: none;
                }
                </style>""",
                        unsafe_allow_html=True)

        visibility = "visible" if self.show_header else "hidden"

        st.markdown("""
            <style>
            header[data-testid="stHeader"] {
                background-color: transparent !important;
                box-shadow: none !important;
                border: none !important;
                backdrop-filter: none !important;
                -webkit-backdrop-filter: none !important;
            }

            .header-blur-underlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 120px;
                backdrop-filter: blur(6px);
                -webkit-backdrop-filter: blur(6px);
                background-color: rgba(255, 255, 255, 0.05);
                z-index: 0;
                pointer-events: none;
            }

            [data-testid="stDecoration"] {
                display: none !important;
            }

            .stAppToolbar {
                background-color: transparent !important;
            }

            .st-emotion-cache-15ecox0,
            .st-emotion-cache-1dp5vir,
            .st-emotion-cache-19or5k2 {
                opacity: 0.65 !important;
            }
            </style>
        """, unsafe_allow_html=True)
        st.markdown("""
            <style>
            .block-container {
                padding-top: 0rem !important;
                margin-top: 0rem !important;
            }

            .main, .stApp {
                padding-top: 0rem !important;
                margin-top: 0rem !important;
            }
            </style>
        """, unsafe_allow_html=True)


# @trace_execution_time
def page_config(file_name: str = ""):

    store_url_args()

    if "sid" not in st.session_state:
        st.session_state.sid = str(uuid.uuid4())
        ACTIVE_SESSIONS[st.session_state.sid] = time.time()

    now = time.time()
    for sid, ts in list(ACTIVE_SESSIONS.items()):
        if now - ts > SESSION_TTL:
            del ACTIVE_SESSIONS[sid]

    if "status" not in st.session_state:
        st.session_state.status = "unverified"

    if "module_info" not in st.session_state:
        st.session_state.module_info = None

    if "next_page" not in st.session_state:
        # st.session_state.next_page = "welcome"
        set_next_page("welcome")

    # print(f"page_config: {file_name}")
    st.set_page_config(
        page_title="LightCode",
        page_icon="💡",
        #page_icon="modules/_media/bulb.jpg",
    layout="wide")
    st.markdown(
        """
        <style>
        body {
            overscroll-behavior-y: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    LayoutMaker().build()


def refresh():
    st.session_state["force_refresh"] = True


def check_refresh():
    if "force_refresh" in st.session_state:
        if st.session_state["force_refresh"]:
            st.session_state["force_refresh"] = False
            time.sleep(2)

            # st.rerun()

def toast(message: str = "", icon="🛟"):
    st.markdown("""
        <style>
        /* Target the toast container */
        div[data-baseweb="toast"] {
            z-index: 9999 !important;  /* Set a high z-index to bring it on top */
            position: fixed;          /* Ensure it stays in the same position on scroll */
            bottom: 100px;                /* Adjust vertical position */
            right: 20px;              /* Adjust horizontal position */
        }
        </style>
        """, unsafe_allow_html=True)
    st.toast(message, icon=icon)


def balloons():
    st.balloons()

def _st():
    return st


def get_next_page() -> str:
    if "next_page" not in st.session_state:
        return ""
    return st.session_state["next_page"]


def set_next_page(page: str):

    st.session_state["next_page"] = page

    if "page_stack" not in st.session_state:
        st.session_state.page_stack = []

    st.session_state.page_stack.append(st.session_state.next_page)

def store_url_args():
    # only the first time, please
    if "query_params" not in st.session_state:
      st.session_state.query_params = st.query_params.to_dict()

def _get_argvs() -> Dict[str, str]:
    result = {}
    # range of sys.argv starts from 1 step by 2
    for i in range(2, len(sys.argv), 2):
        result[sys.argv[i - 1][2:]] = str(sys.argv[i])
    return result


def get_params() -> Dict[str, str]:
    """
    Returns the query parameters merged with the command line arguments.
    So,
    - in desktop dev test => use commande line arguments
    - in cloud => use query parameters (override the command line arguments)
    :return: Dict[str, str]
    """
    params = _get_argvs()
    params.update(st.session_state.query_params)
    return params

def get_param(key: str) -> str:
    params = get_params()
    if key in params:
        return params[key]
    else:
        return ""

def is_admin() -> bool:
    return False
