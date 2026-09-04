"""Streamlit interface for the KiTE Academic Writing Assistant."""

import streamlit as st

from app import analyze_text, explain_with_gemini


st.set_page_config(page_title="KiTE Writing Assistant", page_icon="K")
st.title("KiTE Academic Writing Assistant")
st.caption("Check sentence structure offline, then request an optional Gemini explanation.")

text = st.text_area(
    "Paste an assignment sentence or paragraph",
    height=180,
    placeholder="Example: Explain the importance of data structures in software engineering.",
)

if st.button("Analyze writing", type="primary"):
    analysis = analyze_text(text)
    st.metric("Words", analysis["word_count"])

    left, right = st.columns(2)
    with left:
        st.subheader("Part-of-speech summary")
        st.json(analysis["pos_counts"])
    with right:
        st.subheader("Basic checks")
        if analysis["issues"]:
            for issue in analysis["issues"]:
                st.warning(issue)
        else:
            st.success("No basic issues found.")

    st.subheader("Token analysis")
    st.dataframe(analysis["tokens"], use_container_width=True, hide_index=True)

    st.subheader("Gemini tutor")
    st.write(explain_with_gemini(text, analysis))
