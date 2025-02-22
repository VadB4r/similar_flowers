from database import FlowDoc, VectorDB
from embedder import Embedder
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import numpy as np

app = FastAPI()
db = VectorDB()
db.fill_db()
embedder = Embedder()


class ImageRequest(BaseModel):
    image_path: str



@app.post("/get_similars")
async def detect_image(image_request: ImageRequest) -> List[Dict[str, str]]:
    try:
        vec = embedder.get_embedding(image_request.image_path)

        query = FlowDoc(text=image_request.image_path, embedding=vec)
        results = db.find_sims(query)

        return [
            {
                "image_path": match.text,
                "similarity_score": score
            } for match, score in zip(results[0].matches[1:], results[0].scores[1:])
        ]

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

