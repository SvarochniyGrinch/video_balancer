import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["/project/source", "/libs/shared",],)
