import requests
import csv
import time
import json

# URL для запроса к API Битрикс24
url = "https://crm.okna-ori.by/rest/1/5rqi5834zubf0jjj/crm.item.add?entityTypeId=163"

# Функция для обработки данных и добавления сделок
def process_and_add_deals():
    # Загрузка информации о добавленных сделках из файла (если существует)
    try:
        with open("added_deals.json", "r") as added_deals_file:
            added_deals = set(json.load(added_deals_file))
    except FileNotFoundError:
        added_deals = set()

    # Открываем CSV файл для чтения данных
    with open("parsed_emails123321.csv", "r", newline='', encoding="utf-8") as csv_input_file:
        csv_reader = csv.reader(csv_input_file)

        # Пропускаем заголовок
        next(csv_reader)

        # Обрабатываем каждую строку CSV файла
        for row in csv_reader:
            amount, date, time, description, account, contract = row

            # Проверяем, была ли уже добавлена такая сделка
            deal_info = f"{description}{account}{date}{contract}{amount}{time}"
            if deal_info in added_deals:
                continue

            # Параметры запроса к API
            params = {
                "fields[ufCrm7_1692687429532]": description,
                "fields[ufCrm7_1692687312468]": account,
                "fields[ufCrm7_1692687348218]": date,
                "fields[ufCrm7_1692705471573]": contract,
                "fields[ufCrm7_1692686895896]": amount,
                "fields[ufCrm7_1692690842173]": time
            }

            # Отправляем запрос к API
            response = requests.get(url, params=params)

            # Проверяем успешность запроса
            if response.status_code == 200:
                added_deals.add(deal_info)
                print("Новая сделка успешно добавлена в Битрикс24")
            else:
                print("Произошла ошибка при добавлении новой сделки в Битрикс24")

    # Сохраняем информацию о добавленных сделках в файл
    with open("added_deals.json", "w") as added_deals_file:
        json.dump(list(added_deals), added_deals_file)

# Бесконечный цикл для постоянной проверки и добавления сделок
while True:
    process_and_add_deals()
    time.sleep(60)  # Пауза в 60 секунд перед следующей проверкой
