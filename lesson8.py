def check_medicines(medicines):
    result = []
    
    for name, quantity, category, temperature in medicines:
        if not isinstance(quantity, int) or not isinstance(temperature, (int, float)):
            result.append((name, "Помилка даних"))
            continue
            
        if temperature < 5:
            temp_status = "Надто холодно"
        elif temperature > 25:
            temp_status = "Надто жарко"
        else:
            temp_status = "Норма"
            
        match category:
            case "antibiotic":
                category_status = "Рецептурний препарат"
            case "vitamin":
                category_status = "Вільний продаж"
            case "vaccine":
                category_status = "Потребує спецзберігання"
            case _:
                category_status = "Невідома категорія"
                
        result.append((name, category_status, temp_status))
        
    return result