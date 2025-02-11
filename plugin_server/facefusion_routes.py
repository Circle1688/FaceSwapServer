import os

from fastapi import APIRouter, Depends, HTTPException, status

from plugin_server.gallery_routes import get_avatar_filepath, get_gallery_dir
from plugin_server.schemas import *
from plugin_server.TaskManager import Task
from plugin_server.auth import get_current_user_id

router = APIRouter()


tasks_manager = Task()


@router.post("/generate")
async def generate(request: GenerateRequest, user_id: int = Depends(get_current_user_id)):

	# 请求数据
	ue_json_data = request.dict()

	# 获取头像
	source_image_path = get_avatar_filepath(user_id)

	if not os.path.exists(source_image_path):
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User avatar not found")

	# 确保目录存在
	store_dir = get_gallery_dir(user_id)

	if not os.path.exists(store_dir):
		os.makedirs(store_dir)

	args = {"source_image_path": source_image_path, "ue_json_data": ue_json_data, "output_path": store_dir, "video": False}

	task_id = await tasks_manager.handle_request(args)
	return {"task_id": task_id}


@router.post("/generate_video")
async def generate_video(request: VideoGenerateRequest, user_id: int = Depends(get_current_user_id)):
	# 请求数据
	ue_json_data = request.dict()

	source_image_path = get_avatar_filepath(user_id)

	if not os.path.exists(source_image_path):
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User avatar not found")

	# 确保目录存在
	store_dir = get_gallery_dir(user_id)

	if not os.path.exists(store_dir):
		os.makedirs(store_dir)

	args = {"source_image_path": source_image_path, "ue_json_data": ue_json_data, "output_path": store_dir, "video": True}

	task_id = await tasks_manager.handle_request(args)
	return {"task_id": task_id}


@router.get("/generate/{task_id}")
async def generate_status(task_id: str, user_id: int = Depends(get_current_user_id)):
	if task_id not in tasks_manager.tasks:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
	return {"status": tasks_manager.tasks[task_id], "position": tasks_manager.get_queue_position(task_id)}
