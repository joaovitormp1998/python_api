from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from importlib import import_module

from dotenv import load_dotenv
from os import listdir, getenv

load_dotenv()

# app = FastAPI(docs_url = getenv('DOCS_PATH'), redoc_url = getenv('REDOCS_PATH'))
app = FastAPI(docs_url='/docs')
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

def load(path = 'routers'):
    files = listdir(path)
    files.sort()

    for file in files:
        if not file.startswith('__'):
            if file.endswith('.py'):
                module = import_module(
                    f'{path}.{file}'.replace('.py', '').replace('/', '.'))
                app.include_router(module.router)

            else:
                load(path + '/' + file)

load()

if __name__ == '__main__':
    from uvicorn import run
    run(app, host = '0.0.0.0', port = 8000)


@app.get('')
def read_root():
    return {'API - Tutorcast': 'Platform'}
