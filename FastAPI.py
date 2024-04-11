from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Загрузка модели для машинного перевода
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-ru-en")

# Модель данных для запроса
class TranslationRequest(BaseModel):
    text: str

# Модель данных для ответа
class TranslationResponse(BaseModel):
    translation: str

# Эндпоинт для машинного перевода
@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    try:
        translated_text = translator(request.text)[0].get('translation_text')
        return {"translation": translated_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Bad Request")
