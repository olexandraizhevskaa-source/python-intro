import datetime
from functools import wraps

VALID_TYPES = {"GATE", "CARGO", "ACCESS", "ALARM", "SENSOR", "CALL", "SYSTEM"}

def is_valid_timestamp(ts_str: str) -> bool:
    if len(ts_str) != 19:
        return False
    try:
        datetime.datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S")
        return True
    except ValueError:
        return False

def validate_lines(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.corrupted_count = 0
        
        for line in func(*args, **kwargs):
            line_str = line.strip()
            if not line_str:
                continue
            
            parts = line_str.split("|")
            if len(parts) < 3:
                wrapper.corrupted_count += 1
                continue
            
            timestamp, event_type = parts[0], parts[1]
            key_value_pairs = parts[2:]
            
            if not is_valid_timestamp(timestamp):
                wrapper.corrupted_count += 1
                continue
            
            if event_type not in VALID_TYPES:
                wrapper.corrupted_count += 1
                continue
            
            valid_kv = True
            for kv in key_value_pairs:
                if "=" not in kv:
                    valid_kv = False
                    break
                k, v = kv.split("=", 1)
                if not k or not v:
                    valid_kv = False
                    break
            
            if not valid_kv:
                wrapper.corrupted_count += 1
                continue
            
            yield {
                "timestamp": timestamp,
                "type": event_type,
                "data": dict(pair.split("=", 1) for pair in key_value_pairs),
                "raw": line_str
            }
            
    wrapper.corrupted_count = 0
    return wrapper

def count_and_report_events(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        counts = {event_type: 0 for event_type in VALID_TYPES}
        valid_total = 0
        
        for item in func(*args, **kwargs):
            counts[item["type"]] += 1
            valid_total += 1
            yield item
            
        corrupted_count = getattr(func, "corrupted_count", 0)
        
        print("\n" + "=" * 45)
        print("          ЗВІТ ОБРОБКИ ЖУРНАЛУ ХАБУ        ")
        print("=" * 45)
        print("Кількість цілих подій за типами:")
        for etype in sorted(VALID_TYPES):
            print(f"  • {etype:<8}: {counts[etype]} шт.")
        print("-" * 45)
        print(f"Усього валідних (цілих) подій : {valid_total}")
        print(f"Усього битих (зіпсованих) рядків: {corrupted_count}")
        print("=" * 45 + "\n")
        
    return wrapper

def read_log_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            yield line

@count_and_report_events
@validate_lines
def process_hub_log(filepath: str):
    return read_log_file(filepath)

if __name__ == "__main__":
    log_file_path = "hub_log.txt"
    for _ in process_hub_log(log_file_path):
        pass