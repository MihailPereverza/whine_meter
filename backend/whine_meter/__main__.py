import uvicorn

uvicorn.run("whine_meter.backend:app", host="0.0.0.0", port=8080)
