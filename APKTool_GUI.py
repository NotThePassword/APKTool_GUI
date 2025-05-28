import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading

class APKToolGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("APKTool GUI")
        
        # Variables for file paths and options
        self.apk_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.recompiled_apk_file = tk.StringVar()
        self.apktool_jar_path = tk.StringVar()
        self.framework_file = tk.StringVar()
        self.recompiled_apk_file.set("recompiled.apk")
        
        # Options for decompiling
        self.verbose = tk.BooleanVar()
        self.force_overwrite = tk.BooleanVar()
        self.no_src = tk.BooleanVar()
        self.no_res = tk.BooleanVar()
        self.no_xml = tk.BooleanVar()
        self.decrypt = tk.BooleanVar()
        self.no_decrypt = tk.BooleanVar()
        
        # Options for recompiling
        self.recompile_verbose = tk.BooleanVar()
        self.recompile_force_overwrite = tk.BooleanVar()
        self.recompile_no_src = tk.BooleanVar()
        self.recompile_no_res = tk.BooleanVar()
        
        # GUI widgets
        # File selection
        tk.Label(master, text="APK File:").pack()
        self.apk_file_entry = tk.Entry(master, textvariable=self.apk_file)
        self.apk_file_entry.pack()
        self.browse_apk_button = tk.Button(master, text="Browse", command=self.browse_apk_file)
        self.browse_apk_button.pack()
        
        tk.Label(master, text="Output Directory:").pack()
        self.output_dir_entry = tk.Entry(master, textvariable=self.output_dir)
        self.output_dir_entry.pack()
        self.browse_output_dir_button = tk.Button(master, text="Browse", command=self.browse_output_dir)
        self.browse_output_dir_button.pack()
        
        tk.Label(master, text="Recompiled APK File:").pack()
        self.recompiled_apk_file_entry = tk.Entry(master, textvariable=self.recompiled_apk_file)
        self.recompiled_apk_file_entry.pack()
        self.browse_recompiled_apk_button = tk.Button(master, text="Browse", command=self.browse_recompiled_apk_file)
        self.browse_recompiled_apk_button.pack()
        
        # Options for decompiling
        tk.Checkbutton(master, text="Verbose (Decompile)", variable=self.verbose).pack()
        tk.Checkbutton(master, text="Force Overwrite (Decompile)", variable=self.force_overwrite).pack()
        tk.Checkbutton(master, text="No Source Code (Decompile)", variable=self.no_src).pack()
        tk.Checkbutton(master, text="No Resources (Decompile)", variable=self.no_res).pack()
        tk.Checkbutton(master, text="No XML Parsing (Decompile)", variable=self.no_xml).pack()
        tk.Checkbutton(master, text="No Decryption (Decompile)", variable=self.no_decrypt).pack()
        
        # Framework file for decompiling
        tk.Label(master, text="Framework File:").pack()
        self.framework_file_entry = tk.Entry(master, textvariable=self.framework_file)
        self.framework_file_entry.pack()
        self.browse_framework_file_button = tk.Button(master, text="Browse", command=self.browse_framework_file)
        self.browse_framework_file_button.pack()
        
        # Options for recompiling
        tk.Checkbutton(master, text="Verbose (Recompile)", variable=self.recompile_verbose).pack()
        tk.Checkbutton(master, text="Force Overwrite (Recompile)", variable=self.recompile_force_overwrite).pack()
        tk.Checkbutton(master, text="No Source Code (Recompile)", variable=self.recompile_no_src).pack()
        tk.Checkbutton(master, text="No Resources (Recompile)", variable=self.recompile_no_res).pack()
        
        # APKTool jar path
        tk.Label(master, text="APKTool Jar Path:").pack()
        self.apktool_jar_path_entry = tk.Entry(master, textvariable=self.apktool_jar_path)
        self.apktool_jar_path_entry.pack()
        self.browse_apktool_jar_button = tk.Button(master, text="Browse", command=self.browse_apktool_jar)
        self.browse_apktool_jar_button.pack()
        
        # Buttons for actions
        self.decompile_button = tk.Button(master, text="Decompile APK", command=self.decompile_apk)
        self.decompile_button.pack()
        self.recompile_button = tk.Button(master, text="Recompile APK", command=self.recompile_apk)
        self.recompile_button.pack()
        self.view_file_button = tk.Button(master, text="View File", command=self.view_file)
        self.view_file_button.pack()
        self.edit_file_button = tk.Button(master, text="Edit File", command=self.select_file_to_edit)
        self.edit_file_button.pack()
        
        # Status and progress
        self.status_label = tk.Label(master, text="Ready")
        self.status_label.pack()
        self.progress_bar = ttk.Progressbar(master, mode='indeterminate')
        self.progress_bar.pack()
        
        # Busy flag to prevent multiple operations
        self.is_busy = False
        
    def browse_apk_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")])
        if file_path:
            self.apk_file.set(file_path)
    
    def browse_output_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir.set(dir_path)
    
    def browse_recompiled_apk_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".apk")
        if file_path:
            self.recompiled_apk_file.set(file_path)
    
    def browse_framework_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")])
        if file_path:
            self.framework_file.set(file_path)
    
    def browse_apktool_jar(self):
        file_path = filedialog.askopenfilename(filetypes=[("JAR files", "*.jar")])
        if file_path:
            self.apktool_jar_path.set(file_path)
    
    def view_file(self):
        # Get the output directory
        output_dir = self.output_dir.get()
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory first.")
            return
        # Ask to select a file from that directory
        file_path = filedialog.askopenfilename(initialdir=output_dir)
        if not file_path:
            return
        # Open a new window with the file content
        view_window = tk.Toplevel(self.master)
        view_window.title(f"Viewing {file_path}")
        
        text_widget = tk.Text(view_window)
        text_widget.pack()
        
        # Read the file content
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            text_widget.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
    
    def select_file_to_edit(self):
        # Get the output directory
        output_dir = self.output_dir.get()
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory first.")
            return
        # Ask to select a file from that directory
        file_path = filedialog.askopenfilename(initialdir=output_dir)
        if not file_path:
            return
        # Open a new window for editing
        edit_window = tk.Toplevel(self.master)
        edit_window.title(f"Editing {file_path}")
        
        text_widget = tk.Text(edit_window)
        text_widget.pack()
        
        # Read the file content
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            text_widget.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
        
        # Save button
        save_button = tk.Button(edit_window, text="Save", command=lambda: self.save_edited_file(text_widget.get("1.0", tk.END), file_path))
        save_button.pack()
    
    def save_edited_file(self, new_content, file_path):
        try:
            with open(file_path, 'w') as f:
                f.write(new_content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def toggle_controls(self, is_enabled):
        state = tk.NORMAL if is_enabled else tk.DISABLED
        self.apk_file_entry.config(state=tk.NORMAL if is_enabled else tk.DISABLED)
        self.output_dir_entry.config(state=tk.NORMAL if is_enabled else tk.DISABLED)
        self.recompiled_apk_file_entry.config(state=tk.NORMAL if is_enabled else tk.DISABLED)
        self.browse_apk_button.config(state=tk.NORMAL if is_enabled else tk.DISABLED)
        self.browse_output_dir_button.config(state=tk.NORMAL if is_enabled else tk.DISABLED)
        self.browse_recompiled_apk_button.config(state=tk.NORMAL if is_enabled else tk.DISABLED)
        self.decompile_button.config(state=tk.NORMAL if is_enabled else tk.DISABLED)
        self.recompile_button.config(state=tk.NORMAL if is_enabled else tk.DISABLED)
        self.view_file_button.config(state=tk.NORMAL if is_enabled else tk.DISABLED)
        self.edit_file_button.config(state=tk.NORMAL if is_enabled else tk.DISABLED)
    
    def decompile_apk(self):
        if not self.is_busy:
            # Disable controls
            self.toggle_controls(is_enabled=False)
            self.is_busy = True
            threading.Thread(target=self.decompile_apk_thread).start()
    
    def decompile_apk_thread(self):
        # Construct the command for decompiling
        if self.apktool_jar_path.get():
            command = ["java", "-jar", self.apktool_jar_path.get(), "d", self.apk_file.get(), "-o", self.output_dir.get()]
        else:
            command = ["apktool", "d", self.apk_file.get(), "-o", self.output_dir.get()]
        
        # Add options
        if self.verbose.get():
            command.append("-v")
        if self.force_overwrite.get():
            command.append("--force")
        if self.no_src.get():
            command.append("--no-src")
        if self.no_res.get():
            command.append("--no-res")
        if self.no_xml.get():
            command.append("--no-xml")
        if self.decrypt.get():
            command.append("--decrypt")
        if self.no_decrypt.get():
            command.append("--no-decrypt")
        if self.framework_file.get():
            command.extend(["--system", self.framework_file.get()])
        
        # Show progress
        self.status_label.config(text="Decompiling...")
        self.progress_bar.start()
        
        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", "Decompilation completed successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Decompilation failed: {e}")
        finally:
            # Enable controls
            self.progress_bar.stop()
            self.status_label.config(text="Ready")
            self.toggle_controls(is_enabled=True)
            self.is_busy = False
    
    def recompile_apk(self):
        if not self.is_busy:
            # Disable controls
            self.toggle_controls(is_enabled=False)
            self.is_busy = True
            threading.Thread(target=self.recompile_apk_thread).start()
    
    def recompile_apk_thread(self):
        # Construct the command for recompiling
        if self.apktool_jar_path.get():
            command = ["java", "-jar", self.apktool_jar_path.get(), "b", self.output_dir.get(), "-o", self.recompiled_apk_file.get()]
        else:
            command = ["apktool", "b", self.output_dir.get(), "-o", self.recompiled_apk_file.get]
        
        # Add options
        if self.recompile_verbose.get():
            command.append("-v")
        if self.recompile_force_overwrite.get():
            command.append("--force")
        if self.recompile_no_src.get():
            command.append("--no-src")
        if self.recompile_no_res.get():
            command.append("--no-res")
        
        # Show progress
        self.status_label.config(text="Recompiling...")
        self.progress_bar.start()
        
        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", "Recompilation completed successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Recompilation failed: {e}")
        finally:
            # Enable controls
            self.progress_bar.stop()
            self.status_label.config(text="Ready")
            self.toggle_controls(is_enabled=True)
            self.is_busy = False

if __name__ == "__main__":
    root = tk.Tk()
    app = APKToolGUI(root)
    root.mainloop()
