import streamlit as st
import time

st.set_page_config(page_title="Streamlit Basics",page_icon="tada", layout="wide")

st.title("Streamlit basics")
st.caption("A tiny tour of the widgets and patterns used in project")

section = st.sidebar.radio("Section",[
    "1. Text & Layout",
    "2. Widgets & Reruns",
    "3. Session state",
    "4. Chat UI Preview"
])

if section=="1. Text & Layout":
    st.header("Text & Layout")
    st.markdown(
        """
        **'st.write'** is the Swiss-army knife – it renders strings, numbers,
        lists, dicts, and even DataFrames.

        **'st.markdown'** accepts GitHub-flavoured markdown (bold, links, lists).

        **'st.columns'** splits the page horizontally so you can place widgets
        side by side.
        """
    )
    st.write("Hello World")
    
    left, right = st.columns(2)

    with left:
        st.metric(label="Token used", value=128, delta=12)

    with right:
        st.info("st.info / st.success / st.warning / st.error")
        st.success("st.info / st.success / st.warning / st.error")
        st.warning("st.info / st.success / st.warning / st.error")
        st.error("st.info / st.success / st.warning / st.error")
        
    st.divider()
    st.subheader("Code")
    st.code(
    """
    'st.write("Hello World!")',
    """,language="python"
    )
    
elif section == "2. Widgets & Reruns":
    st.header("Widgets and Rerun")
    st.markdown(
    """
    Widgets return the user's current choice/input on the current run.
    """
    )
    name = st.text_input(label="Enter your name", placeholder="Type your name here")
    mood = st.selectbox(label="Your mood", options=["Happy","Sad","Ambivalent"])
    slider = st.slider(label="Enthusiasm",max_value=100,min_value=1,value=50)
    
    st.divider()
    
    if st.button("Say Hello"):
        st.success(f"Hello {name}! You are {mood} and your enthusiasm is {slider}.")
        
    counter=0
    if st.button("Increment"):
        counter+=1
        st.write(f"Counter: {counter}")
        
elif section == "3. Session state":
    st.header("Session state")
    st.markdown(
        """
        Session state allows you to store values that persist across runs.
        """
    )

    if "click_count" not in st.session_state:
        st.session_state.click_count = 0
        
    if "note" not in st.session_state:
        st.session_state.note=[]

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        if st.button("Click me"):
            st.session_state.click_count += 1

    with col_b:
        if st.button("Reset"):
            st.session_state.click_count = 0

    with col_c:
        st.metric(
            label="Click count",
            value=st.session_state.click_count
        )
        
    note = st.text_input(label="Note",placeholder="Add a note here...")
    
    if st.button("Save note") and note.strip():
        st.session_state.note.append(note.strip())
        note=""

    if st.session_state.note:
        st.subheader("Notes")
        for item in st.session_state.note:
            st.write(item)
    else:
        st.info("No notes yet. Add a note to get started")
        
elif section == "4. Chat UI Preview":
    st.header("Chat UI Preview")
    st.markdown("This is the preview of the chat UI")
    
    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []
    
    for entry in st.session_state.chat_log:
        with st.chat_message(entry["role"]):
            st.write(entry["content"])

    prompt = st.chat_input("Try asking me anything...")

    if prompt:
        st.session_state.chat_log.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                time.sleep(2)
                st.write("Dummy response")

                st.session_state.chat_log.append(
                    {"role": "assistant", "content": "Dummy response"}
                )