import streamlit as st
from Weather_Agent.prompts import build_greeting_prompt, build_system_prompt
from Weather_Agent.client import get_client_and_model
from Weather_Agent.agent import run_agent_turns

with st.sidebar:
    st.header("About this project")
    st.markdown(build_greeting_prompt())
    
    st.divider()
    
    st.subheader("Provider")
    try:
        _client, model, provider = get_client_and_model()
        st.success(f"Provider: {provider.name} (model: {model}).")
    except RuntimeError as e:
        st.error("Something went wrong")
        
    st.divider()
    
    st.subheader("Jinja System Prompt")
    st.caption("The system propmt is the prompt that the agent will use to answer the question.")
    
    with st.expander("Preview rendered prompt", expanded=False):
        st.code(build_system_prompt(),language="markdown")
        
    if st.button("Clear chat"):
        st.session_state.chat_log = []
        st.rerun()    
    
st.title("Weather Agent")

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
    
for entry in st.session_state.chat_log:
    if entry.get("content"):
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])
            
prompt = st.chat_input("Ask the agent about the weather information")

if prompt:
    st.session_state.chat_log.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.write(prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = run_agent_turns(st.session_state.chat_log)
            except Exception as e:
                st.error("Something went wrong")
                answer = str(e)
                
            st.write(answer)
            # st.session_state.chat_log.append({"role":"assistant","content":answer})