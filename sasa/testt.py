    side_img_data = Image.open("side-img.png")
    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(500, 600))
    talk_window = tk.Toplevel(main_window)
    talk_window.title("Talk With Me")
    talk_window.geometry("1024x600")

    CTkLabel(master=talk_window, text="", image=side_img).pack(side="left", fill="y")

    button_frame = CTkFrame(master=talk_window, width=512, height=600)
    button_frame.pack_propagate(0)
    button_frame.pack(expand=True, side="right")

    tk.Label(button_frame, text="Please select an option").pack(pady=10)

    button_width = 20
    button_height = 2

    tk.Button(button_frame, text="Text", command=lambda: start_chatbot("Text"), width=button_width, height=button_height).pack(pady=10)
    tk.Button(button_frame, text="Speech", command=lambda: start_chatbot("Speech"), width=button_width, height=button_height).pack(pady=10)
    tk.Button(button_frame, text="Return", command=lambda: return_to_main_window(talk_window), width=button_width, height=button_height).pack(pady=10) 

