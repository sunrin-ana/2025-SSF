from .router.router import router
import sys
from pathlib import Path
from Backend.utils.run_server import init_FastAPI

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

app = init_FastAPI()

app.include_router(router)
