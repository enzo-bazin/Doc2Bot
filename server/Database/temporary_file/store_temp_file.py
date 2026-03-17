import aiofiles
from fastapi import UploadFile
from os import mkdir, path

async def store_file(user_id, in_file: UploadFile):
    if not path.exists(f"server/Database/temporary_file/temp_{user_id}"):
        mkdir(f"server/Database/temporary_file/temp_{user_id}")
    async with aiofiles.open(f"server/Database/temporary_file/temp_{user_id}/{in_file.filename}", 'wb') as out_file:
        content = await in_file.read()
        await out_file.write(content)