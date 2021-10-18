import streamlit as st

def summarize_output(filename, output):
    title = filename
    text = output
    keywords = "main keywords, keyword1, keyword 2, keyword 3"
    return title,text,keywords

def format_output(title, output):

    keywords_temp_open = """
    <div style = "background-color:Lightblue">
    <p style="padding: 5px; border: 1px Lightblue; color:black;line-height: 2;font-size: 1rem;font-weight: bold;width: 651px;margin: 9px auto 2px;padding-top:15px;padding-bottom:15px">
    """
    keywords_temp_close = """
    </p>
    </div>
    """
    text_temp_open = """
    <div style = "background-color:Lightblue">
    <p style="padding: 10px; border: 2px Lightblue; color:black;line-height: 2;font-size: 1rem;width: 651px;margin: 9px auto 2px;padding-top:15px;padding-bottom:15px">
    """
    text_temp_close = """
    </p>
    </div>
    """
    # if st.button("Summarize"):
    title,text,keywords = summarize_output(title, output)
    st.header("Output - Summarized Text")
    keywords = keywords_temp_open + "Keywords : " + keywords + keywords_temp_close
    #st.markdown(keywords, unsafe_allow_html=True)
    text = text_temp_open + text + text_temp_close
    st.markdown(text, unsafe_allow_html=True)
