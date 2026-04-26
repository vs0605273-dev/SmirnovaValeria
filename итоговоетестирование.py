import random
import string
import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        self.history_file = "history.json"
        self.history = self.load_history()
        self.create_widgets()
        self.update_history_table()
    
    def create_widgets(self):
        settings_frame = ttk.LabelFrame(self.root, text="Настройки пароля", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky="w", pady=5)
        self.length_var = tk.IntVar(value=12)
        self.length_spinbox = ttk.Spinbox(settings_frame, from_=4, to=128, textvariable=self.length_var, width=10)
        self.length_spinbox.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        ttk.Label(settings_frame, text="(мин: 4, макс: 128)").grid(row=0, column=2, sticky="w", pady=5)
        
        ttk.Label(settings_frame, text="Использовать:").grid(row=1, column=0, sticky="w", pady=5)
        
        self.use_lowercase = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Строчные буквы (a-z)", variable=self.use_lowercase).grid(row=1, column=1, sticky="w", padx=10)
        
        self.use_uppercase = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Заглавные буквы (A-Z)", variable=self.use_uppercase).grid(row=2, column=1, sticky="w", padx=10)
        
        self.use_digits = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=self.use_digits).grid(row=3, column=1, sticky="w", padx=10)
        
        self.use_special = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Спецсимволы (!@#$%^&*)", variable=self.use_special).grid(row=4, column=1, sticky="w", padx=10)
        
        self.generate_btn = ttk.Button(settings_frame, text="Сгенерировать пароль!", command=self.generate_password)
        self.generate_btn.grid(row=5, column=0, columnspan=3, pady=10)
        
        password_frame = ttk.LabelFrame(self.root, text="Сгенерированный пароль", padding=10)
        password_frame.pack(fill="x", padx=10, pady=5)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, font=("Courier", 12), state="readonly")
        self.password_entry.pack(fill="x", padx=5, pady=5)
        
        self.copy_btn = ttk.Button(password_frame, text="Копировать в буфер обмена", command=self.copy_to_clipboard)
        self.copy_btn.pack(pady=5)
        
        history_frame = ttk.LabelFrame(self.root, text="История паролей", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("Время", "Пароль", "Длина", "Тип")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)
        
        self.tree.heading("Время", text="Время")
        self.tree.heading("Пароль", text="Пароль")
        self.tree.heading("Длина", text="Длина")
        self.tree.heading("Тип", text="Тип")
        
        self.tree.column("Время", width=150)
        self.tree.column("Пароль", width=250)
        self.tree.column("Длина", width=60)
        self.tree.column("Тип", width=100)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        button_frame = ttk.Frame(history_frame)
        button_frame.pack(fill="x", pady=5)
        
        ttk.Button(button_frame, text="Очистить историю", command=self.clear_history).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Обновить", command=self.update_historyble).pack(side="left", padx=5)
    
    def generate_password(self):
        try:
            length = self.length_var.get()
        except tk.TclError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число для длины пароля")
            return
        
        if length < 4:
            messagebox.showerror("Ошибка", "Длина пароля должна быть не менее 4 символов")
            return
        if length > 128:
            messagebox.showerror("Ошибка", "Длина пароля не должна превышать 128 символов")
            return
        
        if not (self.use_lowercase.get() or self.use_uppercase.get() or self.use_digits.get() or self.use_special.get()):
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
            return
        
        characters = ""
        selected_types = []
        
        if self.use_lowercase.get():
            characters += string.ascii_lowercase
            selected_types.append("строчные")
        if self.use_uppercase.get():
            characters += string.ascii_uppercase
            selected_types.append("заглавные")
        if self.use_digits.get():
            characters += string.digits
            selected_types.append("цифры")
        if self.use_special.get():
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            selected_types.append("спецсимволы")
        
        try:
            password = ''.join(random.choice(characters) for _ in range(length))
            self.password_var.set(password)
            self.save_to_history(password, length, selected_types)
            self.update_history_table()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сгенерировать пароль: {str(e)}")
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Внимание", "Нет пароля для копирования")
    
    def save_to_history(self, password, length, selected_types):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        types_str = ", ".join(selected_types)
        
        self.history.append({
            "timestamp": timestamp,
            "password": password,
            "length": length,
            "types": types_str
        })
        
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        self.save_history()
    
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except IOError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {str(e)}")
    
    def update_history_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for entry in reversed(self.history):
            self.tree.insert("", "end", values=(
                entry["timestamp"],
                entry["password"],
                entry["length"],
                entry["types"]
            ))
    
    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_table()
            messagebox.showinfo("Успех", "История очищена")

def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
