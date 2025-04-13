"""

Main entry point for apps routers

routers structure:

api: (current dir)
    - app_name_1 (some app router dir)
        - router.py (app main router contained file)
        - dto (optional dtos contained dir/file)
        - ... (optional utils contained dirs/files)
    - app_name_2 (other apps)
    ...

    - router: (current file)

    imports structure:
    from fastapi import APIRouter

    ...
    from app_name_N import router as app_name_N_router
    ...

    router = APIRouter()

    ...
    router.include(app_name_N_router)
    ...
...

"""

from fastapi import APIRouter

router = APIRouter()

