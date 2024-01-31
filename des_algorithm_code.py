# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 17:49:34 2023

@author: Reyyan
"""

import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image
from io import BytesIO
from pyDes import des, PAD_PKCS5

class EncryptionApp:
    def __init__(self, master):
        initial_width=500
        initial_heigth=400
        root.geometry(f'{initial_width}x{initial_heigth}+30+30')
        root.resizable(True,True)
        root.configure(bg ='#87ceeb')
        self.master = master
        master.title("Encryption App")

        self.label = tk.Label(master, text="What would you like to encrypt?",font='Times 18 bold',fg='Black', bg ='#87ceeb').place(x=90,y=40)


        self.text_button = tk.Button(master, text="Text", command=self.encrypt_text,font='Times 15 ', bg='#e0ffff').place(x=140,y=170)


        self.image_button = tk.Button(master, text="Image", command=self.encrypt_image,font='Times 15 ',bg='#e0ffff').place(x=200,y=170)


        self.decrypt_image_button = tk.Button(master, text="Decrypt Image", command=self.decrypt_and_display_image,font='Times 15 ',bg='#e0ffff').place(x=270,y=170)


        self.key_label = tk.Label(master, text="Enter the key (8 characters):",font='Times 10 ',bg ='#87ceeb').place(x=110,y=100)


        self.key_entry = tk.Entry(master, show="*", bg ='#87ceeb')
        self.key_entry.place(x=270,y=102)

        self.output_label = tk.Label(master, text="",font='Times 10 ',bg ='#87ceeb')
        self.output_label.place(x=110,y=220)

    def pad_text(self, text):
        padding_size = 8 - (len(text) % 8)
        padded_text = text + bytes([padding_size] * padding_size)
        return padded_text

    def encrypt_text_with_des(self, text, key):
        d = des(key, PAD_PKCS5)
        encrypted_text = d.encrypt(text)
        return encrypted_text

    def decrypt_text_with_des(self, encrypted_text, key):
        d = des(key, PAD_PKCS5)
        decrypted_text = d.decrypt(encrypted_text)
        return decrypted_text

    def encrypt_text(self):
        text_to_encrypt = self.get_input("Enter the text to encrypt:")
        key = self.get_key()

        padded_text_to_encrypt = self.pad_text(text_to_encrypt.encode())
        encrypted_text = self.encrypt_text_with_des(padded_text_to_encrypt, key)

        decrypted_text = self.decrypt_text_with_des(encrypted_text, key)

        self.show_output(f"Encrypted Text: {encrypted_text}\nDecrypted Text: {decrypted_text.decode()}")

    def encrypt_image_with_des(self, image_path, key, encrypted_image_path):
        image = Image.open(image_path)

        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()

        padded_image_bytes = self.pad_text(image_bytes)
        d = des(key, PAD_PKCS5)
        encrypted_image = d.encrypt(padded_image_bytes)

        with open(encrypted_image_path, 'wb') as f:
            f.write(encrypted_image)

        self.show_output(f"Encrypted image saved successfully: {encrypted_image_path}")

    def decrypt_image_with_des(self, encrypted_image_path, key, output_path):
        with open(encrypted_image_path, 'rb') as f:
            encrypted_image = f.read()

        d = des(key, PAD_PKCS5)
        decrypted_image_bytes = d.decrypt(encrypted_image)


        padding_size = decrypted_image_bytes[-1]
        decrypted_image_bytes = decrypted_image_bytes[:-padding_size]
 
        decrypted_image = Image.open(BytesIO(decrypted_image_bytes))
        decrypted_image.save(output_path, format='PNG')

        self.show_output(f"Decrypted image saved successfully: {output_path}")

    def encrypt_image(self):
        image_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.png")])
        encrypted_image_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("txt files", "*.txt")])
        key = self.get_key()

        if image_path and encrypted_image_path and key:
            self.encrypt_image_with_des(image_path, key, encrypted_image_path)

    def decrypt_and_display_image(self):
        encrypted_image_path = filedialog.askopenfilename(title="Select an encrypted image file", filetypes=[("txt files", "*.txt")])
        key = self.get_key()

        if encrypted_image_path and key:
            decrypted_image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image files", "*.png")])
            self.decrypt_image_with_des(encrypted_image_path, key, decrypted_image_path)

    def get_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

    def get_key(self):
        key = self.key_entry.get().encode()
        if len(key) != 8:
            self.show_output("Invalid key length. Please enter 8 characters.")
            return None
        return key

    def show_output(self, message):
        self.output_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
