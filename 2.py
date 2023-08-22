import imaplib
import email
import re
import time
import csv

# Функция для извлечения данных из писем и их сохранения в файл и вывода на экран
def process_emails_and_convert_to_csv():
    imap = imaplib.IMAP4_SSL("imap.yandex.ru")
    imap.login("okd.invoice@yandex.by", "nufssuttjtwiquay")
    imap.select("INBOX")

    # Получение UID всех писем в ящике
    result, data = imap.search(None, "ALL")
    email_uids = data[0].split()

    # Открытие файла для записи данных в формате CSV
    with open("parsed_emails.csv", "w", newline='', encoding="utf-8") as csv_output_file:
        csv_writer = csv.writer(csv_output_file)

        # Заголовок CSV файла
        csv_writer.writerow(["Сумма", "Дата", "Время", "Описание", "Счет"])

        # Открытие и чтение данных из текстового файла
        with open("parsed_emails6.txt", "r", encoding="utf-8") as txt_input_file:
            for line in txt_input_file:
                # Извлекаем данные с помощью регулярного выражения
                pattern = r'Зачисление\s+(\d+\.\d{2})\s+BYN\s+(\d{2}/\d{2}/\d{2})\s+(\d{2}:\d{2})\s+"([^"]+)"\s+счет\s+([A-Z\d]+)'
                match = re.search(pattern, line)
                if match:
                    amount = match.group(1)
                    date = match.group(2)
                    time = match.group(3)
                    description = match.group(4)
                    account = match.group(5)

                    # Записываем данные в CSV файл
                    csv_writer.writerow([amount, date, time, description, account])

    imap.close()
    imap.logout()

# Главный цикл
while True:
    process_emails_and_convert_to_csv()  # Обработка существующих и новых писем и конвертация в CSV
    time.sleep(60)  # Пауза в 60 секунд перед следующей проверкой
