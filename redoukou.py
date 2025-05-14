import streamlit as st
import re

st.set_page_config(layout="wide")
st.title("読み替え補助ツール")

# カスタムCSS（余白詰め）
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
    </style>
""", unsafe_allow_html=True)

# カラム構成
left_col, center_col, right_col = st.columns([2, 0.4, 2])

with left_col:
    st.markdown('<div class="custom-label">読み替え対象</div>', unsafe_allow_html=True)
    source_text = st.text_area(label="", key="source", height=200)

    # 空行（マージン調整）
    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)

    st.markdown('<div class="custom-label">読み替え指示</div>', unsafe_allow_html=True)
    rewrite_instructions = st.text_area(label="", key="instruction", height=200)

with center_col:
    st.write("")
    run_button = st.button("▶ 読み替えを実行")
    show_comparison = st.toggle("原文と比較")
    # ✅ 入力クリアボタン（読み替え対象・指示を空にする）
    if st.button(" 入力をクリア"):
        st.session_state["source"] = ""
        st.session_state["instruction"] = ""
        st.experimental_rerun()

def apply_replacements_safe(text, instructions, show_diff=False):
    # 1. 指示文をパース（ネストに対応）
    pattern = r'「(.*?)」とあるのは「((?:[^「」]|「[^」]*」)*?)」と'
    matches = re.findall(pattern, instructions)

    # 2. 一時置換トークン生成
    tmp_map = {}
    for i, (original, replacement) in enumerate(matches):
        token = f"__TMP{i}__"
        text = re.sub(re.escape(original), token, text)
        tmp_map[token] = (original, replacement)

    # 3. トークンを最終形に置き換え
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
        st.markdown(f"<div style='white-space: pre-wrap; font-size: 16px'>{result}</div>", unsafe_allow_html=True)
