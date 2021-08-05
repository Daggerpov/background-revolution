import os
import sys
import ctypes

import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import time

# determining OS of user
# ratio is to compensate for text size differential between Windows and macOS
# every text attribute's font size should be preceded by int(RATIO * {font size})

if sys.platform == "win32":
    win, mac = True, False
    RATIO = 1
elif sys.platform == "darwin":
    from appscript import app, mactypes
    win, mac = False, True
    RATIO = 1.375
else:
    exit()

# initializing module, hiding root window
root = tk.Tk()
root.withdraw()
current_window = None

SCREEN_WIDTH, SCREEN_HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

RATIO *= SCREEN_WIDTH / 1920

def main():
    # setting the current screen to start menu
    # app = main_screen(root)

    main_screen(root)
    # overall GUI loop which will run constantly, accepting input and such
    root.mainloop()

def resizing_uploaded_images(img, container=''):
    if img:
        iw, ih = img.width, img.height
        scale = SCREEN_WIDTH / iw
        if container == '':
            mw, mh = SCREEN_WIDTH, SCREEN_HEIGHT
        else:
            container.update()
            return ImageTk.PhotoImage(img.resize((int(container.winfo_width() * 0.9), int(container.winfo_height() * 0.9))))

        if iw > ih:
            ih = ih*(mw/iw)
            r = mh/ih if (ih/mh) > 1 else 1
            iw, ih = mw*r, ih*r
        else:
            iw = iw*(mh/ih)
            r = mw/iw if (iw/mw) > 1 else 1
            iw, ih = iw*r, mh*r


        return ImageTk.PhotoImage(img.resize(
            (int(iw*scale), int(ih*scale))))

def write_default_settings():
    with open("Settings.txt", 'w') as settings_file:
        settings_file.write("do_not_show: False")


class PlaceholderEntry(ttk.Entry):
    # initializing the arguments passed in
    def __init__(self, container, placeholder, validation, *args, **kwargs):
        super().__init__(container, *args, style="Placeholder.TEntry", **kwargs)
        self.placeholder = placeholder
        self.insert("0", self.placeholder)

        # runs the appropriate method for when the user is focused in/out of the element
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        # if this argument is given (like for the instagram password,
        # then the entry box will hide its text with asterisks)
        self.validation = validation

    def _clear_placeholder(self, e):
        # deleting all text placed automatically with the placeholder
        if self["style"] == "Placeholder.TEntry":
            self.delete("0", "end")
            self["style"] = "TEntry"

        # editing the property of the entry box 'show' to display asterisks ,
        # instead of any of the entered characters
        if self.validation == "password":
            self["show"] = "*"

    def _add_placeholder(self, e):
        # if there isn't any text entered in AND the user isn't focused in
        # on this, then it'll add the placeholder
        if not self.get():
            self.insert("0", self.placeholder)
            self["style"] = "Placeholder.TEntry"


def create_window(self, master, extra="", title=("", 0), return_value=False):
    #zooms into the window, since before it wouldn't always center correctly with the application's borders
    current_window = tk.Toplevel(master)
    current_window.state("zoomed")

    current_window.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+0+0")
    current_window.title(f"Background Revolution{extra}")
    self.canvas = tk.Canvas(
        current_window, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="#66AFF5"
    )
    self.canvas.pack()
    current_window.config()
    current_window.resizable(width=False, height=False)

    if title != ("", 0):
        self.title_frame = tk.Frame(current_window, bg="#13ae4b", bd=5)
        self.title_frame.place(
            relx=0.5, rely=0.025, relwidth=0.7, relheight=0.15, anchor="n"
        )

        self.title_label = tk.Label(
            self.title_frame,
            text=f"{title[0]}",
            font=("Courier", int(title[1] * RATIO))
        )
        self.title_label.place(relwidth=1, relheight=1)

    if return_value == True:
        self.return_button = tk.Button(
            current_window,
            text="Back",
            font=("Courier", int(50 * RATIO)),
            bg="#13ae4b",
            bd=5,
            command=lambda: main_screen.go_main_screen(self)
        )
        self.return_button.place(
            relwidth=0.1, relheight=0.15, relx=0.025, rely=0.025)

    # if the user kills the window via the window manager,
    # exit the application.
    current_window.wm_protocol("WM_DELETE_WINDOW", root.destroy)

    return current_window


class main_screen:
    def __init__(self, master):
        self.master = create_window(
            self, master, "", ("Background Revolution", 68), return_value=False
        )

        self.quit_button = tk.Button(
            self.master,
            text="Quit",
            font=("Courier", int(50 * RATIO)),
            command=lambda: root.destroy(),
            bg="#13ae4b",
            bd=5
        )
        self.quit_button.place(
            relwidth=0.1, relheight=0.15, relx=0.025, rely=0.025)

        #self.settings_pic = tk.PhotoImage(file="./images/settings_icon.png")
        self.settings_pic_button = tk.Button(
            self.master,
            bg="#13ae4b",
            bd=5,
            command=lambda: main_screen.go_settings_screen(self)
        )
        self.settings_pic_button.place(
            relx=0.875, rely=0.025, relheight=0.15, relwidth=0.1)

        self.settings_pic = resizing_uploaded_images(Image.open("./images/settings_icon.png"), self.settings_pic_button) 
        self.settings_pic_button.configure(image=self.settings_pic)

        with open("Settings.txt") as settings_file:
            settings_data = settings_file.readlines()
            if settings_data == []:
                write_default_settings()
                do_not_show = False
            elif settings_data[0] == "do_not_show: True":
                do_not_show = True
            elif settings_data[0] == 'do_not_show: False':
                do_not_show = False
            else:
                do_not_show = "needs reset"

        self.upload_frame = tk.Frame(self.master, bd=5, bg="#c4dc34")
        self.browse_frame = tk.Frame(self.master, bd=5, bg="#c4dc34")

        if do_not_show == True:
            self.upload_frame.place(
                relwidth=0.675, relheight=0.15, relx=0.025, rely=0.25
            )

            self.browse_frame.place(
                relwidth=0.675, relheight=0.15, relx=0.025, rely=0.475
            )
        else:
            self.upload_frame.place(
                relwidth=0.3, relheight=0.15, relx=0.025, rely=0.25
            )

            self.browse_frame.place(
                relwidth=0.3, relheight=0.15, relx=0.025, rely=0.475
            )

            self.explanation_frame = tk.Frame(self.master, bd=5, bg="#c4dc34")
            self.explanation_frame.place(
                relwidth=0.35, relheight=0.375, relx=0.7, rely=0.25, anchor="ne"
            )
            self.explanation_title_frame = tk.Frame(
                self.explanation_frame, bg="#e5efde")
            self.explanation_title_frame.place(
                relwidth=1, relheight=0.7
            )
            if do_not_show == False:
                
                explanation_reset_text = "This is a program written by Daniel and Stephen that will\nhelp you change your computer backgrounds! There are many\nfeatures and functions to help you. The cog will take you\nto a settings page, 'Upload Custom' allows you to use your\n own images, 'Browse Preset' allows you to use preset\n options, 'Search' allows you search for images online,\n'Manage Collections' is to manage the image colections\n you've made, and 'Schedule' will help you schedule\n your image rotation"
                explanation_reset_font = ("Courier", int(14 * RATIO))
                explanation_reset_command = main_screen.do_not_show_clicked()
                self.explanation_reset_button_text = "Don't show again"

                
            elif do_not_show == 'needs reset':
                explanation_reset_text = "It seems the settings \nhave been edited and can \nno longer be read from."
                explanation_reset_font = ("Courier", int(30 * RATIO))
                explanation_reset_command = write_default_settings()
                self.explanation_reset_button_text = 'Reset Settings'


            self.explantion_text = tk.Label(
                self.explanation_title_frame,
                bg="#e5efde",
                text=explanation_reset_text,
                font=explanation_reset_font
            )
            self.explantion_text.place(
                rely=0.5, relx=0.5, anchor='center'
            )
            self.explanation_do_not_show_button = tk.Button(
                self.explanation_frame,
                text=self.explanation_reset_button_text,
                anchor="center",
                font=("Courier", int(30 * RATIO)),
                bg="#e5efde",
                bd=5,
                command=lambda: explanation_reset_command
            )
            self.explanation_do_not_show_button.place(
                relwidth=1, relheight=0.3, rely=0.7
            )

        self.browse_button = tk.Button(
            self.browse_frame,
            text="Browse Preset",
            font=("Courier", int(50 * RATIO)),
            bg="#e5efde",
            command=lambda: main_screen.go_preset_screen(self)
        )
        self.browse_button.place(relx=0, relheight=1, relwidth=1)

        self.upload_button = tk.Button(
            self.upload_frame,
            text="Upload Custom",
            font=("Courier", int(50 * RATIO)),
            bg="#e5efde",
            command=lambda: main_screen.go_custom_screen(self)
        )
        self.upload_button.place(relx=0, relheight=1, relwidth=1)

        self.search_frame = tk.Frame(self.master, bd=5, bg="#c4dc34")
        self.search_frame.place(
            relwidth=0.675, relheight=0.2, relx=0.025, rely=0.7
        )

        self.collections_frame = tk.Frame(self.master, bd=5, bg="#c4dc34")
        self.collections_frame.place(
            relwidth=0.25, relheight=0.375, relx=0.975, rely=0.437, anchor="e"
        )

        self.collections_button = tk.Button(
            self.collections_frame,
            text="Manage\nCollections",
            font=("Courier", int(50 * RATIO)),
            bg="#e5efde",
            command=lambda: main_screen.go_manage_screen(self)
        )
        self.collections_button.place(relx=0, relheight=1, relwidth=1)

        self.schedule_frame = tk.Frame(self.master, bd=5, bg="#c4dc34")
        self.schedule_frame.place(
            relwidth=0.25, relheight=0.2, relx=0.975, rely=0.7, anchor="ne"
        )

        self.schedule_button = tk.Button(
            self.schedule_frame,
            text="Schedule",
            font=("Courier", int(50 * RATIO)),
            bg="#e5efde",
            command=lambda: main_screen.go_schedule_screen(self)
        )
        self.schedule_button.place(relx=0, relheight=1, relwidth=1)

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

    def go_main_screen(self):
        self.master.destroy()
        main_screen(root)

    def do_not_show_clicked():
        with open("Settings.txt", 'w') as settings_file:
            settings_data = "do_not_show: True"
            settings_file.writelines(settings_data)

class settings_screen:
    def __init__(self, master):
        self.master = create_window(
            self,
            master,
            " - Settings",
            title=("Settings & Info", 80),
            return_value=True,
        )

        self.theme_frame = tk.Frame(self.master, bg="#13ae4b", bd=5)
        self.theme_frame.place(
            relx=0.5, rely=0.425, relwidth=0.95, relheight=0.15, anchor="n"
        )

        self.theme_title = tk.Label(
            self.theme_frame,
            text="Theme:",
            bg="#13ae4b",
            font=(
                "Courier",
                int(80 * RATIO),
                "bold",
            ),
            fg="#c4dc34",
            bd=5,
        )
        self.theme_title.place(
            relx=0.125, rely=0, relwidth=0.3, relheight=1, anchor="n"
        )

        # add themes after in this frame to the right


class custom_screen:
    def __init__(self, master):
        self.master = create_window(
            self, master, "- Custom Collections", return_value=True
        )
        # buttons in top right corner
        self.action_frame = tk.Frame(
            self.master, bd=10, bg="#13ae4b"
        )
        self.action_frame.place(
            relwidth=0.175, relheight=0.15, rely=0.025, relx=0.8)

        self.trashcan_pic_button = tk.Button(
            self.action_frame,
            bg="#e5efde",
            command=lambda: custom_screen.trash_image_preview()
        )
        self.trashcan_pic_button.place(relx=0, relheight=0.67, relwidth=0.5)

        self.trashcan_pic = resizing_uploaded_images(Image.open("./images/trash.png"), self.trashcan_pic_button) 
        self.trashcan_pic_button.configure(image=self.trashcan_pic)

        #note to self: need to apply to trashcan, resizing

        self.save_to_button = tk.Button(
            self.action_frame,
            text="Save To",
            bg="#e5efde",
            font=(
                "Courier",
                int(20 * RATIO),
            ),
            command=lambda: custom_screen.save_images_to()
        )
        self.save_to_button.place(relx=0.5, relheight=0.67, relwidth=0.5)

        self.toggle_select_button = tk.Button(
            self.action_frame,
            text="Toggle Select All",
            font=(
                "Courier",
                int(20 * RATIO),
            ),
            bg="#e5efde",
            command=lambda: custom_screen.toggle_select_all()
        )
        self.toggle_select_button.place(
            relx=0, rely=0.67, relheight=0.33, relwidth=1)

        # fitting the output
        self.preview_frame = tk.Frame(
            self.master, highlightcolor="#13ae4b", bd=10, bg="#13ae4b"
        )
        self.preview_frame.place(
            relx=0.5, rely=0.225, relwidth=0.95, relheight=0.7, anchor="n"
        )

        self.preview_text = tk.Label(
            self.preview_frame,
            text="<Preview Your Images Here>",
            bg="#13ae4b",
            font=(
                "Courier",
                int(80 * RATIO),
                "bold",
            ),
            fg="#0f893b"
        )
        self.preview_text.place(relx=0.5, rely=0.5, anchor="center")

        # button for file explorer

        self.select_button = tk.Button(
            self.master,
            text=f"Select Images from {'File Explorer' if win == True else 'Files'}",
            font=(
                "Courier",
                int(int(f"{'44' if win == True else '58'}") * RATIO),
            ),  # need to test this 58 value on mac
            bg="#e5efde",
            bd=5,
            command=lambda: custom_screen.retrieve_file(self)
        )
        self.select_button.place(
            relx=0.15, relheight=0.15, relwidth=0.625, rely=0.025)

    def retrieve_file(self):
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
                    (a, "*.raw")
                )
            )
        )

        try:
            self.background_uploaded_img = resizing_uploaded_images(Image.open(str(names_of_files[0]))) 
            self.background_uploaded_label = tk.Label(
                self.preview_frame, image=self.background_uploaded_img)
            self.background_uploaded_label.place(relheight=1, relwidth=1)
        
        except:
            self.preview_text.text, self.preview_text.font = \
                "Failed to Upload/Preview Image(s)", \
                "Courier",
            int(68 * RATIO),
            "bold"

    def trash_image_preview():
        pass

    def save_images_to():
        pass

    def toggle_select_all():
        pass

    def set_background_uploaded():
        if win:
            ctypes.windll.user32.SystemParametersInfoW(
                20, 0, names_of_files, 0)
        else:
            app("Finder").desktop_picture.set(mactypes.File(names_of_files))


class preset_screen:
    def __init__(self, master):
        self.master = create_window(
            self, master, "- Preset Collections", return_value=True
        )


class search_screen:
    def __init__(self, master):
        self.master = create_window(
            self, master, " - Search", return_value=True
        )


class manage_screen:
    def __init__(self, master):
        self.master = create_window(
            self, master, " - Manage Collections", return_value=True
        )


class schedule_screen:
    def __init__(self, master):
        self.master = create_window(
            self, master, " - Schedule Collection Rotations", return_value=True
        )


if __name__ == "__main__":
    main()
