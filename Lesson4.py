from abc import ABC, abstractmethod

# 1. Загальний інтерфейс для документів
class Document(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

# --- Звичайні документи (Corp) ---
class Report(Document):
    def render(self) -> str:
        return "[Звіт] Звичайні офіційні дані"

class Invoice(Document):
    def render(self) -> str:
        return "[Рахунок] Стандартна сума та реквізити"

class Contract(Document):
    def render(self) -> str:
        return "[Договір] Стандартні умови співпраці"

# --- Тіньові документи (Shadow) ---
class ShadowReport(Document):
    def render(self) -> str:
        return "[Тіньовий Звіт] Спеціальні дані + приховані поля 🕶️"

class ShadowInvoice(Document):
    def render(self) -> str:
        return "[Тіньовий Рахунок] Змінений формат (сірі постачання)"

class ShadowContract(Document):
    def render(self) -> str:
        return "[Тіньовий Договір] Модифіковані умови"

# 2. Інтерфейс фабрики та самі фабрики
class DocumentFactory(ABC):
    @abstractmethod
    def create_document(self, doc_type: str) -> Document:
        pass

class CorpDocumentFactory(DocumentFactory):
    def create_document(self, doc_type: str) -> Document:
        if doc_type == "report":
            return Report()
        elif doc_type == "invoice":
            return Invoice()
        elif doc_type == "contract":
            return Contract()
        raise ValueError("Невідомий тип документа")

class ShadowDocumentFactory(DocumentFactory):
    def create_document(self, doc_type: str) -> Document:
        if doc_type == "report":
            return ShadowReport()
        elif doc_type == "invoice":
            return ShadowInvoice()
        elif doc_type == "contract":
            return ShadowContract()
        raise ValueError("Невідомий тип документа")

# 3. Фасад / Менеджер з перевіркою безпеки (Білий список)
class DocumentManager:
    ALLOWED_TYPES = {"report", "invoice", "contract"}

    def __init__(self, mode: str):
        self.mode = mode
        # Вибираємо фабрику залежно від конфігу
        if mode == "corp":
            self.factory = CorpDocumentFactory()
        elif mode == "shadow":
            self.factory = ShadowDocumentFactory()
        else:
            raise ValueError("Невідомий режим (mode)")

    def get_document(self, doc_type: str) -> Document:
        # Проста перевірка безпеки (білий список)
        if doc_type not in self.ALLOWED_TYPES:
            raise PermissionError(f"Створення заблоковано: '{doc_type}' не входить до білого списку!")
        
        return self.factory.create_document(doc_type)

# ==========================================
# 4. ДЕМОНСТРАЦІЯ ДВОХ ЗАПУСКІВ
# ==========================================
if __name__ == "__main__":
    print("--- 1. ЧЕСНИЙ РЕЖИМ ('corp') ---")
    corp_manager = DocumentManager(mode="corp")
    print(corp_manager.get_document("report").render())
    print(corp_manager.get_document("invoice").render())

    print("\n--- 2. ТІНЬОВИЙ РЕЖИМ ('shadow') ---")
    shadow_manager = DocumentManager(mode="shadow")
    print(shadow_manager.get_document("report").render())
    print(shadow_manager.get_document("invoice").render())

    print("\n--- 3. ПЕРЕВІРКА БЕЗПЕКИ (БІЛИЙ СПИСОК) ---")
    try:
        corp_manager.get_document("hacker_document")
    except PermissionError as e:
        print(f"Помилка безпеки спіймана: {e}")