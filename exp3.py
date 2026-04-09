from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import pickle
import numpy as np
from pydantic import BaseModel, Field
import logging

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

API_KEY = "12345"

try:
    model = pickle.load(open("model.pkl", "rb"))
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Model loading failed: {str(e)}")
    model = None

try:
    scaler = pickle.load(open("scaler.pkl", "rb"))
    logger.info("Scaler loaded successfully")
except:
    scaler = None
    logger.warning("Scaler not found, using raw input")

class IrisRequest(BaseModel):
    api_key: str
    sepal_length: float = Field(..., gt=0, lt=10)
    sepal_width: float = Field(..., gt=0, lt=10)
    petal_length: float = Field(..., gt=0, lt=10)
    petal_width: float = Field(..., gt=0, lt=10)

class IrisResponse(BaseModel):
    prediction: str

@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    logger.info(f"Request: {request.method} {request.url} | Body: {body.decode()}")
    response = await call_next(request)
    logger.info(f"Response Status: {response.status_code}")
    return response

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Error: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Error: {str(exc)}")
    return JSONResponse(status_code=500, content={"error": "Internal server error"})

@app.post("/predict", response_model=IrisResponse)
def predict(data: IrisRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    if data.api_key != API_KEY:
        logger.warning("Unauthorized access attempt")
        raise HTTPException(status_code=401, detail="Invalid API Key")
    try:
        input_data = np.array([[ 
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width
        ]])
        if scaler:
            input_data = scaler.transform(input_data)
        pred = model.predict(input_data)[0]
        flower_names = {
            0: "Setosa",
            1: "Versicolor",
            2: "Virginica"
        }
        result = flower_names.get(int(pred), "Unknown")
        logger.info(f"Prediction Success: {result}")
        return IrisResponse(prediction=result)
    except Exception as e:
        logger.error(f"Prediction Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed")

@app.get("/")
def home():
<<<<<<< HEAD
    return {"message": "FastAPI Logging & Error Handling Running"}
=======
    return {"message": "FastAPI Logging & Error Handling Running"}
>>>>>>> 1393b42165e9824f1f45aeccb04286db281b8858
