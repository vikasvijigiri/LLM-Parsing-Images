import streamlit as st
from typing import Any, Callable, Dict, Optional
import json
import time
import traceback
import uuid          # ✅ ADD THIS
import time

class StreamlitUI:
    """A powerful reusable Streamlit UI utility manager."""

    # --------------------------------------------------------------
    # INIT
    # --------------------------------------------------------------
    def __init__(self):
        st.markdown(self._global_css(), unsafe_allow_html=True)
        st.set_page_config(
            page_title="JPG Document Processor",
            page_icon="🖼️",
            layout="wide"
        )
        #st.title("🖼️ JPG Image Processor", width="stretch")


    # ---------- BASIC TEXT ELEMENTS ----------
    def title(self, text: str, center: bool = True):
        # CSS override for Streamlit title
        st.markdown("""
        <style>
            .custom-title {
                font-size: 2rem;
                font-weight: 700;
                color: red;
                padding: 0.4rem 0;
            }
        </style>
        """, unsafe_allow_html=True)

        if center:
            st.markdown(
                f"<h1 class='custom-title' style='text-align:center; color:red; font-size:70px'>{text}</h1>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<h1 class='custom-title'>{text}</h1>",
                unsafe_allow_html=True
            )


    def subtitle(self, text: str, center: bool = True):
        # CSS for subtitle/tagline
        st.markdown("""
        <style>
            .custom-subtitle {
                font-size: 1.2rem;
                font-weight: 400;
                color: #555;
                margin-top: -20px;
                margin-bottom: 10px;
            }
        </style>
        """, unsafe_allow_html=True)

        if center:
            st.markdown(
                f"<p class='custom-subtitle' style='text-align:center;'>{text}</p>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<p class='custom-subtitle'>{text}</p>",
                unsafe_allow_html=True
            )



    def header(self, text: str):
        st.header(text)

    def subheader(self, text: str):
        st.subheader(text)

    def section_title(self, text: str):
        """Industry-style section header."""
        st.markdown(f"### {text}")

    def select(self, label: str, options: list, index=0):
        """Unified dropdown/select wrapper."""
        return st.selectbox(label, options, index=index)

    # --------------------------------------------------------------
    # GLOBAL CSS (UI Enhancement)
    # --------------------------------------------------------------
    def _global_css(self):
        return """
        <style>
            /* Fancy Gradient Button */
            .fancy-btn button {
                background: linear-gradient(90deg, #4A90E2, #9013FE) !important;
                color: white !important;
                padding: 12px 20px !important;
                border-radius: 10px !important;
                font-weight: 600 !important;
                border: none !important;
                margin: 6px 0 !important;
                cursor: pointer;
                transition: 0.2s;
            }
            .fancy-btn button:hover {
                transform: translateY(-3px);
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            }

            /* Slide Button Animation */
            @keyframes slideDown {
                from { transform: translateY(-20px); opacity: 0; }
                to   { transform: translateY(0);     opacity: 1; }
            }
            .slide-anim {
                animation: slideDown 0.35s ease-out;
            }

            /* Card */
            .card {
                padding: 15px;
                border-radius: 12px;
                margin-top: 10px;
                background: #f7f7f9;
                border: 1px solid #ddd;
            }

            /* Score Box */
            .score-box {
                border-radius: 10px;
                padding: 12px;
                margin-bottom: 8px;
                color: white;
                font-weight: 600;
            }

            /* Modal Overlay */
            .modal-background {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.6);
                z-index: 9999;
            }
        </style>
        """



    def run_with_stopwatch(self, func, *args, **kwargs):
        """
        Runs func(*args, **kwargs) while displaying a stylish live stopwatch.
        Returns: result
        """

        # UI placeholder for stopwatch
        timer_placeholder = st.empty()

        # Start time
        start = time.time()

        # Flag to know when function is done
        finished = False
        result = None
        exception_raised = None

        # Run function in a controlled block
        while not finished:
            elapsed = time.time() - start

            # # ---- BEAUTIFUL TIMER UI ----
            # timer_placeholder.markdown(
            #     f"""
            #     <div style="
            #         font-size: 42px;
            #         font-weight: 800;
            #         color: #00b4d8;
            #         text-align: center;
            #         padding: 12px 0;
            #         background: rgba(0,180,216,0.08);
            #         border-radius: 12px;
            #         border: 2px solid rgba(0,180,216,0.35);
            #         margin-bottom: 10px;
            #     ">
            #         ⏱ {elapsed:.2f} sec
            #     </div>
            #     """,
            #     unsafe_allow_html=True
            # )

            # Try executing only once, not repeatedly
            if result is None and exception_raised is None:
                try:
                    result = func(*args, **kwargs)
                    finished = True
                except Exception as e:
                    exception_raised = e
                    finished = True

            time.sleep(0.01)

        # If function failed, raise error
        if exception_raised:
            raise exception_raised

        # Final elapsed time
        final_elapsed = time.time() - start

        # ---- Final Timer Display ----
        timer_placeholder.markdown(
            f"""
            <div style="
                font-size: 22px;
                font-weight: 500;
                color: white;
                background: linear-gradient(90deg, #0096c7, #48cae4);
                padding: 15px 0;
                border-radius: 12px;
                text-align: center;
                margin-top: 8px;
            ">
                ⏱ Finished in {final_elapsed:.2f} sec
            </div>
            """,
            unsafe_allow_html=True
        )

        return result



    # --------------------------------------------------------------
    # FANCY BUTTON (NOW ACTUALLY USING CSS)
    # --------------------------------------------------------------
    def button(self, label: str, key: Optional[str] = None):
        # 1. Inject CSS for all buttons
        st.markdown("""
            <style>
            div.stButton > button {
                background-color: #4CAF50; /* Green */
                color: white;
                padding: 10px 24px;
                border-radius: 12px;
                border: 2px solid #4CAF50;
                font-size: 16px;
                font-weight: 600;
                transition-duration: 0.4s;
            }
            div.stButton > button:hover {
                background-color: white;
                color: #4CAF50;
                border: 2px solid #4CAF50;
                transform: scale(1.02);
            }
            </style>
        """, unsafe_allow_html=True)

        # 2. Key Handling
        # We prefer deterministic keys (based on label) so the button works on reload
        if key is None:
            key = label

        return st.button(label, key=key)



    # --------------------------------------------------------------
    # SLIDING ANIMATED BUTTON
    # --------------------------------------------------------------
    def sliding_button(self, label: str, key: Optional[str] = None):
        placeholder = st.empty()
        with placeholder:
            st.markdown(f"<div class='slide-anim'>", unsafe_allow_html=True)
            clicked = st.button(label, key=key)
            st.markdown(f"</div>", unsafe_allow_html=True)
        return clicked




    # ---------- LAYOUT ----------
    def center_selectbox(self, label: str, options: list):
        col1, col2, col3 = st.columns([1, 2, 1])
        return col2.selectbox(label, options)


    def sidebar_nav(self):
        # Initialize menu state
        if "active_page" not in st.session_state:
            st.session_state.active_page = "Upload & Process"

        st.sidebar.markdown("## 📍 Navigation")

        # Menu items
        menu_items = {
            "Upload & Process": "📤 Upload & Process",
            "Dashboard": "📊 Dashboard",
        }

        # Small CSS to style the menu
        st.sidebar.markdown("""
            <style>
                .menu-btn {
                    width: 100%;
                    padding: 10px 14px;
                    border-radius: 8px;
                    border: 1px solid #E3E3E3;
                    background-color: #F8F8F8;
                    text-align: left;
                    font-size: 16px;
                    margin-bottom: 8px;
                    cursor: pointer;
                }
                .menu-btn:hover {
                    background-color: #EFEFEF;
                }
                .menu-btn-active {
                    background-color: #4b8df8 !important;
                    color: white !important;
                    border-color: #4b8df8 !important;
                }
            </style>
        """, unsafe_allow_html=True)

        # Build menu buttons
        for key, label in menu_items.items():
            active_class = "menu-btn-active" if st.session_state.active_page == key else "menu-btn"

            if st.sidebar.button(label, key=key, help=f"Go to {key}", use_container_width=True):
                st.session_state.active_page = key
                st.rerun()

            # Apply styling by injecting CSS dynamically
            st.sidebar.markdown(
                f"<script>var btn = window.parent.document.querySelector('button[k='{key}']'); if (btn) {{ btn.className = '{active_class}'; }} </script>",
                unsafe_allow_html=True
            )

        st.sidebar.markdown("---")
        st.sidebar.caption("Version 1.0 • Ngenux")

        return st.session_state.active_page


    def divider(self):
        st.divider()

    # ---------- STATUS ----------
    def info(self, msg: str):
        st.info(msg)

    def warning(self, msg: str):
        st.warning(msg)

    def success(self, msg: str):
        st.success(msg)

    def error(self, msg: str):
        st.error(msg)




    # --------------------------------------------------------------
    # GRADIENT SCORE BOX
    # --------------------------------------------------------------
    def score_box(self, text: str, score: float):
        score = max(0, min(1, score))
        r = int((1 - score) * 255)
        g = int(score * 255)
        b = 90

        st.markdown(
            f"""
            <div class="score-box" style="background: rgb({r},{g},{b});">
                {text}
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------------
    # NOTIFICATIONS
    # --------------------------------------------------------------
    def success(self, msg: str): st.success(msg)
    def error(self, msg: str): st.error(msg)
    def warning(self, msg: str): st.warning(msg)
    def info(self, msg: str): st.info(msg)

    # --------------------------------------------------------------
    # CUSTOM ERROR HANDLER
    # --------------------------------------------------------------
    def try_run(self, func: Callable, message: str = "Something went wrong"):
        try:
            return func()
        except Exception as e:
            st.error(f"{message}: {e}")
            st.code(traceback.format_exc())
            return None

    # --------------------------------------------------------------
    # SPINNER FOR TASKS
    # --------------------------------------------------------------
    def run_with_spinner(self, label: str, func: Callable, *args, **kwargs):
        with st.spinner(label):
            return func(*args, **kwargs)

    # --------------------------------------------------------------
    # COLLAPSIBLE SECTION
    # --------------------------------------------------------------
    def collapsible(self, label: str, content_func: Callable):
        with st.expander(label):
            content_func()

    # --------------------------------------------------------------
    # JSON HELPERS (ADDED)
    # --------------------------------------------------------------
    def pretty_json(self, data: Any):
        return json.dumps(data, indent=4, ensure_ascii=False)

    def load_json(self, text: str):
        try:
            return json.loads(text)
        except:
            st.error("❌ Invalid JSON format")
            return None

    def json_area(self, label: str, data: Any, height=200):
        pretty = self.pretty_json(data)
        return st.text_area(label, pretty, height=height)

    def json_viewer(self, obj: Any):
        st.json(obj)

    def save_json(self, obj: Dict, filename="data.json"):
        st.download_button("Download JSON", self.pretty_json(obj), filename)

    # -----------------------------
    # Minimal helper (keeps structure, clears primitives)
    # -----------------------------
    def clear_json_values(self, data: Any):
        """Recursively replace primitive values with empty strings while preserving structure."""
        if isinstance(data, dict):
            return {k: self.clear_json_values(v) for k, v in data.items()}
        if isinstance(data, list):
            return [self.clear_json_values(v) for v in data]
        return ""



    # --------------------------------------------------------------
    # CODE BLOCK
    # --------------------------------------------------------------
    def code_block(self, code: str, lang: str = "python"):
        st.code(code, language=lang)

    # --------------------------------------------------------------
    # FILE UPLOAD
    # --------------------------------------------------------------
    def file_uploader(self, label: str, types=None, accept_multiple_files: bool = True):
        """Wrapper for Streamlit file uploader with optional multiple files."""
        return st.file_uploader(label, type=types, accept_multiple_files=accept_multiple_files)


    # --------------------------------------------------------------
    # DATAFRAME
    # --------------------------------------------------------------
    def show_df(self, df, use_container=True):
        st.dataframe(df, use_container_width=use_container)

    # --------------------------------------------------------------
    # CARD
    # --------------------------------------------------------------
    def card(self, content: str):
        st.markdown(f"<div class='card'>{content}</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------
    # PROGRESS BAR
    # --------------------------------------------------------------
    def progress(self, label: str, steps=10, delay=0.1):
        st.write(label)
        p = st.progress(0)
        for i in range(steps):
            time.sleep(delay)
            p.progress((i + 1) / steps)

    # --------------------------------------------------------------
    # MODAL POPUP
    # --------------------------------------------------------------
    def modal(self, content: str):
        st.markdown(
            f"""
            <div class="modal-background">
                <div class="card" style="max-width: 420px; margin: 120px auto; background: white;">
                    {content}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------------
    # SESSION STATE
    # --------------------------------------------------------------
    def get_state(self, key: str, default: Any = None):
        if key not in st.session_state:
            st.session_state[key] = default
        return st.session_state[key]

    def set_state(self, key: str, value: Any):
        st.session_state[key] = value

    # --------------------------------------------------------------
    # INPUT VALIDATION
    # --------------------------------------------------------------
    def validate_non_empty(self, label: str, text: str):
        if not text.strip():
            st.error(f"{label} cannot be empty.")
            return False
        return True

    # --------------------------------------------------------------
    # SPACERS & DIVIDERS
    # --------------------------------------------------------------
    def spacer(self, height: int = 10):
        st.write(f"<div style='height:{height}px'></div>", unsafe_allow_html=True)

    def divider(self):
        st.markdown("---")

    # --------------------------------------------------------------
    # DYNAMIC SECTIONS
    # --------------------------------------------------------------
    def dynamic_section(self, title, func: Callable):
        st.subheader(title)
        func()
        st.markdown("---")

    # --------------------------------------------------------------
    # ANIMATED CONTENT SWAP
    # --------------------------------------------------------------
    def animate_replace(self, placeholder, html_text):
        placeholder.markdown(
            f"<div class='slide-anim'>{html_text}</div>",
            unsafe_allow_html=True
        )
