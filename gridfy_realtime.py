
import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk
import string

import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk
import string

class GridifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gridify")

        # Original high-res image and its path
        self.image_path = None
        self.original_image = None
        self.grid_applied_image = None
        # Resized image for display
        self.tk_original_image = None
        self.tk_grid_image = None
        self.font_size = tk.IntVar(value=10)
        self.font_size.trace("w", self.update_grid)
        self.grid_size = tk.IntVar(value=10)
        self.grid_size.trace("w", self.update_grid)
        self.font_color = "#FFFFFF"

#         # Create canvas for original image and grid image
#         self.original_canvas = tk.Canvas(root, width=500, height=250)
#         self.original_canvas.pack(fill=tk.BOTH, expand=True)  # Use fill and expand to resize with window
#         self.original_canvas.bind("<Configure>", self.update_canvas_images)  # Resize images when canvas size changes
#         self.grid_canvas = tk.Canvas(root, width=500, height=250)
#         self.grid_canvas.pack(fill=tk.BOTH, expand=True)  # Use fill and expand to resize with window
#         self.grid_canvas.bind("<Configure>", self.update_canvas_images)  # Resize images when canvas size changes

        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Button(self.controls_frame, text="画像を開く", command=self.open_image,width=15, height=3).pack(side=tk.TOP, pady=10)
        tk.Scale(self.controls_frame, from_=1, to=50, label="Grid Size", variable=self.grid_size, orient=tk.HORIZONTAL).pack(side=tk.TOP, pady=10)
        tk.Scale(self.controls_frame, from_=1, to=50, label="Font Size", variable=self.font_size, orient=tk.HORIZONTAL).pack(side=tk.TOP, pady=10)
        tk.Button(self.controls_frame, text="Font Color", command=self.choose_font_color,width=15, height=3).pack(side=tk.TOP, pady=10)
        tk.Button(self.controls_frame, text="グリッド画像のみ保存", command=self.save_image,width=15, height=3).pack(side=tk.TOP, pady=10)
        tk.Button(self.controls_frame, text="元画像とグリッド画像の\n結合保存", command=self.save_combined_image, width=15, height=3).pack(side=tk.TOP, pady=10)

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.original_canvas = tk.Canvas(self.canvas_frame, width=500, height=250)
        self.original_canvas.pack(fill=tk.BOTH, expand=True)
        self.original_canvas.bind("<Configure>", self.update_canvas_images)  # Resize images when canvas size changes
        self.grid_canvas = tk.Canvas(self.canvas_frame, width=500, height=250)
        self.grid_canvas.pack(fill=tk.BOTH, expand=True)
        self.grid_canvas.bind("<Configure>", self.update_canvas_images)  # Resize images when canvas size changes


    # Open image file
    def open_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if self.image_path:
            self.original_image = Image.open(self.image_path)
            self.grid_applied_image = self.original_image.copy()
            self.update_canvas_images()

    # Update displayed images
    def update_canvas_images(self, event=None):  # Accept event argument, but do not use it
        if self.original_image and self.grid_applied_image:
            # Update original image
            canvas_width = self.original_canvas.winfo_width()
            canvas_height = self.original_canvas.winfo_height()
            self.tk_original_image = ImageTk.PhotoImage(self.resize_image(self.original_image, canvas_width, canvas_height))
            self.original_canvas.delete("all")  # Clear canvas before drawing new image
            self.original_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_original_image)

            # Update grid image
            canvas_width = self.grid_canvas.winfo_width()
            canvas_height = self.grid_canvas.winfo_height()
            self.tk_grid_image = ImageTk.PhotoImage(self.resize_image(self.grid_applied_image, canvas_width, canvas_height))
            self.grid_canvas.delete("all")  # Clear canvas before drawing new image
            self.grid_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_grid_image)

    def resize_image(self, image, canvas_width, canvas_height):
        width_ratio = canvas_width / image.width
        height_ratio = canvas_height / image.height
        ratio = min(width_ratio, height_ratio)
        new_width = int(image.width * ratio)
        new_height = int(image.height * ratio)
        return image.resize((new_width, new_height))

    # Choose font color
    def choose_font_color(self):
        self.font_color = colorchooser.askcolor()[1]
        self.update_grid()

    # Apply grid to image
    def apply_grid(self, image):
        num_rows = num_cols = self.grid_size.get()
        width, height = image.size
        draw = ImageDraw.Draw(image)

        # Draw grid lines
        for i in range(0, width, width // num_cols):
            draw.line([(i, 0), (i, height)], fill=128)
        for i in range(0, height, height // num_rows):
            draw.line([(0, i), (width, i)], fill=128)

        # Add labels
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", self.font_size.get())
        for i in range(num_rows):
            for j in range(num_cols):
                label = string.ascii_uppercase[j] + str(i + 1)
                draw.text((j * width // num_cols, i * height // num_rows), label, font=font, fill=self.font_color)

    def update_grid(self, *args):
        if self.original_image:
            self.grid_applied_image = self.original_image.copy()
            self.apply_grid(self.grid_applied_image)
            self.update_canvas_images()

    # Save the image with the grid
    def save_image(self):
        
        if self.grid_applied_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image files", "*.jpg *.png")])
            if save_path:
                self.save_to_path(self.grid_applied_image, save_path)

    # Save both images combined as a single image
    def save_combined_image(self):
        if self.original_image and self.grid_applied_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image files", "*.jpg *.png")])
            if save_path:
                combined_image = Image.new('RGB', (self.original_image.width, self.original_image.height * 2))
                combined_image.paste(self.original_image, (0, 0))
                combined_image.paste(self.grid_applied_image, (0, self.original_image.height))
                self.save_to_path(combined_image, save_path)

    def save_to_path(self, image, path):
        if image.mode == 'RGBA':
            rgb_image = image.convert('RGB')
            rgb_image.save(path)
        else:
            image.save(path)

if __name__ == "__main__":
    root = tk.Tk()
    app = GridifyApp(root)
    root.mainloop()

