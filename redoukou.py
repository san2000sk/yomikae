import streamlit as st
import re

st.set_page_config(layout="wide")
st.title("読み替え補助ツール")

# セッション変数の初期化
for key in ["source", "instruction"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# カスタムCSS
st.markdown("""
    <style>
    .custom-label {
        margin-bottom: 0px;
        font-weight: bold;
        font-size: 16px;
    }
    textarea {
        margin-top: 0px !important;
    }
    div[data-baseweb="textarea"] {
        margin-top: 0px !important;
    }
    div[class^="stTextArea"] {
        padding-top: 0px !important;
        margin-top: 0px !important;
    }
    .select-on-click {
        user-select: all;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# カラム構成
left_col, center_col, right_col = st.columns([2, 0.4, 2])

with left_col:
    st.markdown('<div class="custom-label">読み替え対象</div>', unsafe_allow_html=True)
    source_text = st.text_area(
        label="読み替え対象",
        value=st.session_state["source"],
        key="source_textarea",
        label_visibility="collapsed",
        height=200
    )

    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)

    st.markdown('<div class="custom-label">読み替え指示</div>', unsafe_allow_html=True)
    rewrite_instructions = st.text_area(
        label="読み替え指示",
        value=st.session_state["instruction"],
        key="instruction_textarea",
        label_visibility="collapsed",
        height=200
    )

with center_col:
    st.write("")
    run_button = st.button("▶ 読み替えを実行")
    show_comparison = st.toggle("原文と比較")

    # ✅ 入力クリア：セッション変数を空にしてリロード
    if st.button("🗑 入力をクリア"):
        st.session_state["source"] = ""
        st.session_state["instruction"] = ""
        st.rerun()

def apply_replacements_safe(text, instructions, show_diff=False):
    pattern = r'「(.*?)」とあるのは、?「((?:[^「」]|「[^」]*」)*?)」と'
    matches = re.findall(pattern, instructions)

    tmp_map = {}
    for i, (original, replacement) in enumerate(matches):
        token = f"__TMP{i}__"
        text = re.sub(re.escape(original), token, text)
        tmp_map[token] = (original, replacement)

    for token, (original, replacement) in tmp_map.items():
        if show_diff:
            styled = f"<strong style='color:#800000'>＜{original}／{replacement}＞</strong>"
        else:
            styled = f"<strong style='color:#800000'>{replacement}</strong>"
        text = text.replace(token, styled)

    return text

with right_col:
    if run_button and source_text and rewrite_instructions:
        result = apply_replacements_safe(source_text, rewrite_instructions, show_diff=show_comparison)
        st.markdown("#### 読み替え結果")
        st.markdown(f"<div class='select-on-click' style='white-space: pre-wrap; font-size: 16px'>{result}</div>", unsafe_allow_html=True)

# ✅ 必ずセッションに保存（後で読み込むため）
st.session_state["source"] = source_text
st.session_state["instruction"] = rewrite_instructions
