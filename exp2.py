from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel

app = FastAPI()

model = pickle.load(open("model.pkl", "rb"))

class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class IrisResponse(BaseModel):
    prediction: str

@app.post("/predict", response_model=IrisResponse)
def predict(data: IrisRequest):

    input_data = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]])

    pred = model.predict(input_data)[0]

    flower_names = {
        0: "Setosa",
        1: "Versicolor",
        2: "Virginica"
    }

    result = flower_names[int(pred)]

    return IrisResponse(prediction=result)
