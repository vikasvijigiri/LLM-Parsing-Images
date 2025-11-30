import streamlit as st
import html
from streamlit.components.v1 import html as st_html

def score_to_gradient(score: float) -> str:
    """
    Convert score (0-1) into a smooth gradient color.
    """
    score = max(0.0, min(1.0, score))  # clamp

    # RGB interpolation
    start = (255, 77, 77)     # red
    mid   = (255, 165, 0)     # orange
    end   = (46, 204, 113)    # green

    # if below 0.5 → red → orange
    if score < 0.5:
        ratio = score / 0.5
        r = int(start[0] + (mid[0] - start[0]) * ratio)
        g = int(start[1] + (mid[1] - start[1]) * ratio)
        b = int(start[2] + (mid[2] - start[2]) * ratio)

    else:
        ratio = (score - 0.5) / 0.5
        r = int(mid[0] + (end[0] - mid[0]) * ratio)
        g = int(mid[1] + (end[1] - mid[1]) * ratio)
        b = int(mid[2] + (end[2] - mid[2]) * ratio)

    return f"rgb({r}, {g}, {b})"


def render_small_box(pred_text: str, score: float):
    """Render a colored box based only on prediction text and score."""
    bg = score_to_gradient(score)

    st.markdown(
        f"""
        <div style="
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 8px;
            background: linear-gradient(90deg, {bg}, #ffffff);
            border: 1px solid #ccc;
            font-size: 14px;
            font-weight: 500;
        ">
            {pred_text}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_results(result_dict: dict):
    """Render results grouped by dotted keys with safe error handling."""

    if not isinstance(result_dict, dict):
        st.error("Invalid result format: Expected a dictionary.")
        return

    grouped = {}

    # -------------------------
    # Group keys by hierarchy
    # -------------------------
    for key, val in result_dict.items():

        try:
            if not isinstance(key, str):
                raise ValueError(f"Key is not a string: {key}")

            parts = key.split(".")
            section = parts[0]
            subkey = ".".join(parts[1:]) if len(parts) > 1 else None

            if section not in grouped:
                grouped[section] = {}

            if subkey:
                grouped[section][subkey] = val
            else:
                grouped[section]["_self"] = val

        except Exception as e:
            st.warning(f"Skipping malformed entry: {key}. Error: {e}")
            continue

    # -------------------------
    # Render grouped output
    # -------------------------
    for section, items in grouped.items():

        try:
            # st.markdown(f"## 🔹 {section}")

            for key, info in items.items():

                # Validate info dictionary
                if not isinstance(info, dict):
                    st.warning(f"Invalid entry under '{section}.{key}'. Expected dict.")
                    continue

                # Extract safely
                text = info.get("gt_text")
                score = info.get("score", 0)

                # Normalize text
                if text is None:
                    text = "❌ No extraction"
                elif not isinstance(text, str):
                    text = str(text)

                # Normalize score
                try:
                    score = float(score)
                except (ValueError, TypeError):
                    score = 0.0

                # # Field label
                # if key == "_self":
                #     field_label = section
                # else:
                #     field_label = key.replace(".", " → ")

                # st.markdown(f"**{field_label}**")

                # Safe rendering of small box
                try:
                    render_small_box(text, score)
                except Exception as e:
                    st.error(f"Error rendering box: {e}")

        except Exception as e:
            st.error(f"Error rendering section '{section}': {e}")
            continue


def render_compact_boxes(result_dict: dict, container_width: int = 800):
    """Render LLM results compactly using Streamlit columns for proper display."""
    
    if not isinstance(result_dict, dict):
        st.error("Invalid result format: Expected a dictionary.")
        return

    # -----------------
    # Prepare entries
    # -----------------
    entries = []
    for key, info in result_dict.items():
        try:
            if not isinstance(info, dict):
                continue
            text = info.get("llm_text") or "❌ No extraction"
            score = float(info.get("score", 0))
            bg = score_to_gradient(score)
            width = max(80, min(len(text) * 7 + 20, 400))  # width proportional to text
            entries.append((text, bg, width))
        except Exception as e:
            st.warning(f"Skipping key '{key}': {e}")
            continue

    # -----------------
    # Render flex-style layout using Streamlit columns
    # -----------------
    # Calculate how many boxes per row
    max_row_width = container_width
    current_width = 0
    row_entries = []

    for text, bg, width in entries:
        if current_width + width > max_row_width:
            # render current row
            cols = st.columns(len(row_entries))
            for c, (t, b, w) in zip(cols, row_entries):
                c.markdown(
                    f"""
                    <div style="
                        padding:6px 10px;
                        border-radius:6px;
                        background:linear-gradient(90deg, {b}, #ffffff);
                        border:1px solid #ccc;
                        font-size:13px;
                        font-weight:500;
                        white-space:nowrap;
                        overflow:hidden;
                        text-overflow:ellipsis;
                        width:{w}px;
                    " title="{t}">
                        {t}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            row_entries = []
            current_width = 0

        row_entries.append((text, bg, width))
        current_width += width + 6  # 6px gap

    # Render remaining row
    if row_entries:
        cols = st.columns(len(row_entries))
        for c, (t, b, w) in zip(cols, row_entries):
            c.markdown(
                f"""
                <div style="
                    padding:6px 10px;
                    border-radius:6px;
                    background:linear-gradient(90deg, {b}, #ffffff);
                    border:1px solid #ccc;
                    font-size:13px;
                    font-weight:500;
                    white-space:nowrap;
                    overflow:hidden;
                    text-overflow:ellipsis;
                    width:{w}px;
                " title="{t}">
                    {t}
                </div>
                """,
                unsafe_allow_html=True
            )





def render_boxes_component(result_dict: dict, container_width: int = 900, max_box_width: int = 300):
    """Render LLM results as colored boxes safely using st.components.v1.html"""
    
    if not isinstance(result_dict, dict):
        st.error("Invalid result format: Expected a dictionary.")
        return
    
    box_html_list = []
    for key, info in result_dict.items():
        try:
            if not isinstance(info, dict):
                continue
            text = info.get("gt_text")
            score = float(info.get("score", 1))
            bg = score_to_gradient(score)
            safe_text = html.escape(text)

            box_html_list.append(f"""
                <div style="
                    display:inline-block;
                    padding:8px 12px;
                    margin:5px;
                    border-radius:8px;
                    background:linear-gradient(90deg, {bg}, #ffffff);
                    border:1px solid #ccc;
                    font-size:13px;
                    font-weight:500;
                    max-width:220px;           /* max auto width */
                    white-space:normal;        /* allow wrapping */
                    word-wrap:break-word;      /* break long words */
                    overflow:hidden;
                    box-sizing:border-box;
                " title="{safe_text}">
                    {safe_text}
                </div>
            """)
        except Exception as e:
            st.warning(f"Skipping key '{key}': {e}")
            continue

    final_html = f"""
    <style>
        /* Container fits Streamlit column width */
        .box-container {{
            width: 100%;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: flex-start;
            justify-content: flex-start;
        }}

        /* Each colored box */
        .field-box {{
            padding: 6px 10px;
            border-radius: 6px;
            border: 1px solid #ccc;
            font-size: 13px;
            font-weight: 500;
            white-space: normal;          /* Allow wrapping */
            overflow-wrap: break-word;     /* Wrap long text */
            box-sizing: border-box;
            max-width: calc(33% - 8px);    /* Keep 3 boxes per row */
            min-width: 120px;
        }}

        /* Tablet */
        @media (max-width: 1100px) {{
            .field-box {{
                max-width: calc(50% - 8px);    /* 2 per row */
            }}
        }}

        /* Mobile */
        @media (max-width: 700px) {{
            .field-box {{
                max-width: 100%;               /* 1 per row */
            }}
        }}
    </style>

    <div class="box-container">
        {''.join(box_html_list).replace('<div style=', '<div class="field-box" style=')}
    </div>
    """


    # Use st.components.v1.html to render HTML safely
    st_html(final_html, height=1000)