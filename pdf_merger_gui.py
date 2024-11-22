import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from PyPDF2 import PdfMerger

def browse_directory():
    """Open file dialog to select a directory and update the path textbox."""
    directory = filedialog.askdirectory()
    if directory:
        input_path_entry.delete(0, "end")
        input_path_entry.insert(0, directory)

def merge_pdfs():
    """Merge PDFs from the selected directory."""
    directory_path = input_path_entry.get()
    output_filename = output_name_entry.get()

    if not directory_path or not os.path.isdir(directory_path):
        messagebox.showerror("Error", "Please select a valid directory.")
        return

    if not output_filename.endswith(".pdf"):
        output_filename += ".pdf"

    output_file = os.path.join(directory_path, output_filename)

    try:
        merger = PdfMerger()
        for filename in sorted(os.listdir(directory_path)):
            if filename.endswith(".pdf"):
                file_path = os.path.join(directory_path, filename)
                merger.append(file_path)

        merger.write(output_file)
        merger.close()

        messagebox.showinfo("Success", f"Merged PDF saved as {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    # Creat GUI
    root = Tk()
    root.title("PDF Merger")
    root.geometry("500x300")

    # App title
    title_label = Label(root, text="PDF Merger", font=("Helvetica", 16))
    title_label.pack(pady=10)

    # Directory textbox and "Browse" button
    input_path_label = Label(root, text="Select Directory:")
    input_path_label.pack(anchor="w", padx=10)
    input_path_entry = Entry(root, width=50)
    input_path_entry.pack(padx=10, pady=5, anchor="w")
    browse_button = Button(root, text="Browse", command=browse_directory)
    browse_button.pack(padx=10, pady=5, anchor="w")

    # Textbox for output file Name
    output_name_label = Label(root, text="Output PDF Name:")
    output_name_label.pack(anchor="w", padx=10)
    output_name_entry = Entry(root, width=50)
    output_name_entry.pack(padx=10, pady=5, anchor="w")

    # Merge button
    merge_button = Button(root, text="Merge PDFs", command=merge_pdfs)
    merge_button.pack(padx=10, pady=5, anchor="w")

    root.mainloop()
