# VideoCut

uvicorn internal.main:app --reload
python -m uvicorn internal.main:app --reload

python -m venv .venv
source .venv/Scripts/activate
pip install uv

uv init

uv add fastapi uvicorn httpx


docker build -t videocut . 
docker run -d -p 8000:8000 --name videocut-container videocut

Задача разработать приложение на ч (). 

{
    "start_time": "0:00:18",
    "end_time": "0:00:20",
    "movie_name": "bumer"
}

http://127.0.0.1:8000/stream?movie_name=bumer&start_time=0%3A00%3A18&end_time=0%3A00%3A20

Вводная часть (контекст)
1) есть шаблон приложения fastapi на python, есть эндпоинт который возвращает hello world (поэтому пропусти часть с базовой настройкой сервера)
2) в качестве пакетного менеджера я использую uv, для добавления новых пакетов использую команду uv add учти это когда будет советовать устанавливать библиотеки
3) версия python 3.12.9
4) Разрабатываю приложение в ОС Windows 11, для удобства установлен git bash терминал, его буду использовать на протяжении всей разработки
5) main.py основной файл приложения, он находится по пути ./internal/main.py 
6) в приложении есть папка с субтитрами формата srt находится она по пути ./internal/assets/subtitles/bumer.srt (пока там только 1 файл но после реализации mvp будут еще)

Абстрактная цель
разработка api которое бы принимало на вход текст, например "але привет" выполняло поиск по различным субтитрам и находило время и название фильма где используется данный текст (текст может не совпадать на 100%) после чего вырезать данный фрагмент со словами из видео и отправить пользователю небольшой видеофайл где используется конкретный текст из запроса.

Цель
Я буду присылать тебе фрагменты кода из полуготовог оприложения а ты будешь корректировать

Цели
1) написать функцию поиска по субтитрам, возможно установить вспомогательные библиотеки для более лучшего и быстрого результата. Поиск не должен реагировать на регистр и символы, а так же возвращать первый найденный элемент (совпадаение текста должно быть минимум на 80%). Функция должна вернуть время употребления фразы и название фильма (пока можно использовать название файла)

Нужно написать функцию которая бы отсеивала текст с помощью rapidfuzz в python. Запросы 

На моем сервере есть папка с видео C:\Users\user\Desktop\my\VideoCut\internal\assets\movies с формате mp4. У меня есть проект fastApi. Я бы хотел реализовать возможность просматривать фрагмент из видео, например пользователь бы передавал мне название фильма и временную метку, сервер бы находил этот фрагмет и показывал пользователю (без скачивания), при этом надо учесть что это должно работать быстро и оптипизированно, клиент покинул сайт или ввел другой запрос уже открытая трансляция должна закрыться и после открыться новая




Команда	nvm (Node.js)	pyenv (Python)
Установка версии	nvm install 18	pyenv install 3.12.0
Глобальное переключение	nvm use --global 18	pyenv global 3.12.0
Локальное переключение	nvm use 18	pyenv local 3.12.0


