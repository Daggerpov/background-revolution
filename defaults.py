def write_default_settings():
    with open("Settings.txt", "w") as settings_file:
        settings_file.write("""do_not_show: False\n
        first_theme: True\n
        second_theme: False\n
        third_theme: False\n""")

    do_not_show = False

    themes = {"first_theme": True, "second_theme": False, "third_theme": False}

    return do_not_show, themes