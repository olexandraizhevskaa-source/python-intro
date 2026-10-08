from models import Antibiotic, Vitamin, Vaccine

medicines = [
    Antibiotic("Амоксицилін", quantity=20, price=15.5),
    Vitamin("Вітамін D3", quantity=30, price=8.0),
    Vaccine("Вакцина від грипу", quantity=10, price=120.0),
]

for med in medicines:
    print(med.info())
    