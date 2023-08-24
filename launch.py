from main import process_emails
from dogovor import process_emails_and_convert_to_csv
from Post import process_and_add_deals
import time


def main():
    while True:
        process_emails()  # Вызываем первую функцию
        time.sleep(5)  # Пауза в 60 секунд

        process_emails_and_convert_to_csv()  # Вызываем вторую функцию
        time.sleep(5)  # Пауза в 60 секунд

        process_and_add_deals()  # Вызываем третью функцию
        time.sleep(2)  # Пауза в 60 секунд


if __name__ == "__main__":
    main()
