from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from backend.app.auth.auth import get_current_user


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.white_list_paths = ["/", "/login", "/register", "/openapi.json"]

    async def dispatch(self, request: Request, call_next):
        print("Проверка url")
        if request.url.path in self.white_list_paths:
            print(f"✅ Точное совпадение: {request.url.path}")
            return await call_next(request)

        try:
            authorization = request.headers.get("Authorization")

            if not authorization:
                token = request.cookies.get("access_token")
                if not token:
                    return RedirectResponse(url="/login")
            else:
                print("Блокируем")
                scheme, token = authorization.split()
                if scheme.lower() != "bearer":
                    return RedirectResponse(url="/login")

            async def get_token():
                return token

            current_user = await get_current_user(token=await get_token())

            request.state.current_user = current_user
            response = await call_next(request)
            return response

        except HTTPException:
            return RedirectResponse(url="/login")
        except Exception:
            return RedirectResponse(url="/login")

