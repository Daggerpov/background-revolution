import os, sys, ctypes

from appscript import app, mactypes

import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image

HEIGHT, WIDTH = 768, 1366

def main():
    global win, mac
    #determining OS of user
    if sys.platform == "win32":
        win, mac = True, False 
    elif sys.platform == "darwin":
        win, mac = False, True
    else:
        exit()

    #initializing module
    global root
    root = tk.Tk()
    
    # #setting the current screen to start menu
    app = main_screen(root)
    
    # #overall GUI loop which will run constantly, accepting input and such
    root.mainloop()    

class main_screen():
    def __init__(self, master):
        #these properties will mostly stay constant throughout all windows
        self.master = master
        self.master.title("Windows Background Thing")
        self.canvas = tk.Canvas(self.master, height=HEIGHT, width=WIDTH, bg="#66AFF5")
        self.canvas.pack()
        self.master.config(bg="#66AFF5")
        self.master.resizable(width=False, height=False)

        #fitting the button for opening the file explorer
        self.weather_frame = tk.Frame(self.master, bg="#73B504", bd=5)
        self.weather_frame.place(relx=0.4, rely=0.075, relwidth=0.75, relheight=0.1, anchor='n')
        
        #fitting the output
        self.lower_frame = tk.Frame(self.master, highlightcolor="#73B504", bd=10, bg="#73B504")
        self.lower_frame.place(relx=0.4, rely=0.225, relwidth=0.75, relheight=0.7, anchor='n')

        #button for file explorer
        #I only want its command to run once, when it's clicked so I made a 
        #simple lambda that invokes the info_display function
        self.button = tk.Button(self.weather_frame, text="Select Image in File Explorer", font=('Courier', 40), bg='white', 
        command=lambda: main_screen.retrieve_file(self.lower_frame))
        self.button.place(relx=0, relheight=1, relwidth=1)

        #submit button to accept the file

        self.submit_frame = tk.Frame(self.master, highlightcolor="#73B504", bd=10, bg="#73B504")
        self.submit_frame.place(relwidth=0.175, relheight=0.85, rely=0.075, relx=0.8)

        self.submit_pic = tk.PhotoImage(file='./images/submit_pic.png')
        self.submit_pic_new = self.submit_pic.subsample(2, 2)

        self.submit_pic_button = tk.Button(self.submit_frame, image=self.submit_pic_new, bg="white", 
        command=lambda:main_screen.set_background_uploaded(self))
        self.submit_pic_button.place(relx=0, relheight=1, relwidth=1) 
    
    def retrieve_file(lower_frame):
        a = 'compatible image files'

        global name_of_file

        if win:
            directory = '/This PC' 
        else:
            directory = '/Recents' 

        name_of_file = filedialog.askopenfilename(initialdir=directory, title='Select an Image File', filetypes=(
            (a, "*.png"), 
            (a, "*.jpeg"), 
            (a, "*.jpg*"), #should be *.jpg
            (a, "*.gif"),
            (a, "*.tiff"),
            (a, "*.psd"),
            (a, "*.eps"),
            (a, "*.ai"),
            (a, "*.indd"),
            (a, "*.raw")
        )
        )

        background_uploaded = ImageTk.PhotoImage(Image.open(name_of_file))
        
        background_uploaded_label = tk.Label(lower_frame) 
        background_uploaded_label.place(relheight=1, relwidth=1)

        background_uploaded_label.configure(image=background_uploaded)
        background_uploaded_label.image = background_uploaded
    
    def set_background_uploaded(self):
        if win:
            #self.path = os.path.abspath(os.path.dirname(sys.argv[0]))
            ctypes.windll.user32.SystemParametersInfoW(20, 0, name_of_file , 0)
        else:
            app('Finder').desktop_picture.set(mactypes.File(name_of_file))

if __name__ == '__main__':
    main()