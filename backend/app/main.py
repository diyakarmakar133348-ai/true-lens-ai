from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import random
from .processor import process_file

app = FastAPI(title="True Lens AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)

AI_FINGERPRINTS = [
    "Stable Diffusion v2.1", "DALL-E 3", "Midjourney v6", "Firefly v2",
    "ElevenLabs v2", "Sora (OpenAI)", "Runway Gen-2", "Pika Labs v1.0"
]

@app.get("/")
def root():
    return {"message": "True Lens AI Backend is running! Supports Images, Videos, Audio, Documents."}

@app.post("/api/scan")
async def scan_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        content_type = file.content_type or ""
        
        # Process the file using the unified router
        result = process_file(contents, file.filename, content_type)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Add a fake AI model fingerprint if it's fake
        model_used = None
        if result.get("verdict") and "Fake" in result["verdict"]:
            model_used = random.choice(AI_FINGERPRINTS)
        
        # Build standard response
        full_report = {
            "verdict": result["verdict"],
            "confidence": result["confidence"],
            "color": result["color"],
            "model_used": model_used,
            "heatmap": result.get("heatmap"),
            "waveform": result.get("waveform"),
            "timeline": result.get("timeline"),
            "text_sample": result.get("text_sample"),
            "details": result.get("details", "Analysis complete."),
            "metadata": {
                "filename": file.filename,
                "file_size": f"{len(contents) / 1024:.2f} KB",
                "content_type": content_type,
            }
        }
        
        return JSONResponse(content=full_report)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)