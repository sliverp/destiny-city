from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.seed import init_db
from app.routers import invite, quiz, test, result, admin, share

app = FastAPI(title="Destiny City API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(invite.router)
app.include_router(quiz.router)
app.include_router(test.router)
app.include_router(result.router)
app.include_router(admin.router)
app.include_router(share.router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/api/health")
def health_check():
    return {"status": "ok"}