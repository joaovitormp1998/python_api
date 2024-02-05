from fastapi import APIRouter, Response, UploadFile, File, Query, Depends
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from utils.digital_ocean import s3

router = APIRouter(prefix = '/scorm/{dir}', tags = ['Backoffice - Produtos - Scorm'])


@router.get('')
async def scorm(dir: str):
    index_html = s3.get_object(
        Bucket='lmsos', Key=f'scorm/{dir}/index.html')['Body'].read().decode('utf-8')
    return Response(content=index_html, media_type='text/html')


@router.get('/{file_name}')
async def statics(dir: str, file_name: str):
    file = s3.get_object(
        Bucket='lmsos', Key=f'scorm/{dir}/{file_name}')['Body'].read().decode('utf-8')

    if file_name.endswith('.js'):
        media_type = 'text/javascript'
    elif file_name.endswith('.css'):
        media_type = 'text/css'
    else:
        media_type = 'text/html'

    return Response(content=file, media_type=media_type)


@router.get('/images/{image_path}')
async def imagens(dir: str, image_path: str):
    img_data = s3.get_object(
        Bucket='lmsos', Key=f'scorm/{dir}/images/{image_path}')['Body'].read()
    return Response(content=img_data, media_type='image/jpeg')