import uvicorn
from fastapi import FastAPI

from routes.activities import router as activities_router
from routes.organizations import router as organization_router

app = FastAPI()
app.include_router(organization_router, prefix="/org")
app.include_router(activities_router, prefix="/activity")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
