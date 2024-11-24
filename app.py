import os
import streamlit as st
from streamlit_navigation_bar import st_navbar
import pages as pg

st.set_page_config(page_title="Classicape",page_icon="⛰️", initial_sidebar_state="collapsed")

pages = ["Live Camera", "Upload Image", "Help", "GitHub"]
parent_dir = os.path.dirname(os.path.abspath(__file__))
urls = {"GitHub": "https://github.com/traviszusa/Landscape-Image-Classification"}
styles = {
    "nav": {
        "background-color": "#0F1116",
        "justify-content": "left",
    },
    "img": {
        "padding-right": "14px",
        "padding-left": "5px",
    },
    "span": {
        "color": "#e4e3ef",
        "padding": "14px",
    },
    "active": {
        "background-color": "#a4aa64",
        "color": "var(--text-color)",
        "font-weight": "bold",
        "padding": "14px",
    },
    "hover": {
        "background-color": "#a4aa64",
        "color": "var(--text-color)",
        "font-weight": "normal",
        "padding": "14px",
    },
    "ul": {
        "justify-content": "flex-start",
    }
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

page = st_navbar(
    pages,
    logo_path="./resources/images/logo.svg",
    urls=urls,
    styles=styles,
    options=options,
)

functions = {
    "Home": pg.show_home,
    "Live Camera": pg.show_camera,
    "Upload Image": pg.show_upload,
    "Help": pg.show_help,
}

go_to = functions.get(page)
if go_to:
    go_to()