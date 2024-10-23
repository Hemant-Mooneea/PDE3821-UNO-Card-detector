from tkinter import *
from tkinter import PhotoImage

# Function to handle button clicks
def button_action(button_name):
    if button_name == "Button 1":
        open_window_1()  # Open the first window
    elif button_name == "Button 2":
        open_window_2()  # Open the second window
    elif button_name == "Button 3":
        root.quit()  # Close the main window (exit the program)


# Function to open the first window
def open_window_1():
    root.withdraw()  # Hide the main window
    window_1 = Toplevel(root)  # Create a new window
    window_1.title("Window 1 - Camera")  # Set the title of the new window
    window_1.geometry("400x300")  # Set the size of the new window
    
    # Add content to the first window
    label = Label(window_1, text="This is the Camera window", font=("Arial", 18))
    label.pack(pady=20)
    
    # Function to close the new window and show the main window again
    def on_close():
        window_1.destroy()  # Close the new window
        root.deiconify()  # Show the main window again
    
    # Add a close button that will also restore the main window
    close_button = Button(window_1, text="Close", command=on_close, font=("Arial", 14))
    close_button.pack(pady=10)

# Function to open the second window
def open_window_2():
    root.withdraw()  # Hide the main window
    window_2 = Toplevel(root)  # Create another new window
    window_2.title("Window 2 - Photo Detection")  # Set the title of the new window
    window_2.geometry("400x300")  # Set the size of the new window
    
    # Add content to the second window
    label = Label(window_2, text="This is the Photo Detection window", font=("Arial", 18))
    label.pack(pady=20)
    
    # Function to close the new window and show the main window again
    def on_close():
        window_2.destroy()  # Close the new window
        root.deiconify()  # Show the main window again
    
    # Add a close button that will also restore the main window
    close_button = Button(window_2, text="Close", command=on_close, font=("Arial", 14))
    close_button.pack(pady=10)


# Create the main window
root = Tk()
root.title("UNO Card Detection")

# Set window size to accommodate the 500x500 image + space for text
root.geometry("1000x550+300+200")
root.configure(bg="#fff")

# Allow the window to be resizable
root.resizable(True, True)

# Load and display the image (500x500)
img = PhotoImage(file="uno.png")
image_label = Label(root, image=img, bg='white')
image_label.place(x=30, y=25)  # Slight adjustment to y for better centering

# Create a frame on the right side for the text and buttons
frame = Frame(root, bg="white")
frame.place(x=500, y=70, width=400, height=350)  # Adjusted the x for spacing

# Add a welcome label inside the frame
heading = Label(frame, text='Welcome', fg='#57a1f8', bg='white',
                font=("Times", "50", "bold italic"))
heading.place(x=100, y=5)

# Add a subheading label under the welcome label
subheading = Label(frame, text='UNO Detection Card', fg='black', bg='white',
                   font=("Verdana", "15", "italic"))  # Smaller italic font
subheading.place(x=130, y=75)  # Adjusted y position to place it under the heading


# Create buttons
button1 = Button(frame, text="Open Camera", command=lambda: button_action("Button 1"), 
                 bg="#57a1f8", fg="white", font=("Arial", 14), relief="flat")
button1.place(x=100, y=170, width=300, height=40)

button2 = Button(frame, text="Photo Detection", command=lambda: button_action("Button 2"), 
                 bg="#57a1f8", fg="white", font=("Arial", 14), relief="flat")
button2.place(x=100, y=240, width=300, height=40)

button3 = Button(frame, text="Exit", command=lambda: button_action("Button 3"), 
                 bg="#57a1f8", fg="white", font=("Arial", 14), relief="flat")
button3.place(x=100, y=310, width=300, height=40)


# Run the Tkinter main loop
root.mainloop()
