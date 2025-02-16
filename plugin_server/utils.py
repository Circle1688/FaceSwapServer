import shutil
from moviepy import VideoFileClip
import psutil
import requests
from PIL import Image
import os
from io import BytesIO
from hashlib import md5
from plugin_server.oss import *


def find_png_files(directory):
    png_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                png_files.append(os.path.join(root, file))
    return png_files


def compress_image(source_path, quality, thumbnail_width):
    with Image.open(source_path) as img:
        # 如果图片是RGBA模式，转换为RGB模式
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # 计算缩略图的高度，保持图片的原始宽高比
        width, height = img.size
        thumbnail_height = int((thumbnail_width / width) * height)

        # 调整图片大小为缩略图尺寸
        img.thumbnail((thumbnail_width, thumbnail_height))

        file_name, file_extension = source_path.rsplit('.', 1)
        thumbnail_path = f"{file_name}_thumbnail.jpg"

        # 以指定质量保存缩略图
        img.save(thumbnail_path, quality=quality)


def compress_image_bytes(image_bytes, quality, thumbnail_width):
    with Image.open(BytesIO(image_bytes)) as img:
        # 如果图片是RGBA模式，转换为RGB模式
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # 计算缩略图的高度，保持图片的原始宽高比
        width, height = img.size
        thumbnail_height = int((thumbnail_width / width) * height)

        # 调整图片大小为缩略图尺寸
        img.thumbnail((thumbnail_width, thumbnail_height))

        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG', quality=quality)

        # 获取bytes数据并返回
        return output_buffer.getvalue()


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


def download_file(url):
    filename = os.path.basename(url)

    response = requests.get(url)

    if response.status_code == 200:
        file_path = os.path.join(TEMP_DIR, filename)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print("Download successfully")
        return file_path
    else:
        print("Download failed")
        return None


def calculate_file_md5(file_path):
    """计算本地文件的 MD5 值"""
    hash_md5 = md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def download_avatar(user_id):
    avatar_path = f'{user_id}/avatar/avatar.png'
    temp_avatar_dir = os.path.join(TEMP_DIR, user_id)
    if not os.path.exists(temp_avatar_dir):
        os.mkdir(temp_avatar_dir)

    local_avatar_file_path = os.path.join(temp_avatar_dir, "avatar.png")
    if os.path.exists(local_avatar_file_path):
        # 获取本地文件的 MD5
        local_md5 = calculate_file_md5(local_avatar_file_path)
        oss_etag = get_etag(avatar_path)

        if local_md5 == oss_etag:
            print("File is the same as the local file and does not need to be downloaded.")
            return local_avatar_file_path
        else:
            print("File is different from local file, start downloading...")
            return download_file(get_full_url_oss(avatar_path))
    else:
        print("The local file does not exist, start downloading...")
        return download_file(get_full_url_oss(avatar_path))


def clear_folder(directory):
    # 检查目录是否存在
    if not os.path.exists(directory):
        return

    # 遍历目录并删除所有内容
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            # 如果是文件或符号链接，直接删除
            os.unlink(item_path)

        elif os.path.isdir(item_path):
            # 如果是子目录，递归删除整个目录
            shutil.rmtree(item_path)


def get_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append({"filename": file, "filepath": os.path.join(root, file)})
    return file_list


def extract_video_cover(video_path):
    # 加载视频文件
    clip = VideoFileClip(video_path)

    # 获取视频文件的目录和文件名（不带扩展名）
    dir_path, filename = os.path.split(video_path)
    name, ext = os.path.splitext(filename)

    # 生成封面图的文件名
    output_image_path = os.path.join(dir_path, f"{name}_thumbnail.jpg")

    # 保存为图片
    clip.save_frame(output_image_path, t=0)

    # 关闭视频文件
    clip.close()
