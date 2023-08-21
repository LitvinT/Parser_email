import imaplib
import email
import chardet

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

    print("Текст:\n", text)

imap.close()
imap.logout()