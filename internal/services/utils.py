import re
from datetime import datetime, timedelta
from rapidfuzz import process, fuzz

def compare_query_to_text(query, text):
    # Список исключений (например, предлоги, короткие фразы)
    stop_words = {"да", "ну", "нет", "как", "в", "и", "на", "с", "по", "для", "от", "к", "что", "а"}
    
    # Убираем предлоги и короткие слова
    def clean_text(text):
        return [word for word in text.lower().split() if word not in stop_words]
    
    def calculate_match_percent(count, matchCount):
        if count == 0:
            return 0  # Чтобы избежать деления на ноль
        percent = (matchCount / count) * 100
        return percent

    # Очистка текста
    query_words = clean_text(query)

    matchCount = 0;
    for query_part in query_words:
        if fuzz.partial_ratio(query_part, text.lower()) > 80:
            matchCount += 1

    result = calculate_match_percent(len(query_words), matchCount)

    if result > 60:
        return True

    return False

class Utils:
    def load_subtitles(self, file_path: str):
        subtitles = []

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        matches = re.findall(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n", content, re.DOTALL)

        for start_time, end_time, text in matches:
            clean_text = re.sub(r"[^\w\s]", "", text.replace("\n", " ")).strip().lower()
            subtitles.append((f"{start_time} --> {end_time}", clean_text))

        return subtitles
    
    def find_text_in_subtitles(self, search_text, subtitles, threshold: int = 30):
        search_text = re.sub(r"[^\w\s]", "", search_text).strip().lower()

        # Оставляем только те субтитры, где есть слово из запроса
        filtered_subtitles = []
        for time, text in subtitles:
            if compare_query_to_text(search_text, text):
                filtered_subtitles.append((time, text))


        print( filtered_subtitles)
        if not filtered_subtitles:
            return None  # Если вообще ничего не нашли, возвращаем None

        subtitle_texts = [text for _, text in filtered_subtitles]

        match = process.extractOne(search_text, subtitle_texts, scorer=fuzz.ratio)

        if match:
            print(f"Лучшее совпадение: {match[0]} с точностью {match[1]}%")  # Логируем совпадение

        if match and match[1] >= threshold:
            index = subtitle_texts.index(match[0])
            return filtered_subtitles[index]

        return None
    
    def convert_and_round_time(self, time_str):
         # Формат времени
        time_format = "%H:%M:%S,%f"
    
        # Разделяем строку по ' --> '
        start_time_str, end_time_str = time_str.split(" --> ")

        # Преобразуем строку времени в объект datetime
        start_time = datetime.strptime(start_time_str, time_format)
        end_time = datetime.strptime(end_time_str, time_format)

        # Убавляем 1 секунду от start_time
        start_time_adjusted = start_time - timedelta(seconds=2)
        
        # Прибавляем 1 секунду к end_time
        end_time_adjusted = end_time + timedelta(seconds=2)

        # Преобразуем в строку в формате "HH:MM:SS"
        start_time_adjusted_str = start_time_adjusted.strftime("%H:%M:%S")
        end_time_adjusted_str = end_time_adjusted.strftime("%H:%M:%S")

        return [start_time_adjusted_str, end_time_adjusted_str]