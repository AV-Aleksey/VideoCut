import os
from pathlib import Path
import subprocess
import uuid


class Video:
    def cut(self, input_file, start_time, end_time, output_dir, video_name):
        salt = uuid.uuid4().hex

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

        print(f"Обрезка завершена. Сохранено в: {output_path}")

        return Path(output_path) 
