import streamlit as st
from string import Template

from generater import generate_structured_json
from sender import create_post

st.set_page_config(page_title="Prompt Builder App")
st.title("Prompt Builder App")

with st.sidebar:
    model = st.text_input("Model", value="gpt-4o-mini")
    is_post = st.checkbox("Is post?")

AI_NAME = st.text_input("AI Name", value="Predis.ai")
AI_OFFICIAL_LINK = st.text_input("Official Link", value="http://predis.ai")
PRICING_LINK = st.text_input("Pricing Link", value="http://predis.ai/pricing")
DEMO_LINK = st.text_input("Demo link", value="https://www.youtube.com/watch?v=Yqv_KOb9dvk")

st.divider()

prompt_template = st.text_area("Prompt Template")
schema_json = st.text_area("Schema JSON")

def main():
    template = Template(prompt_template) 

    prompt = template.safe_substitute(
        AI_NAME=AI_NAME,
        AI_OFFICIAL_LINK=AI_OFFICIAL_LINK,
        PRICING_LINK=PRICING_LINK,
        DEMO_LINK=DEMO_LINK,
        )
    
    data = generate_structured_json(prompt)

    if data:
        st.divider()
        st.json(data)
    
    if is_post: create_post(data)

if st.button("Run"):
    main()