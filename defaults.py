import json

def write_default_settings():
    with open("settings.json", "w") as settings_file:
        json.dump('''
        {
    "do_not_show": "False",
    "themes": [
        {
            "first_theme": "True", 
            "second_theme": "False",
            "third_theme": "False"
        }
    ],
    "color_palettes": [
        {
            "darker_than_primary_button": "#0f893b",
            "darker_than_text_button": "#9cb19c",
            "main_background": "#66aff5",
            "primary_button_background": "#13ae4b",
            "selection_frame_background": "#c4dc34",
            "text_button_background": "#e5efde"
        },
        {
            "darker_than_primary_button": "#6c5b7b",
            "darker_than_text_button": "#f89c8f",
            "main_background": "#355c7d",
            "primary_button_background": "#c06c84",
            "selection_frame_background": "#f67280",
            "text_button_background": "#f8b195"
        },
        {
            "darker_than_primary_button": "#ccadb2",
            "darker_than_text_button": "#57838d",
            "main_background": "#445a67",
            "primary_button_background": "#f3bfb3",
            "selection_frame_background": "#84969c",
            "text_button_background": "#b4c9c7"
        }
    ]
}''', settings_file)