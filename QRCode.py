import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import Image, ImageTk

# Function to generate QR code
def generate_qr():
    # Get the input data from the text entry box
    data = entry.get()
    
    if data:
        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create the QR code image
        img = qr.make_image(fill='black', back_color='white')
        
        # Save the image to a temporary file
        img.save("qr_code.png")
        
        # Display the QR code in the GUI
        img = Image.open("qr_code.png")
        img = img.resize((200, 200))  # Resize to fit in the GUI
        img_tk = ImageTk.PhotoImage(img)
        qr_label.config(image=img_tk)
        qr_label.image = img_tk  # Keep a reference to avoid garbage collection

# Function to save the generated QR code
def save_qr():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        img = Image.open("qr_code.png")
        img.save(file_path)

# Create the main window
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x400")

# Create a label, entry, and button for input
label = tk.Label(root, text="Enter data to generate QR code:")
label.pack(pady=10)

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr)
generate_button.pack(pady=10)

# Label to display the generated QR code
qr_label = tk.Label(root)
qr_label.pack(pady=10)

# Button to save the QR code
save_button = tk.Button(root, text="Save QR Code", command=save_qr)
save_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
