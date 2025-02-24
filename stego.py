import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def encrypt_message():
    global img, password
    
    filepath = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.png")])
    if not filepath:
        return
    
    img = cv2.imread(filepath)
    if img is None:
        messagebox.showerror("Error", "Image not found!")
        return

    msg = msg_entry.get()
    password = password_entry.get()
    
    if not msg or not password:
        messagebox.showerror("Error", "Message and password cannot be empty!")
        return
    
    d = {chr(i): i for i in range(255)}
    rows, cols, _ = img.shape

    # Store message length in first pixel
    img[0, 0, 0] = len(msg)

    # Encrypt message
    n, m, z = 0, 1, 0  # Start from (0,1) to avoid overwriting length
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        m += 1
        if m >= cols:
            m = 0
            n += 1
        z = (z + 1) % 3

    cv2.imwrite("encryptedImage.jpg", img)
    os.system("encryptedImage.jpg")
    messagebox.showinfo("Success", "Message encrypted and saved!")

def decrypt_message():
    global img, password
    
    pas = password_entry.get()
    if password != pas:
        messagebox.showerror("Error", "Incorrect password!")
        return
    
    msg_length = img[0, 0, 0]
    c = {i: chr(i) for i in range(255)}

    # Decrypt message
    message = ""
    n, m, z = 0, 1, 0
    for i in range(msg_length):
        message += c[img[n, m, z]]
        m += 1
        if m >= img.shape[1]:
            m = 0
            n += 1
        z = (z + 1) % 3

    messagebox.showinfo("Decrypted Message", message)

# Create Tkinter Window
root = tk.Tk()
root.title("Image Steganography")
root.geometry("400x300")

# Input Fields
tk.Label(root, text="Enter Secret Message:").pack(pady=5)
msg_entry = tk.Entry(root, width=40)
msg_entry.pack(pady=5)

tk.Label(root, text="Enter Passcode:").pack(pady=5)
password_entry = tk.Entry(root, width=40, show="*")
password_entry.pack(pady=5)

# Buttons
tk.Button(root, text="Encrypt Message", command=encrypt_message).pack(pady=10)

tk.Label(root, text="Enter Passcode:").pack()
decrypt_password_entry = tk.Entry(root, width=40, show="*")
decrypt_password_entry.pack(pady=2)

tk.Button(root, text="Decrypt Message", command=decrypt_message).pack(pady=10)

root.mainloop()
