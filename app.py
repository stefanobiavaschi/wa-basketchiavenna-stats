import streamlit as st
import pandas as pd
from PIL import Image

from lib.func_data import import_data, sec_to_time, avg_perc, set_bg_hack, header
from lib.func_page import singola, home, aggregato


def main():
    st.set_page_config(
        page_title="Stats Basket Chiavenna",
        page_icon="📈",
        layout="wide"
    )
    
    titleimg = r'file/background.jpg'
    bg_ext = "jpg"
    # set_bg_hack(titleimg, bg_ext)

    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header{visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
        <style>
        /* Hide the link button */
        .stApp a:first-child {
            display: none;
        }
        
        .css-15zrgzn {display: none}
        .css-eczf16 {display: none}
        .css-jn99sy {display: none}
        </style>
        """, unsafe_allow_html=True)
    st.markdown(r"""
        <style>
            .st-emotion-cache-z5fcl4 {
        width: 100%;
        padding: 1rem 1rem 10rem;
        min-width: auto;
        max-width: initial;
    }
        </style>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        r"""
        <style>
        .stDeployButton {
                visibility: hidden;
            }
        
        """, unsafe_allow_html=True
    )

    st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

    header()
        


    # Definizione delle pagine
    pages = {
        "home": home,
        "singola": singola,
        "aggregato": aggregato,
    }

    # Inizializzazione della sessione
    if "page" not in st.session_state:
        st.session_state.page = "home"

    # Esegui la pagina corrispondente
    pages[st.session_state.page]()



if __name__ == "__main__":
    main()