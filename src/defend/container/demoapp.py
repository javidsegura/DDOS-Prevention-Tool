import streamlit as st
from resourceController import startDefense

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

    with st.expander("Defense"):
        on = st.toggle("Activate Defense")
        treshold = st.slider("Treshold (%)", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        wait_time = st.slider("Wait Time (s)", min_value=0.0, max_value=30.0, value=15.0, step=0.1)
        if on:
            defense_data = startDefense(treshold=treshold, wait_time=wait_time)
            trafficRecord = defense_data["history"]
            ipCounts = defense_data["ip_counts"]
            ip = defense_data["ip"]
            underAttack = defense_data["under_attack"]
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"Traffic Record: {trafficRecord}")
            with col2:
                st.write(f"IP Counts: {ipCounts}")
            with col3:
                st.write(f"IP: {ip}")
            with col4:
                st.write(f"Under Attack: {underAttack}")

if __name__ == "__main__":
    main()
