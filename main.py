from fastapi import FastAPI
from routers import upload_router, train_router, convert_router, download_router, health, download_coreml_model, synthesize_batch

app = FastAPI(title="MyChildBookReading Voice Training API")

# 📌 라우터 등록
app.include_router(upload_router.router)
app.include_router(train_router.router)
app.include_router(convert_router.router)
app.include_router(download_router.router)
app.include_router(download_coreml_model.router)
app.include_router(health.router)
app.include_router(synthesize_batch.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8500)
