import imaplib
import email
import time

mail = imaplib.IMAP4_SSL("imap.mail.ru")
mail.login("login", "password")
mail.select("INBOX")

while True:
  result, data = mail.uid('search', None, "ALL") # получаем UID новых писем
  email_uids = data[0].split()
  for uid in email_uids:
    result, data = mail.uid('fetch', uid, '(RFC822)') # получаем письмо
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    print("Новое письмо:")
    print(msg["Subject"])
    print(msg["From"])
    print(msg.get_payload())

  time.sleep(60) # пауза 60 секунд до следующей проверки
