import customtkinter as ctk
import importer

def run():
    app = ctk.CTk()
    app.title("Limpe - Higienização Tributária")
    
    def upload_file():
        file_path = ctk.filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        if file_path:
            importer.process_file(file_path)
    
    upload_button = ctk.CTkButton(app, text="Upload Arquivo", command=upload_file)
    upload_button.pack(pady=20)
    
    app.mainloop()
