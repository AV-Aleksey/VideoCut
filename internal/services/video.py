import os
import uuid
import ffmpeg._run as ffmpeg
from internal.config import settings


from pathlib import Path
from datetime import datetime, timedelta

def add_seconds(time_str, seconds, format="%H:%M:%S"):
    time_obj = datetime.strptime(time_str, format)
    time_obj += timedelta(seconds=seconds)

    return time_obj.strftime(format)

class Video:
    def cut(self, start_time, end_time, video_name):
        salt = uuid.uuid4().hex

        print(settings.STATIC_PATH)
        
        input_file = Path(settings.STATIC_PATH) /  "movies" / f"{video_name}.mp4"
        output_dir = Path(settings.STATIC_PATH) / "results"

        # Формат имени выходного файла
        output_file = output_dir / (video_name + salt + ".mp4")

        # Полный путь для сохранения выходного файла
        output_path = os.path.join(output_dir, output_file)

        (
            ffmpeg
            .input(str(input_file), ss=add_seconds(start_time, -1), to=add_seconds(end_time, 1))
            .output(str(output_file), vcodec="libx264", acodec="aac")
            .run(overwrite_output=True)
        )

        return Path(output_path) 
    
    async def stream(self, start_time: float, end_time: float, video_name: str):
        input_file = Path(settings.STATIC_PATH) / "movies" / f"{video_name}.mp4"

        command = (
            ffmpeg.input(str(input_file), ss=start_time, t=6)
            .output("pipe:", format="mp4", vcodec="libx264", movflags="frag_keyframe+empty_moov")
            .global_args("-loglevel", "error")
        )

        process = command.run_async(pipe_stdout=True, pipe_stderr=True)

        try:
            for chunk in iter(lambda: process.stdout.read(1024 * 1024), b""):
                yield chunk
        finally:
            process.kill()

        # 🔥 Проверяем ошибки, если что-то пошло не так
        stderr_output = process.stderr.read().decode("utf-8").strip()
        if stderr_output:
            print(f"FFmpeg ERROR: {stderr_output}")


