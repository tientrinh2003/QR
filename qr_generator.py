import tkinter as tk
from PIL import Image, ImageTk
import pyqrcode
import threading

class QRGenerator:
    def __init__(self):
        self.root = None

    def generate_qr(self, content, filename):
        url = pyqrcode.create(content)
        url.png(filename, scale=6)

    def display_qr(self, filename):
        if self.root is None:
            self.root = tk.Tk()
            # self.root.attributes('-fullscreen', True)
            # self.root.wm_attributes("-topmost", True)
            self.root.bind('<Escape>', lambda e: self.close_qr())

        img = Image.open(filename)
        img = ImageTk.PhotoImage(img)
        label = tk.Label(self.root, image=img)
        label.pack(expand=True)

        label.image = img  # Keep a reference to avoid garbage collection

    def close_qr(self):
        if self.root is not None:
            self.root.after(0, self._destroy_root)  # Schedule destruction in the main thread

    def _destroy_root(self):
        if self.root is not None:
            self.root.quit()  # Close the main event loop
            self.root.destroy()  # Destroy the window
            self.root = None

    def generate_and_display_qr(self, content):
        filename = "package_qr.png"
        self.generate_qr(content, filename)
        threading.Thread(target=self._start_display, args=(filename,)).start()

    def _start_display(self, filename):
        self.display_qr(filename)
        self.root.mainloop()  # Run the main event loop in a separate thread

    def show_success_message(self, message):
        if self.root is not None:
            success_label = tk.Label(self.root, text=message, font=("Helvetica", 24), fg="green")
            success_label.pack(expand=True)
            self.root.after(3000, self.close_qr)  # Automatically close after 3 seconds
