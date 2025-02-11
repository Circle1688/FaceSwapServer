import psutil
from PIL import Image
import os


def find_png_files(directory):
    png_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                png_files.append(os.path.join(root, file))
    return png_files


def compress_image(source_path, quality, thumbnail_width):
    with Image.open(source_path) as img:
        # 计算缩略图的高度，保持图片的原始宽高比
        width, height = img.size
        thumbnail_height = int((thumbnail_width / width) * height)

        # 调整图片大小为缩略图尺寸
        img.thumbnail((thumbnail_width, thumbnail_height))

        file_name, file_extension = source_path.rsplit('.', 1)
        thumbnail_path = f"{file_name}_thumbnail.jpg"

        # 以指定质量保存缩略图
        img.save(thumbnail_path, quality=quality)


def kill_process_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.name() == process_name:
                proc.terminate()  # 先尝试发送SIGTERM信号
                try:
                    proc.wait(timeout=3)  # 等待3秒，看进程是否结束
                except psutil.TimeoutExpired:
                    print(f"Process {process_name} PID: {proc.pid} No response to SIGTERM signal, try sending SIGKILL signal")
                    proc.kill()  # 发送SIGKILL信号强制结束进程
                    proc.wait(timeout=3)  # 再次等待进程结束
                print(f"Process {process_name} PID: {proc.pid} has been ended")
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"Error while ending process: {e}")
