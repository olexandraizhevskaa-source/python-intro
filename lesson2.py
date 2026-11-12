deals = [
    ("Олексій", 50, "clean"),
    ("Марія", 450.50, "suspicious"),
    ("Іван", 1200, "fraud"),
    ("Олена", "не число", "clean"),
    ("Тарас", 500, "unknown_status"),
]

processed_clients = []

for name, amount, status in deals:
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        amount_category = "Фальшиві дані"
    elif amount < 100:
        amount_category = "Дрібнота"
    elif amount <= 999:
        amount_category = "Середнячок"
    else:
        amount_category = "Великий клієнт"

    match status:
        case "clean":
            status_decision = "Працювати без питань"
        case "suspicious":
            status_decision = "Перевірити документи"
        case "fraud":
            status_decision = "У чорний список"
        case _:
            status_decision = "Невідомий статус"

    processed_clients.append((name, amount_category, status_decision))

for client in processed_clients:
    print(client)