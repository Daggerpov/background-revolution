import tkinter as tk
from tkinter import ttk, filedialog

HEIGHT = 768
WIDTH = 1366

def main():
    #initializing module
    global root
    root = tk.Tk()
    
    # #setting the current screen to start menu
    app = main_screen(root)
    
    # #overall GUI loop which will run constantly, accepting input and such
    root.mainloop()

def retrieve_file():
    a = 'compatible image files'
    root.filename = filedialog.askopenfilename(initialdir='/', title='Select an Image File', filetypes=(
        ("compatible image files", "*.png"), 
        (a, "*.jpeg"), 
        (a, "*.jpg"),
        (a, "*.gif"),
        (a, "*.tiff"),
        (a, "*.psd"),
        (a, "*.pdf"),
        (a, "*.eps"),
        (a, "*.ai"),
        (a, "*.indd"),
        (a, "*.raw")
    )
    )

    

class main_screen():
    def __init__(self, master):
        #these properties will mostly stay constant throughout all windows
        self.master = master
        self.master.title("Windows Background Thing")
        self.canvas = tk.Canvas(self.master, height=HEIGHT, width=WIDTH, bg = '#23272a')
        self.canvas.pack()
        self.master.config(bg = "#23272a")
        self.master.resizable(width=False, height=False)

        #fitting the button for opening the file explorer
        self.weather_frame = tk.Frame(self.master, bg="#99aab5", bd=5)
        self.weather_frame.place(relx=0.4, rely=0.075, relwidth=0.75, relheight=0.1, anchor='n')
        
        #fitting the output
        self.lower_frame = tk.Frame(self.master, highlightcolor="#99aab5", bd=10)
        self.lower_frame.place(relx=0.4, rely=0.225, relwidth=0.75, relheight=0.7, anchor='n')

        #button for file explorer
        #I only want its command to run once, when it's clicked so I made a 
        #simple lambda that invokes the info_display function
        self.button = tk.Button(self.weather_frame, text="Select Image in File Explorer", font=('Courier', 40), bg='white', 
        command=lambda:retrieve_file())
        self.button.place(relx=0, relheight=1, relwidth=1)

        #submit button to accept the file

        self.submit_frame = tk.Frame(self.master, highlightcolor="#99aab5", bd=10)
        self.submit_frame.place(relwidth=0.175, relheight=0.85, rely=0.075, relx=0.8)

        self.submit_pic = tk.PhotoImage(file='./images/submit_pic.png')
        self.submit_pic_new = self.submit_pic.subsample(2, 2)

        self.submit_pic_button = tk.Button(self.submit_frame, image=self.submit_pic_new, bd=5
        , bg="white")#command=lambda:
        self.submit_pic_button.place(relx=0, relheight=1, relwidth=1) 

if __name__ == '__main__':
    main()