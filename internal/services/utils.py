import re

from rapidfuzz import process, fuzz

def compare_query_to_text(query, text):
    # Список исключений (например, предлоги, короткие фразы)
    stop_words = {"да", "ну", "нет", "как", "в", "и", "на", "с", "по", "для", "от", "к", "что"}
    
    # Убираем предлоги и короткие слова
    def clean_text(text):
        return [word for word in text.lower().split() if word not in stop_words]

    # Очистка текста
    query_words = clean_text(query)
    text_words = clean_text(text)

    # Если запрос слишком короткий (например, одна или две фразы), не проверяем
    if len(query_words) == 0:
        return False
    
    # 1. Проверка на подстроку (используем partial_ratio)
    if fuzz.partial_ratio(query.lower(), text.lower()) > 80:
        return True

    # 2. Проверка на схожесть с ошибками (используем ratio)
    if fuzz.ratio(query.lower(), text.lower()) > 70:
        return True

    # 3. Проверка на совпадение более 50% слов (по словам)
    common_words = len(set(query_words).intersection(set(text_words)))
    if common_words / len(query_words) > 0.5:
        return True

    # Если не совпадает по ни одному из критериев
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