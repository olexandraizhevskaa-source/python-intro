import csv
from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class InventoryRepo:

  def __init__(self):
    self.path, self.items = None, []

  def load(self, path):
    self.path, self.items = path, []
    with open(path, encoding="utf-8-sig") as f:
      for r in csv.DictReader(f):
        r["quantity"] = int(r["quantity"]) if r["quantity"].isdigit() else 0
        r["price"] = float(str(r["price"]).replace(",", "."))
        self.items.append(r)

  def save(self, path=None):
    if path:
      self.path = path
    fields = [
        "id",
        "name",
        "category",
        "quantity",
        "price",
        "location",
        "created_at",
    ]
    with open(self.path, "w", encoding="utf-8", newline="") as f:
      w = csv.DictWriter(f, fieldnames=fields)
      w.writeheader()
      w.writerows(self.items)


class App:

  def __init__(self, root):
    self.root = root
    self.root.title("Облік")
    self.root.geometry("900x550")
    self.repo, self.file, self.sort_col, self.sort_rev = InventoryRepo(), None, None, False

    m = tk.Menu(root)
    fm = tk.Menu(m, tearoff=0)
    fm.add_command(label="Відкрити...", command=self.open_f)
    fm.add_command(label="Зберегти", command=self.save_f)
    fm.add_command(label="Зберегти як...", command=self.save_as_f)
    m.add_cascade(label="Файл", menu=fm)
    root.config(menu=m)

    f = ttk.Frame(root, padding=10)
    f.pack(fill=tk.BOTH, expand=True)

    sf = ttk.Frame(f)
    sf.pack(fill=tk.X, pady=5)
    ttk.Label(sf, text="Пошук:").pack(side=tk.LEFT)
    self.sv = tk.StringVar()
    self.sv.trace_add("write", lambda *_: self.update_table())
    ttk.Entry(sf, textvariable=self.sv, width=25).pack(side=tk.LEFT, padx=5)

    cf = ttk.Frame(f)
    cf.pack(fill=tk.BOTH, expand=True)

    cols = ("id", "name", "category", "quantity", "price", "location", "created_at")
    self.tree = ttk.Treeview(cf, columns=cols, show="headings")
    for c in cols:
      self.tree.heading(c, text=c, command=lambda _c=c: self.sort(_c))
      self.tree.column(c, width=100)
    self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    self.tree.bind("<<TreeviewSelect>>", self.select_item)

    ff = ttk.LabelFrame(cf, text=" Дані ", padding=10)
    ff.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

    self.entries = {}
    for k in cols[:-1]:
      ttk.Label(ff, text=k).pack(anchor=tk.W)
      e = ttk.Entry(ff)
      e.pack(fill=tk.X, pady=2)
      self.entries[k] = e

    ttk.Button(ff, text="Додати", command=self.add).pack(fill=tk.X, pady=2)
    ttk.Button(ff, text="Оновити", command=self.update).pack(fill=tk.X, pady=2)
    ttk.Button(ff, text="Видалити", command=self.delete).pack(fill=tk.X, pady=2)
    ttk.Button(ff, text="Очистити", command=self.clear).pack(fill=tk.X, pady=2)

    self.status = tk.StringVar(value="Готово")
    ttk.Label(f, textvariable=self.status, relief=tk.SUNKEN).pack(
        fill=tk.X, pady=5
    )

  def update_table(self):
    q = self.sv.get().lower()
    items = [
        i
        for i in self.repo.items
        if q in i["name"].lower() or q in i["category"].lower()
    ]
    if self.sort_col:
      items.sort(
          key=lambda x: x[self.sort_col], reverse=self.sort_rev
      )
    for r in self.tree.get_children():
      self.tree.delete(r)
    for i in items:
      self.tree.insert("", tk.END, values=list(i.values()))

  def sort(self, col):
    self.sort_rev = not self.sort_rev if self.sort_col == col else False
    self.sort_col = col
    self.update_table()

  def get_data(self):
    d = {k: e.get().strip() for k, e in self.entries.items()}
    if not d["name"] or not d["category"]:
      self.status.set("Помилка: Назва та категорія обов'язкові!")
      return None
    try:
      d["quantity"] = int(d["quantity"])
      d["price"] = float(d["price"].replace(",", "."))
    except ValueError:
      self.status.set("Помилка в числі!")
      return None
    if not d["id"]:
      d["id"] = str(
          max([int(x["id"]) for x in self.repo.items if x["id"].isdigit()] or [0])
          + 1
      )
    d["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return d

  def add(self):
    d = self.get_data()
    if d:
      self.repo.items.append(d)
      self.update_table()
      self.clear()
      self.status.set("Додано.")

  def update(self):
    sel = self.tree.selection()
    if not sel:
      return
    id_val = self.tree.item(sel[0], "values")[0]
    d = self.get_data()
    if d:
      for i, item in enumerate(self.repo.items):
        if str(item["id"]) == str(id_val):
          d["created_at"] = item["created_at"]
          self.repo.items[i] = d
      self.update_table()
      self.status.set("Оновлено.")

  def delete(self):
    sel = self.tree.selection()
    if sel and messagebox.askyesno("Видалити?", "Точно видалити?"):
      id_val = self.tree.item(sel[0], "values")[0]
      self.repo.items = [i for i in self.repo.items if str(i["id"]) != str(id_val)]
      self.update_table()
      self.clear()
      self.status.set("Видалено.")

  def clear(self):
    for e in self.entries.values():
      e.delete(0, tk.END)

  def select_item(self, e):
    sel = self.tree.selection()
    if sel:
      vals = self.tree.item(sel[0], "values")
      for i, k in enumerate(self.entries):
        self.entries[k].delete(0, tk.END)
        self.entries[k].insert(0, vals[i])

  def open_f(self):
    p = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
    if p:
      self.repo.load(p)
      self.file = p
      self.update_table()
      self.status.set(f"Завантажено: {os.path.basename(p)}")

  def save_f(self):
    if self.file:
      self.repo.save(self.file)
      self.status.set("Збережено.")
    else:
      self.save_as_f()

  def save_as_f(self):
    p = filedialog.asksaveasfilename(defaultextension=".csv")
    if p:
      self.repo.save(p)
      self.file = p
      self.status.set("Збережено.")


if __name__ == "__main__":
  root = tk.Tk()
  App(root)
  root.mainloop()