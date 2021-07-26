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

class PlaceholderEntry(ttk.Entry):
    #initializing the arguments passed in
    def __init__(self, container, placeholder, validation, *args, **kwargs):
        super().__init__(container, *args, style="Placeholder.TEntry", **kwargs)
        self.placeholder = placeholder
        self.insert("0", self.placeholder)
        
        #runs the appropriate method for when the user is focused in/out of the element
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        
        #if this argument is given (like for the instagram password, 
        # then the entry box will hide its text with asterisks)
        self.validation = validation

    
    def _clear_placeholder(self, e):
        #deleting all text placed automatically with the placeholder
        if self["style"] == "Placeholder.TEntry":
            self.delete("0", "end")
            self["style"] = "TEntry"
        
        #editing the property of the entry box 'show' to display asterisks ,
        #instead of any of the entered characters
        if self.validation == 'password':
            self['show'] = "*"
        
    def _add_placeholder(self, e):
        #if there isn't any text entered in AND the user isn't focused in 
        #on this, then it'll add the placeholder
        if not self.get():
            self.insert("0", self.placeholder)
            self["style"] = "Placeholder.TEntry"

def create_window(self, master, extra="", title=('', 0)):
    current_window = tk.Toplevel(master)

    current_window.geometry(f"{screen_width}x{screen_height}+0+0")
    current_window.title(f"Background Revolution{extra}")
    self.canvas = tk.Canvas(
        current_window, width=screen_width, height=screen_height, bg="#66AFF5"
    )
    self.canvas.pack()
    current_window.config(bg="#66AFF5")
    current_window.resizable(width=False, height=False)

    if title != ('', 0):
        self.title_frame = tk.Frame(current_window, bg="#13ae4b", bd=5)
        self.title_frame.place(
            relx=0.5, rely=0.025, relwidth=0.7, relheight=0.15, anchor="n"
        )

        self.title_label = tk.Label(
            self.title_frame,
            text=f"{title[0]}",
            font=("Courier", int(title[1] * ratio)),
        )
        self.title_label.place(relwidth=1, relheight=1)

    self.exit_button = tk.Button(
        current_window, 
        text="Quit", 
        font=("Courier", int(38 * ratio)),
        command=lambda: root.destroy(),
        bg="#13ae4b",
        bd=5)
    self.exit_button.place(relwidth=0.1, relheight=0.15, relx=0.025, rely=0.025)

    # if the user kills the window via the window manager,
    # exit the application.
    current_window.wm_protocol("WM_DELETE_WINDOW", root.destroy)
    
    return current_window

class main_screen:
    def __init__(self, master):
        self.master = create_window(self, master, '', ("Background Revolution", 38))

        self.settings_frame = tk.Frame(
            self.master, bd=5, bg="#13ae4b"
        )
        self.settings_frame.place(relwidth=0.1, relheight=0.15, rely=0.025, relx=0.875)

        self.settings_pic = tk.PhotoImage(file="./images/settings_icon.png")
        # self.settings_pic_new = self.submit_pic.subsample(2, 2)

        self.settings_pic_button = tk.Button(
            self.settings_frame,
            image=self.settings_pic,
            bg="#e5efde",
            command=lambda: main_screen.go_settings_screen(self),
        )
        self.settings_pic_button.place(relx=0, relheight=1, relwidth=1)


    def go_settings_screen(self):
        self.master.destroy()
        settings_screen(root)

    def go_custom_screen(self):
        self.master.destroy()
        custom_screen(root)

    def go_preset_screen(self):
        self.master.destroy()
        preset_screen(root)

    def go_search_screen(self):
        self.master.destroy()
        search_screen(root)

    def go_manage_screen(self):
        self.master.destroy()
        manage_screen(root)

    def go_schedule_screen(self):
        self.master.destroy()
        schedule_screen(root)

class settings_screen:
    def __init__(self, master):
        self.master = create_window(self, master, ' - Settings')




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



if __name__ == "__main__":
    main()
