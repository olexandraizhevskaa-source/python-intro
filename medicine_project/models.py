from abc import ABC, abstractmethod


class Medicine(ABC):
    def __init__(self, name: str, quantity: int, price: float):
        if not isinstance(name, str):
            raise TypeError("name має бути рядком")
        if not isinstance(quantity, int):
            raise TypeError("quantity має бути цілим числом")
        if not isinstance(price, (int, float)):
            raise TypeError("price має бути числом")

        self.name = name
        self.quantity = quantity
        self.price = price

    @abstractmethod
    def requires_prescription(self) -> bool:
        pass

    @abstractmethod
    def storage_requirements(self) -> str:
        pass

    def total_price(self) -> float:
        return self.quantity * self.price

    def info(self) -> str:
        prescription = "потрібен рецепт" if self.requires_prescription() else "без рецепта"
        return (f"{self.name}: {self.quantity} шт. по {self.price} грн "
                f"({prescription}), зберігання: {self.storage_requirements()}, "
                f"вартість: {self.total_price():.2f} грн")


class Antibiotic(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "8–15°C, темне місце"


class Vitamin(Medicine):
    def requires_prescription(self) -> bool:
        return False

    def storage_requirements(self) -> str:
        return "15–25°C, сухо"


class Vaccine(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "2–8°C, холодильник"

    def total_price(self) -> float:
        # +10% до звичайної вартості
        return self.quantity * self.price * 1.10