import random
import time
from queue import Queue

request_queue = Queue()
next_request_id = 1

def generate_request():
    global next_request_id
    request = {
        "id": next_request_id,
        "description": f"Заявка №{next_request_id}",
    }
    request_queue.put(request)
    print(f"[+] Згенеровано нову заявку: {request['description']}")
    next_request_id += 1

def process_request():
    if not request_queue.empty():
        request = request_queue.get()
        print(f"[-] Обробляється: {request['description']}")
    else:
        print("[!] Черга порожня — немає заявок для обробки")

def main():
    print("Сервісний центр запущено. Команди: g — згенерувати, p — обробити, s — стан черги, q — вийти")
    while True:
        command = input("Введіть команду: ").strip().lower()

        if command == "g":
            generate_request()
        elif command == "p":
            process_request()
        elif command == "s":
            print(f"[i] Заявок у черзі: {request_queue.qsize()}")
        elif command == "auto":
            for _ in range(random.randint(2, 5)):
                generate_request()
                time.sleep(0.2)
            while not request_queue.empty():
                process_request()
                time.sleep(0.2)
        elif command in ("q", "quit", "exit"):
            print("Завершення роботи сервісного центру.")
            break
        else:
            print("Невідома команда. Використайте g, p, s, auto або q.")

if __name__ == "__main__":
    main()
