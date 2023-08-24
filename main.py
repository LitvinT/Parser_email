import imaplib
import email
import re
import time

# Функция для извлечения данных из писем и их сохранения в файл и вывода на экран


def process_emails():
    print("Функция 1 вызвана")
    imap = imaplib.IMAP4_SSL("imap.yandex.ru")
    imap.login("okd.invoice@yandex.by", "nufssuttjtwiquay")
    imap.select("INBOX")

    # Получение UID всех писем в ящике
    result, data = imap.search(None, "ALL")
    email_uids = data[0].split()

    # Открытие файла для записи данных
    with open("parsed_emails6.txt", "a", encoding="utf-8") as output_file:
        # Загрузка уже обработанных записей из файла
        processed_data = set()
        try:
            with open("parsed_emails6.txt", "r", encoding="utf-8") as existing_data_file:
                processed_data = set(existing_data_file.readlines())
        except FileNotFoundError:
            pass

        # Итерация по письмам
        for email_uid in email_uids:
            result, data = imap.fetch(email_uid, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            if msg.is_multipart():
                raw = msg.get_payload(0).get_payload(decode=True)
            else:
                raw = msg.get_payload(decode=True)

            encoding = msg.get_charset() or "cp1251"  # Используем кодировку cp1251

            # Извлекаем данные с помощью регулярного выражения
            pattern = r'Зачисление\s+(\d+\.\d{2}\s+BYN\s+\d{2}/\d{2}/\d{2}\s+\d{2}:\d{2})\s+"([^"]+)"\s+счет\s+([A-Z\d]+)'
            matches = re.findall(pattern, raw.decode(encoding), re.IGNORECASE | re.MULTILINE)

            for match in matches:
                data_to_save = f"Зачисление {match[0]} \"{match[1].strip()}\" счет {match[2]}\n"
                if data_to_save not in processed_data:
                    output_file.write(data_to_save)
                    print(data_to_save)
                    processed_data.add(data_to_save)

    imap.close()
    imap.logout()


process_emails()  # Вызов функции



