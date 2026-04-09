import uvicorn

# If run directly from the terminal, execute the server startup block below.
# If imported by another file, skip this block entirely to prevent the server from accidentally auto-starting.
if __name__ == "__main__":
    uvicorn.run("app.app:app", host = "0.0.0.0", port = 8000, reload = True)