import json
import time
import requests

from plugin_server.config import PIXVERSE_API_KEY
from plugin_server.logger import server_logger

PIXVERSE_POLLING_INTERVAL = 3

def pixverse_upload_image(image_path):
    url = "https://app-api.pixverse.ai/openapi/v2/image/upload"

    payload = {}
    files = [
        ('image', ('', open(image_path, 'rb'), 'application/octet-stream'))
    ]
    headers = {
        'API-KEY': PIXVERSE_API_KEY,
        'Ai-trace-id': '{{$string.uuid}}'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    if response.status_code == 200:
        rsp = response.json()
        img_id = rsp['resp']['img_id']
        return True, img_id

    elif response.status_code == 500:
        server_logger.info("[PixVerse] Uploaded Image content moderation failed.")
        return False, None


def pixverse_image_to_video(img_id, args):
    url = "https://app-api.pixverse.ai/openapi/v2/video/img/generate"

    payload = json.dumps({
        "duration": args['duration'],
        "img_id": img_id,
        "model": "v3.5",
        "motion_mode": "normal",
        "negative_prompt": args['negative_prompt'],
        "prompt": args['prompt'],
        "quality": "360p",
        "seed": args['seed'],
        "water_mark": False
    })
    headers = {
        'API-KEY': PIXVERSE_API_KEY,
        'Ai-trace-id': '{{$string.uuid}}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    rsp = response.json()

    return rsp['resp']['video_id']


def pixverse_get_result(video_id):
    while True:
        url = f"https://app-api.pixverse.ai/openapi/v2/video/result/{video_id}"

        payload = {}
        headers = {
            'API-KEY': PIXVERSE_API_KEY,
            'Ai-trace-id': '{{$string.uuid}}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        rsp = response.json()

        status = rsp['resp']['status']

        # 1: Generation successful; 5: Generating; 7: Contents moderation failed; 8: Generation failed;
        if status == 1:
            server_logger.info("[PixVerse] Generation successful.")
            video_url = rsp['resp']['url']
            return True, video_url
        elif status == 7:
            server_logger.info("[PixVerse] Contents moderation failed.")
            return False, None
        elif status == 8:
            server_logger.info("[PixVerse] Generation failed.")
            return False, None
        elif status == 5:
            time.sleep(PIXVERSE_POLLING_INTERVAL)
        else:
            return False, None



def download_video(url, save_path):
    try:
        # 发起 GET 请求
        response = requests.get(url, stream=True)

        # 打开本地文件，以二进制写入模式
        with open(save_path, 'wb') as file:
            # 分块写入文件，避免占用过多内存
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return True
    except Exception as e:
        server_logger.info(f"[PixVerse] [Download Video] {e}")
        return False


def pixverse_process(image_path, video_path, args):
    # 上传图片
    result, img_id = pixverse_upload_image(image_path)

    # 上传成功
    if result:
        # 生成视频
        video_id = pixverse_image_to_video(img_id, args)

        # 获取生成结果
        generate_result, video_url = pixverse_get_result(video_id)

        # 生成成功
        if generate_result:
            # 下载视频
            return download_video(video_url, video_path)

    return False
