import time
import requests

from plugin_server.config import *
from plugin_server.logger import server_logger
from plugin_server.pixverse import pixverse_process
from plugin_server.ue import ue_process
from plugin_server.utils import *


def facefusion_image_interval(source_image_path, target_image_path, image_output_path):
	try:
		# 请求facefusion
		request_data = {
			"source_path": os.path.abspath(source_image_path),
			"target_path": os.path.abspath(target_image_path),
			"output_path": os.path.abspath(image_output_path)
		}
		response = requests.post(FACEFUSION_URL, json=request_data)
		rsp_json = response.json()

		# 压缩
		img = Image.open(image_output_path)

		file_name, file_extension = image_output_path.rsplit('.', 1)
		jpg_path = f"{file_name}.jpg"

		# 以指定质量保存压缩后的结果
		img.save(jpg_path, quality=100)

		# 移除png原图
		os.remove(image_output_path)

		return True, jpg_path
	except Exception as e:
		server_logger.exception(f"[Image generation exception] {e}")

		return False, None


def facefusion_image(source_image_path, images_folder, output_path, image_options):
	quality = image_options['quality']
	thumbnail_width = image_options['thumbnail_width']

	target_image_paths = find_png_files(images_folder)
	for i, target_image_path in enumerate(target_image_paths):

		if len(target_image_paths) == 1:
			image_output_path = output_path + ".png"
		else:
			image_output_path = output_path + f"-{i + 1}" + ".png"

		server_logger.info(f"FaceFusion process image... {i + 1} of {len(target_image_paths)}")

		result, image_output_path = facefusion_image_interval(source_image_path, target_image_path, image_output_path)

		# 生成成功
		if result:
			# 生成缩略图
			server_logger.info(f"Generate thumbnail...")
			compress_image(image_output_path, quality, thumbnail_width)
		else:
			return False
	return True


def facefusion_video(source_image_path, video_path, output_path):
	try:
		video_output_path = output_path + ".mp4"
		# 请求facefusion
		request_data = {
			"source_path": os.path.abspath(source_image_path),
			"target_path": os.path.abspath(video_path),
			"output_path": os.path.abspath(video_output_path)
		}
		response = requests.post(FACEFUSION_URL, json=request_data)
		rsp_json = response.json()

		return True

	except Exception as e:
		server_logger.exception(f"[Video generation exception] {e}")

		return False


def face_swap_internal(task_id, args):
	source_image_path = args["source_image_path"]
	ue_json_data = args["ue_json_data"]
	output_path = os.path.join(args['output_path'], f"{task_id}")
	is_video = args["video"]

	server_logger.info(f"[{task_id}] Start process...")

	start_time = time.time()

	# UE生成图像
	images_folder = ue_process(ue_json_data)

	if not is_video:
		server_logger.info("FaceFusion...")
		# facefusion图像
		result = facefusion_image(source_image_path, images_folder, output_path, ue_json_data['image_options'])
	else:
		target_image_path = find_png_files(images_folder)[0]

		# 创建临时文件夹
		temp_dir = './.temp'
		if not os.path.exists(temp_dir):
			os.mkdir(temp_dir)
		image_output_path = os.path.join(temp_dir, 'temp.png')

		server_logger.info("Pre swap face...")
		# 首次换脸
		first_result, image_output_path = facefusion_image_interval(source_image_path, target_image_path, image_output_path)
		# 首次换脸成功
		if first_result:
			server_logger.info("PixVerse...")

			# 处理视频
			video_path = os.path.join(temp_dir, 'temp.mp4')
			if pixverse_process(image_output_path, video_path, ue_json_data['video_options']):
				server_logger.info("Process video...")

				# 视频换脸
				result = facefusion_video(source_image_path, video_path, output_path)
			else:
				result = False
		else:
			result = False

	end_time = round(time.time() - start_time, 2)
	server_logger.info(f"[{task_id}] Finish process in {end_time} seconds.")

	return result
