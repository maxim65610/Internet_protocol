import os
import re
import socket
import requests


def get_ip_info(ip):
    """
    Получает информацию о номере автономной системы (AS), стране и провайдере для заданного IP-адреса.
    Использует API whois сервисов для запроса данных.
    """
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        data = response.json()

        # Извлекаем AS, страну и провайдера
        as_info = data.get("org", "Неизвестно")
        country = data.get("country", "Неизвестно")
        provider = as_info.split(" ", 1)[1] if " " in as_info else "Неизвестно"
        as_number = as_info.split(" ")[0] if " " in as_info else "Неизвестно"

        return as_number, country, provider
    except Exception as e:
        return "Ошибка", "Ошибка", "Ошибка"


def trace_route(target):
    """
    Выполняет трассировку маршрута до целевого домена или IP-адреса.
    Возвращает список промежуточных IP-адресов.
    """
    try:
        target_ip = socket.gethostbyname(target)
        print(f"Трассировка до {target} ({target_ip})\n")

        if os.name == "nt":
            command = f"tracert -d -w 100 {target_ip}"
        else:
            command = f"traceroute -n -w 1 {target_ip}"

        result = os.popen(command).read()
        return result
    except socket.gaierror:
        print("Ошибка: Не удалось разрешить доменное имя в IP-адрес.")
        return ""
    except Exception as e:
        print(f"Ошибка при выполнении трассировки: {e}")
        return ""


def parse_traceroute_output(output):
    """
    Парсит вывод команды tracert/traceroute и извлекает IP-адреса.
    """
    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    ips = re.findall(ip_pattern, output)
    return ips


def main():
    """
    Основная функция программы.
    """
    print("Введите доменное имя или IP-адрес:")
    target = input().strip()

    if not target:
        print("Ошибка: Введите корректное доменное имя или IP-адрес.")
        return

    traceroute_output = trace_route(target)
    if not traceroute_output:
        return

    ips = parse_traceroute_output(traceroute_output)

    print("\nРезультаты трассировки:")
    print(f"{'No':<5}{'IP-адрес':<20}{'AS':<15}{'Страна':<15}{'Провайдер'}")
    print("-" * 70)

    for idx, ip in enumerate(ips, start=1):
        as_number, country, provider = get_ip_info(ip)
        print(f"{idx:<5}{ip:<20}{as_number:<15}{country:<15}{provider}")


if __name__ == "__main__":
    main()