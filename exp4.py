# for Authorize Enter : mlops123.
from fastapi import FastAPI, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
import pickle
import numpy as np
from pydantic import BaseModel

API_KEY = "mlops123"
api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)

app = FastAPI(title="Iris Prediction API", version="1.0.0", description="Secure Iris Prediction API with API Key")

# Load your trained model
model = pickle.load(open("model.pkl", "rb"))

# Request and Response models
class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class IrisResponse(BaseModel):
    prediction: str

# API key verification
def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=401, detail="Invalid API Key")

# Secure endpoint
@app.post("/predict", response_model=IrisResponse, tags=["Prediction"])
def predict(data: IrisRequest, api_key: str = Security(verify_api_key)):
    input_data = np.array([[ 
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]])
    pred = model.predict(input_data)[0]
    flower_names = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}
    return IrisResponse(prediction=flower_names[int(pred)])

# Optional: Custom OpenAPI to make sure security appears
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "x-api-key"
        }
    }
    # Apply security globally (all endpoints)
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"APIKeyHeader": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi