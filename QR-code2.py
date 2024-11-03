import qrcode
import tkinter as tk
from tkinter import messagebox
def generate_qr_code():
    data = entry.get()
    if not data:
        messagebox.showerror("Error", "Please enter some data to generate a QR code.")
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save("qrcode.png")
    
    messagebox.showinfo("Success", "QR Code generated and saved as 'qrcode.png'")

root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x300")
root.config(bg="#ADD8E6")  

label = tk.Label(root, text="Enter data or URL:", bg="#ADD8E6", font=("Helvetica", 12))
label.pack(pady=10)

entry = tk.Entry(root, width=40, font=("Helvetica", 12))
entry.pack(pady=10)

generate_button = tk.Button(
    root, 
    text="Generate QR Code", 
    command=generate_qr_code,
    font=("Helvetica", 12),
    bg="#4CAF50",    
    fg="white",
    activebackground="#45a049",
    activeforeground="white",
    relief="raised",
    bd=3
)
generate_button.pack(pady=20)
root.mainloop()