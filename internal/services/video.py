import os
from pathlib import Path
import subprocess
import uuid


class Video:
    def cut(self, start_time, end_time, video_name):
        salt = uuid.uuid4().hex
        
        input_file = Path(__file__).parent.parent / "assets" /  "movies" / f"{video_name}.mp4"
        output_dir = Path(__file__).parent.parent / "assets" / "results"

        # Формат имени выходного файла
        output_file = output_dir / (video_name + salt + ".mp4")

        # Полный путь для сохранения выходного файла
        output_path = os.path.join(output_dir, output_file)

        # Команда для обрезки видео с использованием FFmpeg
        command = [
            "ffmpeg",
            "-i", str(input_file),
            "-ss", start_time,  # Время начала обрезки
            "-to", end_time,    # Время окончания обрезки
            "-c:v", "libx264",  # Перекодировка видео
            "-c:a", "aac",      # Перекодировка аудио
            "-strict", "experimental",  # Если используется нестабильная версия кодека
            str(output_file)    # Путь к файлу вывода
        ]
        
        subprocess.run(command, check=True)

        return Path(output_path) 
