import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageEnhance
from tkinter import ttk
from io import BytesIO


root = tk.Tk()
root.geometry("1000x600")  # GUI Interface size
root.title("PixelCraft - A Python based Image Manipulation Tool")
root.config(bg="white")

pen_color = "black"
pen_size = 5
file_path = ""
original_image = None
manipulated_image = None

brightness_value = 1.0  # Default brightness value
contrast_value = 1.0  # Default contrast value
saturation_value = 1.0  # Default saturation value
hue_value = 0  # Default hue value


def add_image():
    global file_path, original_image, manipulated_image
    file_path = filedialog.askopenfilename(initialdir="D:\My Github Projects\PixelCraft\images")
    image = Image.open(file_path)
    width, height = int(image.width / 2), int(image.height / 2)
    image = image.resize((width, height), Image.LANCZOS)
    canvas.config(width=image.width, height=image.height)
    original_image = image.copy()
    manipulated_image = original_image.copy()
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

def change_size(size):
    global pen_size
    pen_size = size

def draw(event):
    x1, y1 = (event.x - pen_size), (event.y - pen_size)
    x2, y2 = (event.x + pen_size), (event.y + pen_size)
    canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline='')

def clear_canvas():
    canvas.delete("all")
    canvas.create_image(0, 0, image=canvas.image, anchor="nw")

def apply_filter(filter):
    global manipulated_image
    if filter == "Original":
        manipulated_image = original_image.copy()
    else:
        image = original_image.copy()
        if filter == "Black and White":
            image = ImageOps.grayscale(image)
        elif filter == "Blur":
            image = image.filter(ImageFilter.BLUR)
        elif filter == "Sharpen":
            image = image.filter(ImageFilter.SHARPEN)
        elif filter == "Smooth":
            image = image.filter(ImageFilter.SMOOTH)
        elif filter == "Emboss":
            image = image.filter(ImageFilter.EMBOSS)
        manipulated_image = image.copy()
    image = ImageTk.PhotoImage(manipulated_image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def change_brightness(value):
    global brightness_value
    brightness_value = float(value)
    apply_adjustments()

def change_contrast(value):
    global contrast_value
    contrast_value = float(value)
    apply_adjustments()

def change_saturation(value):
    global saturation_value
    saturation_value = float(value)
    apply_adjustments()

def change_hue(value):
    global hue_value
    hue_value = int(value)
    apply_adjustments()

def apply_adjustments():
    global manipulated_image, brightness_value, contrast_value, saturation_value, hue_value
    image = original_image.copy()

    # Apply brightness adjustment
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_value)

    # Apply contrast adjustment
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_value)

    # Apply saturation adjustment
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(saturation_value)

    # Apply hue adjustment
    image = image.convert('HSV')
    pixels = image.load()
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            pixels[x, y] = (pixels[x, y][0] + hue_value % 256, pixels[x, y][1], pixels[x, y][2])
    image = image.convert('RGB')

    manipulated_image = image.copy()
    image = ImageTk.PhotoImage(manipulated_image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def download_image():
    if manipulated_image:
        save_path = filedialog.asksaveasfilename(
            initialdir="D:\My Github Projects\PixelCraft\images",
            defaultextension=".png",
            filetypes=(("PNG Image", "*.png"), ("All Files", "*.*"))
        )
        if save_path:
            original_width, original_height = original_image.size
            resized_image = manipulated_image.resize((original_width*2, original_height*2), Image.LANCZOS)
            resized_image.save(save_path)

# Create GUI Elements

left_frame = tk.Frame(root, width=200, height=600, bg="white")
left_frame.pack(side="left", fill="y")

canvas = tk.Canvas(root, width=750, height=600)
canvas.pack()

image_button = tk.Button(left_frame, text="Add Image", command=add_image, bg="white")
image_button.pack(pady=15)

color_button = tk.Button(left_frame, text="Change Pen Color", command=change_color, bg="white")
color_button.pack(pady=5)

pen_size_frame = tk.Frame(left_frame, bg="white")
pen_size_frame.pack(pady=5)

pen_size_1 = tk.Radiobutton(pen_size_frame, text="Small", value=3, command=lambda: change_size(3), bg="white")
pen_size_1.pack(side="left")

pen_size_2 = tk.Radiobutton(pen_size_frame, text="Medium", value=5, command=lambda: change_size(5), bg="white")
pen_size_2.pack(side="left")
pen_size_2.select()

pen_size_3 = tk.Radiobutton(pen_size_frame, text="Large", value=7, command=lambda: change_size(7), bg="white")
pen_size_3.pack(side="left")

clear_button = tk.Button(left_frame, text="Clear", command=clear_canvas, bg="#FF9797")
clear_button.pack(pady=10)

filter_label = tk.Label(left_frame, text="Select Filter", bg="white")
filter_label.pack()
filter_combobox = ttk.Combobox(left_frame, values=["Original", "Black and White", "Blur", "Emboss", "Sharpen", "Smooth"])
filter_combobox.pack()

filter_combobox.bind("<<ComboboxSelected>>", lambda event: apply_filter(filter_combobox.get()))

download_button = tk.Button(left_frame, text="Download Image", command=download_image, bg="white")
download_button.pack(pady=10)

brightness_slider = tk.Scale(left_frame, from_=0.0, to=2.0, resolution=0.01, orient="horizontal", label="Brightness",
                            command=change_brightness, bg="white")
brightness_slider.pack(pady=5)

contrast_slider = tk.Scale(left_frame, from_=0.0, to=2.0, resolution=0.01, orient="horizontal", label="Contrast",
                          command=change_contrast, bg="white")
contrast_slider.pack(pady=5)

saturation_slider = tk.Scale(left_frame, from_=0.0, to=2.0, resolution=0.01, orient="horizontal", label="Saturation",
                             command=change_saturation, bg="white")
saturation_slider.pack(pady=5)

hue_slider = tk.Scale(left_frame, from_=-180, to=180, orient="horizontal", label="Hue",
                      command=change_hue, bg="white")
hue_slider.pack(pady=5)


canvas.bind("<B1-Motion>", draw)

root.mainloop()
