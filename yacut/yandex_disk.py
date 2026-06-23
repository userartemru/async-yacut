import asyncio
from urllib.parse import unquote

import aiohttp

from yacut import app


API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


def get_auth_headers():
    return {'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'}


async def upload_files_to_yandex_disk(files):
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.ensure_future(upload_file_and_get_link(session, file))
            for file in files
            if file.filename
        ]
        return await asyncio.gather(*tasks)


async def upload_file_and_get_link(session, file):
    upload_url = await get_upload_url(session, file.filename)
    location = await upload_file(session, upload_url, file)
    download_link = await get_download_link(session, location)
    return file.filename, download_link


async def get_upload_url(session, filename):
    async with session.get(
        REQUEST_UPLOAD_URL,
        headers=get_auth_headers(),
        params={'path': f'app:/{filename}', 'overwrite': 'True'},
    ) as response:
        data = await response.json()
        return data['href']


async def upload_file(session, upload_url, file):
    async with session.put(upload_url, data=file.read()) as response:
        location = response.headers['Location']
        return unquote(location).replace('/disk', '')


async def get_download_link(session, location):
    async with session.get(
        DOWNLOAD_LINK_URL,
        headers=get_auth_headers(),
        params={'path': location},
    ) as response:
        data = await response.json()
        return data['href']
