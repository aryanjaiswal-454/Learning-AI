import streamlit as st

st.set_page_config(page_title="Streamlit Basics",page_icon="tada", layout="wide")

st.title("Streamlit basics")
st.caption("A tiny tour of the widgets and patterns used in project")

section = st.sidebar.radio("Section",[
    "1. Text & Layout",
    "2. Widgets & Reruns",
    "3. Session state",
    "4. Chat UI Preview "
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