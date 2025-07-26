from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # API key dari environment

TOPIK_DIIZINKAN = ["dampak sosial informatika", "etika digital", "privasi", "jejak digital"]

class Pertanyaan(BaseModel):
    teks: str

@app.post("/tanya")
async def tanya_ai(data: Pertanyaan):
    pertanyaan = data.teks.lower()

    if not any(topik in pertanyaan for topik in TOPIK_DIIZINKAN):
        return {"jawaban": "Pertanyaan ini di luar materi pelajaran."}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {"parts": [{"text": f"Jawab pertanyaan berikut secara singkat dan sesuai pelajaran SMP: {pertanyaan}"}]}
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    hasil = response.json()

    if "candidates" in hasil:
        jawaban = hasil["candidates"][0]["content"]["parts"][0]["text"]
    else:
        jawaban = "Maaf, terjadi kesalahan dalam menjawab."

    return {"jawaban": jawaban}
