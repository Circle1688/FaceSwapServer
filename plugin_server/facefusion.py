import os.path
import time
from plugin_server.gallery_routes import suggest_file_name
from plugin_server.logger import server_logger
from plugin_server.oss import upload_file_oss
from plugin_server.pixverse import pixverse_process
from plugin_server.ue import ue_process
from plugin_server.upscale import upscale_process
from plugin_server.utils import *

# 创建临时文件夹
if not os.path.exists(TEMP_DIR):
	os.mkdir(TEMP_DIR)

TEMP_OUTPUT_DIR = os.path.join(TEMP_DIR, 'output')
if not os.path.exists(TEMP_OUTPUT_DIR):
	os.mkdir(TEMP_OUTPUT_DIR)


def upload_files_oss(folder, user_id):
	for file in get_files(folder):
		if not upload_file_oss(file['filepath'], suggest_file_name(user_id, file['filename'])):
			return False
	return True


def stop_facefusion_task():
	try:
		# 请求facefusion
		resp = requests.get(FACEFUSION_URL + '_stop')

		if resp.status_code != 200:
			server_logger.exception(f"[FaceFusion stop failed] {resp.status_code}")
			return False

		server_logger.info("[FaceFusion] stop task successfully")
		return True

	except Exception as e:
		server_logger.exception(f"[FaceFusion stop exception] {e}")

		return False


def facefusion_image_interval(source_image_path, target_image_path, image_output_path):
	start_time = time.time()
	server_logger.info("[FaceFusionImage] Start facefusion image process...")
	try:
		# 请求facefusion
		request_data = {
			"source_path": os.path.abspath(source_image_path),
			"target_path": os.path.abspath(target_image_path),
			"output_path": os.path.abspath(image_output_path)
		}
		try:
			resp = requests.post(FACEFUSION_URL, json=request_data, timeout=15)

			if resp.status_code != 200:
				server_logger.exception(f"[Image generation failed] {resp.status_code}")
				return False, None

		except requests.exceptions.Timeout:
			if not stop_facefusion_task():
				return False, None

		# 压缩
		img = Image.open(image_output_path)

		file_name, file_extension = image_output_path.rsplit('.', 1)
		jpg_path = f"{file_name}.jpg"

		# 以指定质量保存压缩后的结果
		img.save(jpg_path, quality=100)

		# 移除png原图
		os.remove(image_output_path)

		end_time = round(time.time() - start_time, 2)
		server_logger.info(f"[FaceFusionImage] Finish facefusion image process in {end_time} seconds.")

		return True, jpg_path
	except Exception as e:
		server_logger.exception(f"[Image generation exception] {e}")

		return False, None


def facefusion_image(source_image_path, images_folder, output_path, image_options):
	quality = image_options['quality']
	thumbnail_width = image_options['thumbnail_width']

	target_image_paths = find_png_files(images_folder)
	for i, target_image_path in enumerate(target_image_paths):

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
	start_time = time.time()
	server_logger.info("[FaceFusionVideo] Start facefusion video process...")
	try:
		video_output_path = output_path + ".mp4"
		# 请求facefusion
		request_data = {
			"source_path": os.path.abspath(source_image_path),
			"target_path": os.path.abspath(video_path),
			"output_path": os.path.abspath(video_output_path)
		}
		try:
			resp = requests.post(FACEFUSION_URL, json=request_data, timeout=40)

			if resp.status_code != 200:
				server_logger.exception(f"[Video generation failed] {resp.status_code}")
				return False

		except requests.exceptions.Timeout:
			if not stop_facefusion_task():
				return False

		end_time = round(time.time() - start_time, 2)
		server_logger.info(f"[FaceFusionVideo] Finish facefusion video process in {end_time} seconds.")
		return video_output_path

	except Exception as e:
		server_logger.exception(f"[Video generation exception] {e}")

		return None


def face_swap_internal(task_id, args):
	result = False
	start_time = time.time()
	server_logger.info(f"[{task_id}] Start process...")

	# 清除临时文件夹内容
	clear_folder(TEMP_OUTPUT_DIR)

	user_id = args['user_id']

	task_type = args['task_type']
	if task_type == "upscale":
		# 下载视频
		input_path = download_file(args["video_url"])

		if input_path:
			file_name = f'{task_id}_upscale.mp4'
			# 输出文件路径
			output_file_path = os.path.join(TEMP_OUTPUT_DIR, file_name)
			if upscale_process(input_path, output_file_path):
				# 生成视频缩略图
				extract_video_cover(output_file_path)
				# 上传到oss
				result = upload_files_oss(TEMP_OUTPUT_DIR, user_id)

	elif task_type == "image":
		# 下载头像
		source_image_path = download_file(args["avatar_url"])

		if source_image_path:
			ue_json_data = args["ue_json_data"]

			# 输出目录
			output_path = os.path.join(TEMP_OUTPUT_DIR, f"{task_id}")

			server_logger.info("UE...")
			# UE生成图像
			images_folder = ue_process(ue_json_data)

			server_logger.info("FaceFusion image...")

			# facefusion图像
			if facefusion_image(source_image_path, images_folder, output_path, ue_json_data['image_options']):
				# 上传到oss
				result = upload_files_oss(TEMP_OUTPUT_DIR, user_id)

	elif task_type == "video":
		# 下载头像
		source_image_path = download_file(args["avatar_url"])

		if source_image_path:
			ue_json_data = args["ue_json_data"]
			output_path = os.path.join(TEMP_OUTPUT_DIR, f"{task_id}")

			server_logger.info("UE...")
			# UE生成图像
			images_folder = ue_process(ue_json_data)
			# 获取生成的图像
			target_image_path = find_png_files(images_folder)[0]
			# 临时图像文件
			image_output_path = os.path.join(TEMP_DIR, 'temp.png')

			server_logger.info("Pre swap face...")
			# 首次换脸
			first_result, image_output_path = facefusion_image_interval(source_image_path, target_image_path, image_output_path)
			# 首次换脸成功
			if first_result:
				server_logger.info("PixVerse...")
				# 处理视频
				file_name = f'{task_id}.mp4'
				# 临时视频文件
				video_path = os.path.join(TEMP_OUTPUT_DIR, file_name)
				if pixverse_process(image_output_path, video_path, ue_json_data['video_options']):
					server_logger.info("Process video...")

					# 视频换脸
					video_output_path = facefusion_video(source_image_path, video_path, output_path)
					if video_output_path:
						# 生成视频缩略图
						extract_video_cover(video_output_path)
						# 上传到oss
						result = upload_files_oss(TEMP_OUTPUT_DIR, user_id)

	else:
		server_logger.info(f"[{task_id}] Unsupported task type.")

	end_time = round(time.time() - start_time, 2)
	server_logger.info(f"[{task_id}] Finish process in {end_time} seconds.")

	return result
