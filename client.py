import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox
import requests

SERVER_URL = "http://127.0.0.1:5000"
CACHE_FILE = "cache.csv"
FIELDNAMES = ["id", "name", "category", "quantity", "price", "location", "created_at"]


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Облік товарів (Клієнт)")
        self.root.geometry("850x550")

        self.create_menu()
        self.create_widgets()
        
        # Завантаження даних при старті
        self.load_data()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        sync_menu = tk.Menu(menubar, tearoff=0)
        sync_menu.add_command(label="Синхронізувати зараз", command=self.sync_now)
        sync_menu.add_command(label="Експорт CSV (з сервера)", command=self.export_csv)
        menubar.add_cascade(label="Меню", menu=sync_menu)
        
        self.root.config(menu=menubar)

    def create_widgets(self):
        # Фрейм для форми введення
        form_frame = ttk.LabelFrame(self.root, text="Дані товару")
        form_frame.pack(fill="x", padx=10, pady=10)

        labels = ["Назва:", "Категорія:", "Кількість:", "Ціна:", "Локація:"]
        self.entries = {}

        for i, label in enumerate(labels):
            lbl = ttk.Label(form_frame, text=label)
            lbl.grid(row=0, column=i*2, padx=5, pady=5, sticky="w")
            ent = ttk.Entry(form_frame, width=12)
            ent.grid(row=0, column=i*2+1, padx=5, pady=5)
            key = ["name", "category", "quantity", "price", "location"][i]
            self.entries[key] = ent

        # Приховане поле для ID обраного рядка
        self.selected_id = tk.StringVar()

        # Кнопки CRUD
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Додати", command=self.add_item).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Оновити", command=self.update_item).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Видалити", command=self.delete_item).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Очистити форму", command=self.clear_form).pack(side="left", padx=5)

        # Таблиця (Treeview)
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(table_frame, columns=FIELDNAMES, show="headings")
        for col in FIELDNAMES:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=110)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # Статус-бар
        self.status_var = tk.StringVar()
        self.status_var.set("Готово до роботи.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")

    def set_status(self, message, is_error=False):
        self.status_var.set(message)

    def save_to_cache(self, items):
        """Зберігає список товарів у локальний кеш."""
        try:
            with open(CACHE_FILE, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writeheader()
                for item in items:
                    writer.writerow(item)
        except Exception as e:
            print(f"Помилка збереження кешу: {e}")

    def load_from_cache(self):
        """Завантажує товари з локального кешу."""
        items = []
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    items.append(row)
        return items

    def update_table(self, items):
        """Оновлює графічний інтерфейс таблиці."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in items:
            self.tree.insert("", "end", values=list(item.values()))

    def load_data(self):
        """Завантажує дані з сервера або переходить в офлайн-режим."""
        try:
            response = requests.get(f"{SERVER_URL}/items", timeout=3)
            if response.status_code == 200:
                items = response.json()
                self.save_to_cache(items)
                self.update_table(items)
                self.set_status("Статус: Онлайн (дані завантажено з сервера).")
            else:
                self.handle_server_error(response)
        except requests.exceptions.RequestException:
            # Офлайн режим
            items = self.load_from_cache()
            self.update_table(items)
            self.set_status("Статус: Офлайн-режим (сервер недоступний, завантажено з cache.csv).", is_error=True)

    def handle_server_error(self, response):
        try:
            err_msg = response.json().get("error", "Помилка сервера")
        except:
            err_msg = f"Код помилки: {response.status_code}"
        self.set_status(f"Помилка: {err_msg}", is_error=True)

    def add_item(self):
        data = self.get_form_data()
        if not data:
            return
        try:
            response = requests.post(f"{SERVER_URL}/items", json=data, timeout=3)
            if response.status_code == 201:
                self.set_status("Товар успішно додано через API.")
                self.clear_form()
                self.load_data()
            else:
                self.handle_server_error(response)
        except requests.exceptions.RequestException:
            self.set_status("Помилка: Сервер недоступний для додавання запису.", is_error=True)

    def update_item(self):
        item_id = self.selected_id.get()
        if not item_id:
            messagebox.showwarning("Увага", "Оберіть товар для оновлення!")
            return
        data = self.get_form_data()
        if not data:
            return
        try:
            response = requests.put(f"{SERVER_URL}/items/{item_id}", json=data, timeout=3)
            if response.status_code == 200:
                self.set_status(f"Товар ID {item_id} успішно оновлено.")
                self.clear_form()
                self.load_data()
            else:
                self.handle_server_error(response)
        except requests.exceptions.RequestException:
            self.set_status("Помилка: Сервер недоступний для оновлення запису.", is_error=True)

    def delete_item(self):
        item_id = self.selected_id.get()
        if not item_id:
            messagebox.showwarning("Увага", "Оберіть товар для видалення!")
            return
        try:
            response = requests.delete(f"{SERVER_URL}/items/{item_id}", timeout=3)
            if response.status_code == 200:
                self.set_status(f"Товар ID {item_id} видалено.")
                self.clear_form()
                self.load_data()
            else:
                self.handle_server_error(response)
        except requests.exceptions.RequestException:
            self.set_status("Помилка: Сервер недоступний для видалення.", is_error=True)

    def get_form_data(self):
        try:
            name = self.entries["name"].get().strip()
            category = self.entries["category"].get().strip()
            quantity_str = self.entries["quantity"].get().strip()
            price_str = self.entries["price"].get().strip()
            location = self.entries["location"].get().strip()

            if not name or not category:
                raise ValueError("Назва та категорія обов'язкові.")

            quantity = int(quantity_str)
            price = float(price_str)

            return {
                "name": name,
                "category": category,
                "quantity": quantity,
                "price": price,
                "location": location
            }
        except ValueError as e:
            self.set_status(f"Помілка валідації: {e}", is_error=True)
            messagebox.showerror("Помилка", f"Перевірте коректність полів:\n- Кількість має бути цілим числом\n- Ціна має бути числом\n({e})")
            return None

    def on_row_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item_values = self.tree.item(selected_items[0], "values")
            self.selected_id.set(item_values[0])
            
            # Заповнюємо поля форми даними з вибраного рядка
            keys = ["name", "category", "quantity", "price", "location"]
            # item_values іде як [id, name, category, quantity, price, location, created_at]
            mapping = [1, 2, 3, 4, 5]
            for key, idx in zip(keys, mapping):
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, item_values[idx])

    def clear_form(self):
        self.selected_id.set("")
        for ent in self.entries.values():
            ent.delete(0, tk.END)

    def sync_now(self):
        """Примусова синхронізація."""
        self.load_data()
        self.set_status("Синхронізацію виконано успішно.")

    def export_csv(self):
        """Запитує у сервера актуальний файл і зберігає локально."""
        try:
            response = requests.get(f"{SERVER_URL}/items", timeout=3)
            if response.status_code == 200:
                items = response.json()
                self.save_to_cache(items)
                messagebox.info("Експорт", "Актуальні дані успішно завантажено та збережено у локальний кеш!")
                self.set_status("Експорт CSV виконано успішно.")
            else:
                self.handle_server_error(response)
        except requests.exceptions.RequestException:
            self.set_status("Помилка: Не вдалося підключитися до сервера для експорту.", is_error=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()