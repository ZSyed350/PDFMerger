import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, StringVar, OptionMenu
from PyPDF2 import PdfMerger

def browse_directory():
    """Open file dialog to select a directory and update the path textbox."""
    directory = filedialog.askdirectory()
    if directory:
        input_path_entry.delete(0, "end")
        input_path_entry.insert(0, directory)

def get_ordered_files(dir, sort_by="alphabetically"):
    """
    Sorts a list of files based on the user's choice.
    
    Args:
        dir (str): Directory containing PDFs to merge.
        sort_by (str): Sorting criteria. Options are:
                       - "alphabetically"
                       - "date_newest_first"
                       - "date_oldest_first"
                       
    Returns:
        list: Sorted list of file paths.
    """
    file_list = os.listdir(dir)
    file_list_fp = [os.path.join(dir, file) for file in file_list]  # file_list but with full paths
    if sort_by == "alphabetically":
        return sorted(file_list)
    elif sort_by == "date_newest_first":
        return sorted(file_list_fp, key=os.path.getmtime, reverse=True)
    elif sort_by == "date_oldest_first":
        return sorted(file_list_fp, key=os.path.getmtime)
    else:
        raise ValueError("Invalid sort_by option. Choose from 'alphabetically', 'date_newest_first', or 'date_oldest_first'.")

def merge_pdfs():
    """Merge PDFs from the selected directory."""
    directory_path = input_path_entry.get()
    output_filename = output_name_entry.get()
    sort_by = sort_by_var.get()  # Get the sort_by value from the drop-down

    if not directory_path or not os.path.isdir(directory_path):
        messagebox.showerror("Error", "Please select a valid directory.")
        return

    if not output_filename.endswith(".pdf"):
        output_filename += ".pdf"

    output_file = os.path.join(directory_path, output_filename)

    try:
        merger = PdfMerger()
        for filename in get_ordered_files(directory_path, sort_by=sort_by):
            if filename.endswith(".pdf"):
                file_path = os.path.join(directory_path, filename)
                merger.append(file_path)

        merger.write(output_file)
        merger.close()

        messagebox.showinfo("Success", f"Merged PDF saved as {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    # Create GUI
    root = Tk()
    root.title("PDF Merger")
    root.geometry("500x350")

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

    # Sorting options drop-down
    sort_by_label = Label(root, text="Sort Files By:")
    sort_by_label.pack(anchor="w", padx=10)
    sort_by_var = StringVar(value="alphabetically")  # Default option
    sort_by_options = ["alphabetically", "date_newest_first", "date_oldest_first"]
    sort_by_menu = OptionMenu(root, sort_by_var, *sort_by_options)
    sort_by_menu.pack(padx=10, pady=5, anchor="w")

    # Textbox for output file name
    output_name_label = Label(root, text="Output PDF Name:")
    output_name_label.pack(anchor="w", padx=10)
    output_name_entry = Entry(root, width=50)
    output_name_entry.pack(padx=10, pady=5, anchor="w")

    # Merge button
    merge_button = Button(root, text="Merge PDFs", command=merge_pdfs)
    merge_button.pack(padx=10, pady=5, anchor="w")

    root.mainloop()
