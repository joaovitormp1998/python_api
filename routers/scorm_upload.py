from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from tempfile import NamedTemporaryFile
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from os.path import join, relpath, sep
from os import walk
from io import BytesIO

from database.central.scorm import ScormORM
from utils.digital_ocean import s3

router = APIRouter(prefix = '/scorm', tags = ['Backoffice - Produtos - Scorm'])


@router.post('', status_code = 201)
async def upload_scorm_zip(tenant_id: str, zip_file: UploadFile = File(...)):
        if not zip_file.filename.endswith('.zip'):
            raise HTTPException(status_code = 400, detail = "O arquivo enviado deve ser um arquivo ZIP.")

        with TemporaryDirectory() as temp_dir:
            dir_ = temp_dir.replace('/tmp', '')
            await ScormORM.create(tenant_id = tenant_id, s3_key = dir_)

            zip_content = await zip_file.read()
            zip_buffer = BytesIO(zip_content)

            with ZipFile(zip_buffer, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            for root, dirs, files in walk(temp_dir):
                for file in files:
                    local_file_path = join(root, file)
                    relative_path = relpath(local_file_path, f'{temp_dir}/html')
                    s3_key = f'scorm/{dir_}/{relative_path.replace(sep, '/')}'

                    s3.upload_file(local_file_path, 'lmsos', s3_key)

        return {"message": "Arquivos enviados com sucesso."}