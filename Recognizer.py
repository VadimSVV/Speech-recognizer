import os
import zipfile
from vosk import Model, KaldiRecognizer
import pyaudio

# Динамический путь к папке "Downloads"
downloads_folder = os.path.join(os.environ['USERPROFILE'], "Downloads")
archive_path = os.path.join(downloads_folder, "vosk-model-small-ru-0.22.zip")

# Папка распакованной модели рядом со скриптом
model_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vosk-model-small-ru-0.22")

print(f"Путь к архиву: {archive_path}")
print(f"Путь к модели: {model_folder}")

# Проверяем наличие архива и распаковываем если нужно
if not os.path.exists(archive_path):
    print(f"Архив модели не найден: {archive_path}")
    exit(1)

if not os.path.exists(model_folder):
    print("Модель не распакована, начинаю распаковку...")
    try:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(os.path.abspath(__file__)))
        print("Распаковка прошла успешно.")
    except Exception as e:
        print(f"Ошибка распаковки: {e}")
        exit(1)
else:
    print("Модель уже распакована.")

# Инициализация модели
try:
    model = Model(model_folder)
except Exception as e:
    print(f"Ошибка инициализации модели: {e}")
    exit(1)

recognizer = KaldiRecognizer(model, 16000)

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

print("Начинаю слушать... Говорите.")

while True:
    data = stream.read(1024)
    if recognizer.AcceptWaveform(data):
        print(recognizer.Result())
