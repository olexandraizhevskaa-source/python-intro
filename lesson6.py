import functools


def shadow(limit=200):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            total_sum = 0
            limit_exceeded = False
            gen = func(*args, **kwargs)

            for item in gen:
                print(item)
                try:
                    parts = str(item).strip().split()
                    if len(parts) >= 2:
                        amount = float(parts[-1])
                        total_sum += amount

                        if total_sum > limit and not limit_exceeded:
                            print(
                                "«Тіньовий ліміт перевищено. Активую схему»."
                            )
                            limit_exceeded = True
                except (ValueError, TypeError):
                    pass

            return total_sum

        return wrapper

    return decorator


def suspicious_counter(threshold=100):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            suspicious_sum = 0
            gen = func(*args, **kwargs)

            for item in gen:
                try:
                    parts = str(item).strip().split()
                    if len(parts) >= 2:
                        amount = float(parts[-1])
                        if amount > threshold:
                            suspicious_sum += amount
                            print(
                                f"[ПОПЕРЕДЖЕННЯ]: Виявлено підозрілу транзакцію на суму {amount}! (Накопичено підозрілих: {suspicious_sum})"
                            )
                except (ValueError, TypeError):
                    pass

                yield item

        return wrapper

    return decorator


def transaction_generator():
    transactions = [
        "payment 120",
        "invalid_row_without_number",
        "refund 50",
        "transfer 300",
        "bad payload 999xyz",
        "payment 10",
    ]
    for tx in transactions:
        yield tx


@shadow(limit=200)
@suspicious_counter(threshold=100)
def process_transactions():
    return transaction_generator()


if __name__ == "__main__":
    final_amount = process_transactions()
    print(f"\nФінальна накопичена сума: {final_amount}")