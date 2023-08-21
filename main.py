import imaplib
import email
import chardet
import re

imap = imaplib.IMAP4_SSL("imap.yandex.ru")
imap.login("okd.invoice@yandex.by", "nufssuttjtwiquay")
imap.select("INBOX")

result, data = imap.search(None, "ALL")

for num in data[0].split():
    result, data = imap.fetch(num, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])

    if msg.is_multipart():
        raw = msg.get_payload(0).get_payload(decode=True)
    else:
        raw = msg.get_payload(decode=True)

    encoding = chardet.detect(raw)['encoding']
    text = raw.decode(encoding)

    # Используйте регулярное выражение для извлечения нужных строк
    pattern = r'Зачисление \d+\.\d{2} BYN \d{2}/\d{2}/\d{2} \d{2}:\d{2} "Принятые платежи согласно реестру" счет [A-Z\d]+'
    matches = re.findall(pattern, text)

    for match in matches:
        print(match)

imap.close()
imap.logout()

