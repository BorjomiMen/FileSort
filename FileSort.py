import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
from plyer import notification

class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Sorter")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#2C3E50")

        self.rules = self.load_rules()

        self.create_widgets()
    
    def load_rules(self):
        try:
            with open("rules.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                ".pdf": "Documents",
                ".docx": "Documents",
                ".xlsx": "Documents",
                ".txt": "Documents",
                ".jpg": "Images",
                ".png": "Images",
                ".gif": "Images",
                ".mp4": "Videos",
                ".avi": "Videos",
                ".mkv": "Videos",
                ".mp3": "Music",
                ".wav": "Music",
                ".flac": "Music"
            }

    def save_rules(self):
        with open("rules.json", "w") as f:
            json.dump(self.rules, f, indent=2)

    def create_widgets(self):

        folder_frame = tk.Frame(self.root, bg="#2C3E50")
        folder_frame.pack(pady=10, padx=10, fill="x")

        self.folder_path = tk.StringVar()
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path, width=60)
        self.folder_entry.pack(side="left", expand=True, fill="x")

        self.select_button = ttk.Button(folder_frame, text="📁 Выбрать", command=self.select_folder)
        self.select_button.pack(side="left", padx=5)


        rules_frame = tk.LabelFrame(self.root, text="Правила сортировки", bg="#2C3E50", fg="white")
        rules_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.rules_grid = tk.Frame(rules_frame, bg="#2C3E50")
        self.rules_grid.pack(pady=5, padx=5)

        self.rule_vars = []
        self.create_rules_table()

        button_frame = tk.Frame(self.root, bg="#2C3E50")
        button_frame.pack(pady=10)

        self.sort_button = ttk.Button(button_frame, text="🗂️ Сортировать", command=self.sort_files)
        self.sort_button.pack(side="left", padx=5)

        self.add_rule_button = ttk.Button(button_frame, text="➕ Добавить правило", command=self.add_rule)
        self.add_rule_button.pack(side="left", padx=5)

        self.save_rules_button = ttk.Button(button_frame, text="💾 Сохранить правила", command=self.save_rules)
        self.save_rules_button.pack(side="left", padx=5)


        log_frame = tk.LabelFrame(self.root, text="Лог действий", bg="#2C3E50", fg="white")
        log_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.log_text = ScrolledText(log_frame, height=10, bg="#1C1C1C", fg="white", wrap="word")
        self.log_text.pack(padx=5, pady=5, fill="both", expand=True)

    def create_rules_table(self):

        for widget in self.rules_grid.winfo_children():
            widget.destroy()


        tk.Label(self.rules_grid, text="Расширение", bg="#2C3E50", fg="white").grid(row=0, column=0, padx=5, sticky="w")
        tk.Label(self.rules_grid, text="Папка назначения", bg="#2C3E50", fg="white").grid(row=0, column=1, padx=5, sticky="w")
        tk.Label(self.rules_grid, text="", bg="#2C3E50").grid(row=0, column=2, padx=5)  # Для кнопки удаления


        self.rule_vars = []
        for i, (ext, folder) in enumerate(self.rules.items()):
            ext_var = tk.StringVar(value=ext)
            folder_var = tk.StringVar(value=folder)
            self.rule_vars.append((ext_var, folder_var))

            ttk.Entry(self.rules_grid, textvariable=ext_var, width=10).grid(row=i+1, column=0, padx=5, pady=2)
            ttk.Entry(self.rules_grid, textvariable=folder_var, width=20).grid(row=i+1, column=1, padx=5, pady=2)
            ttk.Button(self.rules_grid, text="❌", width=3, command=lambda idx=i: self.remove_rule(idx)).grid(row=i+1, column=2, padx=2)

    def add_rule(self):
        self.rule_vars.append((tk.StringVar(value=".ext"), tk.StringVar(value="NewFolder")))
        self.create_rules_table()

    def remove_rule(self, idx):
        if messagebox.askyesno("Удалить правило", "Вы уверены, что хотите удалить это правило?"):
            del self.rule_vars[idx]
            self.create_rules_table()

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)

    def sort_files(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Ошибка", "Выберите папку для сортировки!")
            return

        new_rules = {}
        for ext_var, folder_var in self.rule_vars:
            ext = ext_var.get().strip().lower()
            folder_name = folder_var.get().strip()
            if ext and folder_name:
                new_rules[ext] = folder_name
        self.rules = new_rules
        self.save_rules()

        moved_count = 0
        try:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename)
                    target_folder = self.rules.get(ext.lower(), "Other")
                    target_path = os.path.join(folder, target_folder)

                    os.makedirs(target_path, exist_ok=True)
                    shutil.move(file_path, os.path.join(target_path, filename))
                    self.log_text.insert(tk.END, f"✅ Файл '{filename}' перемещён в '{target_folder}'\n")
                    moved_count += 1
            if moved_count == 0:
                self.log_text.insert(tk.END, "ℹ️ Нет файлов для сортировки\n")
            else:
                self.log_text.insert(tk.END, f"🎉 Завершено! Перемещено {moved_count} файлов\n")
                notification.notify(
                    title="File Sorter",
                    message=f"Сортировка завершена! Перемещено {moved_count} файлов.",
                    timeout=10
                )
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сортировке файлов:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()