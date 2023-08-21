import imaplib
import email
import chardet
import time
from bs4 import BeautifulSoup


# Функция для извлечения данных из писем и их сохранения в файл и вывода на экран
def process_emails():
    imap = imaplib.IMAP4_SSL("imap.yandex.ru")
    imap.login("okd.invoice@yandex.by", "nufssuttjtwiquay")
    imap.select("INBOX")

    # Получение UID всех писем в ящике
    result, data = imap.search(None, "ALL")
    email_uids = data[0].split()

    # Открытие файла для записи данных
    with open("parsed_emails4.txt", "a", encoding="utf-8") as output_file:
        # Загрузка уже обработанных записей из файла
        processed_data = set()
        try:
            with open("parsed_emails4.txt", "r", encoding="utf-8") as existing_data_file:
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

            encoding = chardet.detect(raw)['encoding']
            text = raw.decode(encoding)

            # Используем BeautifulSoup для парсинга HTML-текста и извлечения данных из тегов <pre>
            soup = BeautifulSoup(text, 'html.parser')
            pre_tags = soup.find_all('pre')

            for pre_tag in pre_tags:
                pre_text = pre_tag.get_text().strip()
                data_to_save = f"{pre_text}\n"
                if data_to_save not in processed_data:
                    output_file.write(data_to_save)
                    print(data_to_save)
                    processed_data.add(data_to_save)

    imap.close()
    imap.logout()


# Главный цикл
while True:
    process_emails()  # Обработка существующих и новых писем
    time.sleep(60)  # Пауза в 60 секунд перед следующей проверкой
