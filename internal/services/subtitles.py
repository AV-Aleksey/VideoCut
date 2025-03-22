import json
from pathlib import Path
import srt
from typing import List, Dict

import re
from rapidfuzz import fuzz

def compare_percent(query, text):
    # Список исключений (например, предлоги, короткие фразы)
    stop_words = {"в", "и", "с", "к", "а"}
    
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

    matchCount = 0
    for query_part in query_words:
        if fuzz.partial_ratio(query_part, text.lower()) > 80:
            matchCount += 1

    return calculate_match_percent(len(query_words), matchCount)

class Subtitles:
    def get(self, name):
        srt_path = Path(__file__).parent.parent / "assets" / "subtitles" / f"{name}.srt"
        json_path = Path(__file__).parent.parent / "assets" / "subtitles" / "json" / f"{name}.json"

        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as json_file:
                return json.load(json_file)

        if srt_path.exists():
            result = self.parse(srt_path)

            with open(json_path, 'w', encoding='utf-8') as json_file:
                json.dump(result, json_file, ensure_ascii=False, indent=4)

            return result
        else:
            return None
        

    def list(self):
        subtitles_dir = Path(__file__).parent.parent / "assets" / "subtitles"

        return [file.stem for file in subtitles_dir.glob("*.srt")]

    def parse(self, path) -> List[Dict[str, str]]:
        #Удаляет HTML-теги из текста
        def clean_text(text: str) -> str:
            text = re.sub(r"<.*?>", "", text).lower().replace("\n", " ").strip()
            text = re.sub(r"[.,!?()\[\]{}\-]", "", text)
            return text

        with open(path, "r", encoding="utf-8") as file:
            subtitles = list(srt.parse(file.read()))

        parsed_subtitles = []
        for subtitle in subtitles:
            parsed_subtitles.append({
                "startTime": str(subtitle.start).split('.')[0],
                "endTime": str(subtitle.end).split('.')[0],
                "text": clean_text(subtitle.content)
            })
    
        return parsed_subtitles
    
    def find(self, search_text, movie_name, threshold: int = 60):
        subtitles = self.get(movie_name)
        if not subtitles:
            return None

        search_text = re.sub(r"[^\w\s]", "", search_text).strip().lower()
    
        # Оставляем только те субтитры, где есть слово из запроса
        filtered_subtitles = []
        for item in subtitles:
            percent = compare_percent(search_text, item['text'])

            if percent >= threshold:
                item['percent'] = percent

                filtered_subtitles.append(item)

        filtered_subtitles.sort(key=lambda x: x["percent"], reverse=True)

        if not filtered_subtitles:
            return None

        return filtered_subtitles[0]