def get_center_coords(window, width, height):
    screen_width = window.winfo_screenwidth()  # Width of the screen
    screen_height = window.winfo_screenheight()  # Height of the screen

    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    return f"{width}x{height}+{int(x)}+{int(y)}"


def make_invisible(widget):
    widget.pack_forget()
