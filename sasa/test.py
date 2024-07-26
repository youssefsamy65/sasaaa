import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Voice Command Setup")
root.geometry("500x200")

# Create a label with the cheerful instruction message
instruction_label = tk.Label(root, text="Please open your mobile browser and go to:\nhttp://localhost:3000/voice_command", font=("Arial", 14), fg="green")
instruction_label.pack(pady=20)

# Create a Terminate button
terminate_button = tk.Button(root, text="Close", command=root.destroy, bg="red", fg="white", font=("Arial", 12, "bold"))
terminate_button.pack(pady=10)

# Run the application
root.mainloop()

