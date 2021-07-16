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
        self.weather_frame.place(relx=0.5, rely=0.05, relwidth=0.75, relheight=0.1, anchor='n')
        
        #fitting the output
        self.lower_frame = tk.Frame(self.master, highlightcolor="#99aab5", bd=10)
        self.lower_frame.place(relx=0.5, rely=0.20, relwidth=0.75, relheight=0.7, anchor='n')

        name = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        name.place(rely=0, relwidth=1, relheight=0.165)

        chamber_member_bool = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        chamber_member_bool.place(rely=0.165, relwidth=1, relheight=0.165)

        phone_number = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        phone_number.place(rely=0.33, relwidth=1, relheight=0.165)

        website = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        website.place(rely=0.495, relwidth=1, relheight=0.165)

        address = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        address.place(rely=0.66, relwidth=1, relheight=0.165)

        address2 = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        address2.place(rely=0.825, relwidth=1, relheight=0.165)

        #button for file explorer
        #I only want its command to run once, when it's clicked so I made a 
        #simple lambda that invokes the info_display function
        self.button = tk.Button(self.weather_frame, text="Web Scrape", font=('Courier', 24), bg='white', 
        command=lambda:retrieve_file())
        self.button.place(relx=0, relheight=1, relwidth=1)

        #next and prev. buttons for chambers navigation
        
        #making the picture into a label
        self.previous_pic = tk.PhotoImage(file='./images/previous_pic.png')
        self.previous_pic_label = tk.Label(self.master, image=self.previous_pic)
        self.previous_pic_label.place(relwidth=0.1, relheight=0.17786, rely=0.45, relx=0.0125)

        #putting a button at the same spot as the label, essentially making it into one.
        self.previous_pic_button = tk.Button(self.master, image=self.previous_pic, 
        )#command=lambda:
        self.previous_pic_button.place(relwidth=0.1, relheight=0.17786, rely=0.45, relx=0.0125)

        self.next_pic = tk.PhotoImage(file='./images/next_pic.png')
        self.next_pic_label = tk.Label(self.master, image=self.next_pic)
        self.next_pic_label.place(relwidth=0.1, relheight=0.17786, rely=0.45, relx=0.885) #1366/768 = 1.7786, so I set height to 
                                                                                        #this so that it'd be proportional to width.
        self.next_pic_button = tk.Button(self.master, image=self.next_pic, 
        )#command=lambda:
        self.next_pic_button.place(relwidth=0.1, relheight=0.17786, rely=0.45, relx=0.885) 

if __name__ == '__main__':
    main()