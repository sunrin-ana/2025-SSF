import sys
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


app = FastAPI(
    title="싸이월드 - 추억 속으로",
    description="2000년대 감성의 소셜 네트워크 서비스",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/public", StaticFiles(directory="public"), name="public")


# 정적 파일 서빙
async def init_folders(app: FastAPI):
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


async def init_db():

    for service in os.listdir("Backend/services"):
        try:
            if service.endswith(".py"):
                module_name = "Backend.services." + service[:-3]
                module = __import__(module_name, fromlist=[""])
                service_class_name = service[:-3].split("_")[0] + "Service"
                service_class_name = service_class_name.replace(
                    service_class_name[0], service_class_name[0].upper(), 1
                )
                service_class = getattr(module, service_class_name)

                await service_class.init_db()
                print(f"{service_class_name} : init_db")

        except Exception as e:
            print(f"failed to init_db {service}")
            print(e)


async def startup_event():
    await init_folders(app)
    await init_db()


def init_FastAPI() -> FastAPI:
    app.add_event_handler("startup", startup_event)
    return app
