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
    root.filename = filedialog.askopenfilename(initialdir='/', title='Select an Image File', filetypes=(
        ("compatible image files", "*.png"), 
        ("compatible image files", "*.jpeg"), 
        ("compatible image files", "*.jpg"),
        ("compatible image files", "*.gif"),
        ("compatible image files", "*.tiff"),
        ("compatible image files", "*.psd"),
        ("compatible image files", "*.pdf"),
        ("compatible image files", "*.eps"),
        ("compatible image files", "*.ai"),
        ("compatible image files", "*.indd"),
        ("compatible image files", "*.raw")
    )
    )


class PlaceholderEntry(ttk.Entry):
    #initializing the arguments passed in
    def __init__(self, container, placeholder, validation, *args, **kwargs):
        super().__init__(container, *args, style="Placeholder.TEntry", **kwargs)
        self.placeholder = placeholder
        self.insert("0", self.placeholder)
        
        #runs the appropriate method for when the user is focused in/out of the element
        self.bind("<FocusIn>", self.clear_placeholder)
        self.bind("<FocusOut>", self.add_placeholder)
        
        #if this argument is given (like for the instagram password, 
        # then the entry box will hide its text with asterisks)
        self.validation = validation

    
    def clear_placeholder(self, e):
        #deleting all text placed automatically with the placeholder
        if self["style"] == "Placeholder.TEntry":
            self.delete("0", "end")
            self["style"] = "TEntry"
        
        #editing the property of the entry box 'show' to display asterisks ,
        #instead of any of the entered characters
        if self.validation == 'password':
            self['show'] = "*"
        
    def add_placeholder(self, e):
        #if there isn't any text entered in AND the user isn't focused in 
        #on this, then it'll add the placeholder
        if not self.get():
            self.insert("0", self.placeholder)
            self["style"] = "Placeholder.TEntry"


class main_screen():
    def __init__(self, master):
        #these properties will mostly stay constant throughout all windows
        self.master = master
        self.master.title("Windows Background Thing")
        self.canvas = tk.Canvas(self.master, height=HEIGHT, width=WIDTH, bg = '#23272a')
        self.canvas.pack()
        self.master.config(bg = "#23272a")
        self.master.resizable(width=False, height=False)

        
        # #making the style of this window compatible with my custom entry class
        # self.style = ttk.Style(self.master)
        # self.style.configure("Placeholder.TEntry", foreground="#d5d5d5")
        

        #fitting the entry and button for weather
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

        #entry text box for user input
        self.entry = PlaceholderEntry(self.weather_frame, "State Name", '', font=('Courier', 36))
        self.entry.place(relwidth=0.65, relheight=1)

        #button for state entry
        #I only want its command to run once, when it's clicked so I made a 
        #simple lambda that invokes the info_display function
        self.button = tk.Button(self.weather_frame, text="Web Scrape", font=('Courier', 24), bg='white', 
        command=lambda:retrieve_file())
        self.button.place(relx=0.7, relheight=1, relwidth=0.3)




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