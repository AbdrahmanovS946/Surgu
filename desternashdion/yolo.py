import cv2
import time
import smtplib
from email.mime.multipart import MIMEMultipart

# Загрузка предварительно обученного классификатора Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Загрузка изображения
camera = cv2.VideoCapture(0)

# Настройки электронной почты
email = 'abdrahmanovserghey@yandex.ru'
password = 'rvsjbmlxxaeekdub'
server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)

# Параметры отслеживания
last_time_detected = 0
last_people_detected = False

# Функция для отправки электронной почты
def send_email(subject):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = email
    server.sendmail(msg['From'], [email, 'abdraxmanov.1999@bk.ru'], msg.as_string())

# Запуск цикла обработки кадров
server.ehlo(email)
server.login(email, password)
while True:
    _, img = camera.read()

    # Обнаружение лиц
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Проверка наличия лиц в кадре
    people_detected = len(faces) > 0

    # Обработка обнаружения людей
    if people_detected and not last_people_detected and time.time() - last_time_detected > 120:
        send_email('Сотрудник на месте')
        last_time_detected = time.time()

    last_people_detected = people_detected

    # Вывод результатов
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Image', img)
    key = cv2.waitKey(1)
    if key == 27:  # ESC key
        break

server.quit()
camera.release()
cv2.destroyAllWindows()