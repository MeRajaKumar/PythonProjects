import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import Image, ImageTk

# Function to generate QR code
def generate_qr():
    data = entry.get()
    
    if data:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill='black', back_color='white')
        
        img.save("qr_code.png")
        
        img = Image.open("qr_code.png")
        img = img.resize((200, 200))  
        img_tk = ImageTk.PhotoImage(img)
        qr_label.config(image=img_tk)
        qr_label.image = img_tk  

# Function to save the generated QR code
def save_qr():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        img = Image.open("qr_code.png")
        img.save(file_path)

# Function to reset all input and QR code display
def reset_all():
    entry.delete(0, tk.END)  
    qr_label.config(image='')  
    qr_label.image = None  

# Create the main window
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x550")

root.configure(bg="#DFF6F9")

label = tk.Label(root, text="Enter Data to Generate QR Code:", bg="#DFF6F9", font=("Arial", 12))
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
generate_button.pack(pady=10)

qr_label = tk.Label(root, bg="#DFF6F9")
qr_label.pack(pady=10)

save_button = tk.Button(root, text="Save QR Code", command=save_qr, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
save_button.pack(pady=10)

reset_button = tk.Button(root, text="Reset", command=reset_all, bg="#F44336", fg="white", font=("Arial", 10, "bold"))
reset_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
