import aiofiles
from fastapi import UploadFile
import os
import shutil
from server.Utils.constants import settings

async def store_file(user_id, in_file: UploadFile):
    temp_dir = settings.UPLOAD_DIR / f"temp_{user_id}"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = temp_dir / in_file.filename
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await in_file.read()
        await out_file.write(content)

def remove_file(user_id):
    temp_dir = settings.UPLOAD_DIR / f"temp_{user_id}"
    if temp_dir.exists() and temp_dir.is_dir():
        shutil.rmtree(temp_dir)
