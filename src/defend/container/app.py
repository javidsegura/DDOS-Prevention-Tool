import streamlit as st

def main():
    # Set page config
    st.set_page_config(page_title="The History of C",
                       layout="centered",
                       page_icon="https://upload.wikimedia.org/wikipedia/commons/3/35/The_C_Programming_Language_logo.svg")

    # Title of the website
    st.title("The History of C")

    # Description about C
    st.write("""
    C is a powerful general-purpose programming language. It was created in 1972 by Dennis Ritchie 
    at Bell Labs and has been widely used for systems programming, embedded systems, and application 
    development. C serves as the foundation for many modern languages, including C++, Java, and Python.
    """)

    # Embed a video (replace with your own hosted video URL if needed)
    st.video("https://www.youtube.com/watch?v=de2Hsvxaf8M", format="video/mp4")

if __name__ == "__main__":
    main()
