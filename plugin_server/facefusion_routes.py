from fastapi import APIRouter, Depends, HTTPException, status

from plugin_server.schemas import *
from plugin_server.TaskManager import Task
from plugin_server.auth import get_current_user_id

router = APIRouter()


tasks_manager = Task()


@router.post("/generate")
async def generate(request: GenerateRequest, user_id: int = Depends(get_current_user_id)):
	# 请求数据
	ue_json_data = request.dict()

	args = {"user_id": user_id, "ue_json_data": ue_json_data, "task_type": "image"}

	task_id = await tasks_manager.handle_request(args)
	return {"task_id": task_id}


@router.post("/generate_video")
async def generate_video(request: VideoGenerateRequest, user_id: int = Depends(get_current_user_id)):
	# 请求数据
	ue_json_data = request.dict()

	args = {"user_id": user_id, "ue_json_data": ue_json_data, "task_type": "video"}

	task_id = await tasks_manager.handle_request(args)
	return {"task_id": task_id}


@router.post("/upscale")
async def upscale(request: UpscaleRequest, user_id: int = Depends(get_current_user_id)):
	# 请求数据
	video_url = request.video_url

	args = {"video_url": video_url, "user_id": user_id, "task_type": "upscale"}

	task_id = await tasks_manager.handle_request(args)
	return {"task_id": task_id}


@router.get("/generate/{task_id}")
async def generate_status(task_id: str, user_id: int = Depends(get_current_user_id)):
	if task_id not in tasks_manager.tasks:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
	return {"status": tasks_manager.tasks[task_id], "position": tasks_manager.get_queue_position(task_id)}
