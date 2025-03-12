# styles.py

light_theme = {
    "background": "#FFFFFF",
    "text": "#000000",
    "graph_bg": "#F5F5F5",
    "graph_text": "#000000",
    "font": "Arial, sans-serif"
}

dark_theme = {
    "background": "#2C2C2C",  # Charcoal for a softer dark mode
    "text": "#E0E0E0",
    "graph_bg": "#3A3A3A",
    "graph_text": "#FFFFFF",
    "font": "Arial, sans-serif"
}

# ✅ Move global page styles here
def get_global_styles(selected_theme):
    theme = dark_theme if selected_theme == "dark" else light_theme
    return {
        "backgroundColor": theme["background"],
        "color": theme["text"],
        "height": "100vh",
        "width": "100vw",
        "fontFamily": theme["font"],
        "padding": "20px",
        "transition": "background-color 0.5s ease"
    }
