from abc import ABC, abstractmethod


class JunkItem:
  def __init__(self, name: str, quantity: int, value: float):
    self.name = name
    self.quantity = quantity
    self.value = value

  def __repr__(self):
    return f"JunkItem(name='{self.name}', quantity={self.quantity}, value={self.value})"


# 6. Виділений окремий інтерфейс (абстрактний клас)
class StorageBackend(ABC):

  @abstractmethod
  def save(self, items: list[JunkItem]) -> None:
    pass

  @abstractmethod
  def load(self) -> list[JunkItem]:
    pass


# 2. Реалізація класу JunkStorage (тепер наслідує StorageBackend)
class JunkStorage(StorageBackend):

  def __init__(self, filename: str):
    self.filename = filename

  def save(self, items: list[JunkItem]) -> None:
    """Записує список предметів у файл у форматі CSV (роздільник |, дроби через кому)."""
    with open(self.filename, "w", encoding="utf-8") as f:
      for item in items:
        # Замінюємо крапку на кому для десяткових дробів
        value_str = str(item.value).replace(".", ",")
        line = f"{item.name}|{item.quantity}|{value_str}\n"
        f.write(line)

  def load(self) -> list[JunkItem]:
    """Читає та відновлює об'єкти JunkItem з файлу з перевіркою на зіпсовані рядки (пункт 5)."""
    items = []
    try:
      with open(self.filename, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
          line = line.strip()
          if not line:
            continue

          parts = line.split("|")
          # Перевірка: чи є рівно три поля
          if len(parts) != 3:
            print(
                f"[Попередження] Рядок {line_num} пропущено: невірний формат"
                f" (очікувалось 3 поля)."
            )
            continue

          name_str, qty_str, val_str = parts

          # Перевірка: quantity має бути числом (int)
          try:
            qty = int(qty_str)
          except ValueError:
            print(
                f"[Попередження] Рядок {line_num} пропущено: quantity '{qty_str}'"
                " не є цілим числом."
            )
            continue

          # Перевірка: value має бути числом (float, крапка або кома)
          try:
            val = float(val_str.replace(",", "."))
          except ValueError:
            print(
                f"[Попередження] Рядок {line_num} пропущено: value '{val_str}'"
                " не є числом з плаваючою комою."
            )
            continue

          items.append(JunkItem(name_str, qty, val))
    except FileNotFoundError:
      print(f"Файл {self.filename} не знайдено.")

    return items


# Клас для керування складом (не прив'язаний до конкретного формату сховища)
class WarehouseManager:

  def __init__(self, storage: StorageBackend):
    self.storage = storage

  def save_inventory(self, items: list[JunkItem]):
    self.storage.save(items)

  def load_inventory(self) -> list[JunkItem]:
    return self.storage.load()


# === 3. Демонстрація роботи ===
if __name__ == "__main__":
  filename = "warehouse.csv"

  # Створюємо сховище
  storage = JunkStorage(filename)
  manager = WarehouseManager(storage)

  # Створюємо початкові предмети з прикладу
  original_items = [
      JunkItem("Бляшанка", 5, 2.5),
      JunkItem("Стара плата", 3, 7.8),
      JunkItem("Купка дротів", 10, 1.2),
  ]

  print("--- Зберігаємо предмети у файл ---")
  manager.save_inventory(original_items)

  # Зіпсований рядок спеціально для перевірки п. 5
  with open(filename, "a", encoding="utf-8") as f:
    f.write("Битий рядок без форматів\n")
    f.write("Зламане число|не_число|5.5\n")

  print("\n--- Зчитуємо предмети з файлу ---")
  loaded_items = manager.load_inventory()

  print("\n--- Результат завантаження ---")
  for item in loaded_items:
    print(item)

  # 4. Переконуємось, що значення збереглися правильно
  assert len(loaded_items) == 3, "Кількість коректних елементів не збігається!"
  assert loaded_items[0].name == "Бляшанка"
  assert loaded_items[0].quantity == 5
  assert loaded_items[0].value == 2.5
  print(
      "\nУспіх! Усі дані завантажено правильно, а зіпсовані рядки успішно"
      " пропущено."
  )