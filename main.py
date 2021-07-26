import os, sys, ctypes

import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import time

# determining OS of user
# ratio is to compensate for text size differential between Windows and macOS
# every text attribute's font size should be preceded by int(ratio * {font size})

if sys.platform == "win32":
    win, mac = True, False
    ratio = 1
elif sys.platform == "darwin":
    from appscript import app, mactypes

    win, mac = False, True
    ratio = 1.375
else:
    exit()

# initializing module
root = tk.Tk()
# root.withdraw()
current_window = None

screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")

# assuming 768p is the smallest screen sizes people will have that are using this app,
# here we're making the text bigger for anyone using a size bigger such as 1080p.
if screen_height != 1024:
    ratio *= 1.4

# makes app fullscreen, but no way to exit from within it, need to alt-tab out or use keyboard shortcut
# root.attributes('-fullscreen', True)


def main():
    # setting the current screen to start menu
    #app = main_screen(root)

    main_screen(root)
    # overall GUI loop which will run constantly, accepting input and such
    root.mainloop()


def create_window(self, master, extra=""):
    current_window = tk.Toplevel(master)

    current_window.title(f"Background Revolution{extra}")
    self.canvas = tk.Canvas(
        current_window, width=screen_width, height=screen_height, bg="#66AFF5"
    )
    self.canvas.pack()
    current_window.config(bg="#66AFF5")
    current_window.resizable(width=False, height=False)

    # if the user kills the window via the window manager,
    # exit the application.
    # current_window.wm_protocol("WM_DELETE_WINDOW", root.destroy)
    
    return current_window


class main_screen:
    def __init__(self, master):
        self.master = create_window(self, master)

        self.title_frame = tk.Frame(self.master, bg="#13ae4b", bd=5)
        self.title_frame.place(
            relx=0.4, rely=0.025, relwidth=0.75, relheight=0.15, anchor="n"
        )

        self.title_label = tk.Label(
            self.title_frame,
            text="Background Revolution",
            font=("Courier", int(38 * ratio)),
        )
        self.title_label.place(relwidth=1, relheight=1)

        self.settings_frame = tk.Frame(
            self.master, highlightcolor="#13ae4b", bd=5, bg="#13ae4b"
        )
        self.settings_frame.place(relwidth=0.175, relheight=0.85, rely=0.075, relx=0.8)

        self.settings_pic = tk.PhotoImage(file="./images/settings_icon.png")
        # self.settings_pic_new = self.submit_pic.subsample(2, 2)

        self.settings_pic_button = tk.Button(
            self.settings_frame,
            image=self.settings_pic,
            bg="#e5efde",
            command=lambda: main_screen.go_settings_screen(self),
        )
        self.settings_pic_button.place(relx=0, relheight=1, relwidth=1)

    def go_custom_screen(self):
        self.custom_screen_current = tk.Toplevel(self.master)
        self.app = custom_screen(self.custom_screen_current)

    def go_preset_screen(self):
        self.preset_screen_current = tk.Toplevel(self.master)
        self.app = preset_screen(self.preset_screen_current)

    def go_search_screen(self):
        self.search_screen_current = tk.Toplevel(self.master)
        self.app = search_screen(self.search_screen_current)

    def go_manage_screen(self):
        self.manage_screen_current = tk.Toplevel(self.master)
        self.app = manage_screen(self.manage_screen_current)

    def go_schedule_screen(self):
        self.schedule_screen_current = tk.Toplevel(self.master)
        self.app = schedule_screen(self.schedule_screen_current)

    def go_settings_screen(self):
        self.master.destroy()
        settings_screen(root)


class custom_screen:
    def __init__(self, master):
        self.master = create_window(self, master, '- Custom Collections')

        # fitting the output
        self.preview_frame = tk.Frame(
            self.master, highlightcolor="#13ae4b", bd=10, bg="#13ae4b"
        )
        self.preview_frame.place(
            relx=0.4, rely=0.225, relwidth=0.75, relheight=0.7, anchor="n"
        )

        self.preview_text = tk.Label(
            self.preview_frame,
            text="<Preview Your Image Here>",
            bg="#13ae4b",
            font=("Courier", int(48 * ratio), "bold"),
            fg="#0f893b",
        )
        self.preview_text.place(relx=0.5, rely=0.5, anchor="center")

        # button for file explorer
        # I only want its command to run once, when it's clicked so I made a
        # simple lambda that invokes the info_display function
        self.button = tk.Button(
            self.select_frame,
            text=f"Select Images from {'File Explorer' if win == True else 'Files'}",
            font=("Courier", int(38 * ratio)),
            bg="#e5efde",
            command=lambda: main_screen.retrieve_file(self.preview_frame),
        )
        self.button.place(relx=0, relheight=1, relwidth=1)

        # submit button to accept the file

        self.submit_frame = tk.Frame(
            self.master, highlightcolor="#13ae4b", bd=10, bg="#13ae4b"
        )
        self.submit_frame.place(relwidth=0.175, relheight=0.85, rely=0.075, relx=0.8)

        self.submit_pic = tk.PhotoImage(file="./images/Arrow-Down-Green.png")
        self.submit_pic_new = self.submit_pic.subsample(2, 2)

        self.submit_pic_button = tk.Button(
            self.submit_frame,
            image=self.submit_pic_new,
            bg="#e5efde",
            command=lambda: main_screen.set_background_uploaded(self),
        )
        self.submit_pic_button.place(relx=0, relheight=1, relwidth=1)

    def retrieve_file(preview_frame):
        a = "compatible image files"

        global names_of_files

        if win:
            directory = "/This PC"
        else:
            directory = "/Recents"

        names_of_files = list(
            filedialog.askopenfilenames(
                initialdir=directory,
                title="Select Image Files",
                filetypes=(
                    (a, "*.png"),
                    (a, "*.jpeg"),
                    (a, "*.jpg*"),
                    (a, "*.gif"),
                    (a, "*.tiff"),
                    (a, "*.psd"),
                    (a, "*.eps"),
                    (a, "*.ai"),
                    (a, "*.indd"),
                    (a, "*.raw"),
                ),
            )
        )

        if names_of_files != "":
            background_uploaded = ImageTk.PhotoImage(Image.open(str(names_of_files[0])))
            background_uploaded_label = tk.Label(preview_frame)
            background_uploaded_label.place(relheight=1, relwidth=1)

            background_uploaded_label.configure(image=background_uploaded)
            background_uploaded_label.image = background_uploaded

    def set_background_uploaded(self):
        if win:
            # self.path = os.path.abspath(os.path.dirname(sys.argv[0]))
            ctypes.windll.user32.SystemParametersInfoW(20, 0, names_of_files, 0)
        else:
            app("Finder").desktop_picture.set(mactypes.File(names_of_files))


class preset_screen:
    def __init__(self, master):
        self.master = create_window(self, master, '- Preset Collections')

class search_screen:
    def __init__(self, master):
        self.master = create_window(self, master, ' - Search')


class manage_screen:
    def __init__(self, master):
        self.master = create_window(self, master, ' - Manage Collections')


class schedule_screen:
    def __init__(self, master):
        self.master = create_window(self, master, ' - Schedule Collection Rotations')


class settings_screen:
    def __init__(self, master):
        self.master = create_window(self, master, ' - Settings')


if __name__ == "__main__":
    main()
