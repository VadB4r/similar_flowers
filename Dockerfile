FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel

RUN pip install --no-cache-dir \
    matplotlib \
    scikit-learn \
    fastapi \
    uvicorn \
    joblib \
    pillow \
    vectordb

WORKDIR /app

COPY ./data/ ./data/
COPY ./models/vgg_flower_trained.pt ./models/vgg_flower_trained.pt
COPY database.py database.py
COPY embedder.py embedder.py
COPY service.py service.py

EXPOSE 8000

CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]

