from typing import Optional, Tuple, Union
import customtkinter as ctk
from os import path, listdir
from os .path import join
import os
from PIL import Image, ImageTk
from customtkinter.windows.widgets.font import CTkFont
from customtkinter.windows.widgets.image import CTkImage
import tkinter as tk
import sys

# from ctypes import windll,byref, sizeof,c_int
import ctypes as ct



class App(tk.Tk):
    
    def __init__(self,image_path=0):
        super().__init__()
        self.title("Image_viewer")
        self.minsize(400,400)
        self.geometry("800x600")
        self.menu = Menu(self)
        # Change the title bar color to grey
        self.update()
        # hwd = windll.user32.GetParent(self.winfo_id())
        # color = 0x00FF00FF
        
        # windll.dwmapi.DwmSetWindowAttribute(hwd,35,byref(c_int(color)),sizeof(c_int))
        # print(hwd)
        
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ct.windll.user32.GetParent
        hwnd = get_parent(self.winfo_id())
        rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
        value = 2
        value = ct.c_int(value)
        set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))
        
        if image_path:
            self.Image_frame =ImageFrame(self,image_path=image_path)
        
        # self.Image_frame =ImageFrame(self)
        
        
    def start(self):
        self.mainloop()
    def load_new(self,img_path):
        try: 
            self.Image_frame.destroy()
        except:
            pass
        print(img_path)
        self.Image_frame =ImageFrame(self,image_path=img_path)
        
        
class ImageFrame(ctk.CTkFrame):
    def __init__(self,parent,image_path=0):
        super().__init__(parent)
        
        
        self.pack(fill="both",expand=True)
        self.update()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        print(self.height)
        if image_path:
            self.image_canvas= Image_canvas(self,self.width,self.height,image_path)
        else:
            self.image_canvas= Image_canvas(self,self.width,self.height)
        self.bind("<Configure>", command= self.image_canvas.resize_image)
    
    
        
        
class Image_canvas(tk.Canvas):
    def __init__(self,parent,width,height,image_path=0,):
        super().__init__(parent,bg="#282828",bd=0,relief="ridge",highlightthickness=0)
        self.pack(fill="both",expand=True)
        if image_path:
            self.load_image(width,height,image_path=image_path)                

    def load_image(self,width,height,image_path=0):
        if image_path: 
            self.image = Image.open(image_path)    
        else: 
            self.image = Image.open("./Images/screenshot.png")
        self.loaded_width = self.image.size[0]
        self.loaded_height = self.image.size[1]
        
        scale = self.calculate_scale(width,height)
        self.image_resized = self.image.resize((int(scale[0]),int(scale[1])))
        self.image_tk = ImageTk.PhotoImage(self.image_resized)
        self.loaded_image = self.create_image(width/2, height/2, image=self.image_tk, anchor="center",)
        
    def calculate_scale(self,v_width,v_height):
        width_scale = v_width/self.loaded_width
        height_scale = v_height/self.loaded_height
        
        scaling_factor = min(width_scale, height_scale)
        scaled_width = self.loaded_width * scaling_factor
        scaled_height = self.loaded_height * scaling_factor
        if scaled_width <= v_width and scaled_height <= v_height:
            final_width = scaled_width
            final_height = scaled_height
        
        else:
        # The scaled image overflows the viewport, so we need to adjust the scaling
            final_width = self.loaded_width * min(width_scale, height_scale)
            final_height = self.loaded_height * min(width_scale, height_scale)
        
        return [final_width,final_height]
    
    def resize_image(self,event):
        size = self.calculate_scale(event.width,event.height)
        self.resized = self.image_resized.resize((int(size[0]),int(size[1])), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.resized)
        self.itemconfig(self.loaded_image, image=self.photo)
        self.coords(self.loaded_image, event.width / 2, event.height / 2)
        

class Menu (tk.Menu):
    def __init__(self,parent):
        super().__init__(parent)
        self.menubar = self
        parent.config(menu= self.menubar)
        self.FileMenu = tk.Menu(self.menubar,tearoff=0)
        self.FileMenu.add_command(label="Open",command=self.openFile)
        self.menubar.add_cascade(label="File", menu=self.FileMenu)
        
    def openFile(self):
        file_path = ctk.filedialog.askopenfilename(
        initialdir="/",  # Initial directory (change as needed)
            title="Select a file",
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")]
        )
        if file_path:
            app.load_new(file_path)
            # print("Selected file:", file_path)
        




if  __name__ == "__main__":
    if len(sys.argv) == 2:
        image_path = sys.argv[1]
        print(image_path)
        app = App(image_path)
        app.start()
    else:
        app = App()
        app.start()
        
        
        