from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
from price_bounds import PriceModelWithBounds

# ===========================
# Load trained artifacts
# ===========================
encoder = joblib.load("encoder.joblib") 
scaler  = joblib.load("scaler.joblib")  
model   = joblib.load("xgb_price_bundle.joblib")   
wrapper = PriceModelWithBounds(**model)

class InputData(BaseModel):
    date: str
    bedrooms: float
    bathrooms: float
    sqft_living: float
    sqft_lot: float
    floors: float
    waterfront: int
    view: int
    condition: int
    sqft_above: float
    sqft_basement: float
    yr_built: int
    yr_renovated: int
    city: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "House Price Model API is running!"}

def safe_label_transform(le, s: pd.Series):
    """LabelEncoder doesn't handle unseen labels. Fail fast with a helpful message."""
    unknown = s[~s.isin(le.classes_)]
    if not unknown.empty:
        allowed = ", ".join(map(str, le.classes_[:10]))
        more = "…" if len(le.classes_) > 10 else ""
        raise ValueError(f"Unknown city value(s): {sorted(unknown.unique())}. "
                         f"Allowed examples: {allowed}{more}")
    return le.transform(s)

@app.post("/predict")
def predict(data: InputData):
    try:
        row = data.model_dump() if hasattr(data, "model_dump") else data.dict()
        df = pd.DataFrame([row])

        dt = pd.to_datetime(df["date"], errors="coerce")
        if dt.isna().any():
            raise ValueError("Invalid 'date' format; e.g., '2014-05-02'.")

        df["renovated"] = (df["yr_renovated"] > 0).astype(int)
        df["year"] = dt.dt.year
        df["month"] = dt.dt.month
        df = df.drop(columns=["date"])

        df["city"] = safe_label_transform(encoder, df["city"])

        num_cols = [
            "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors",
            "sqft_above", "sqft_basement", "yr_built", "yr_renovated",
        ]
        df[num_cols] = scaler.transform(df[num_cols])

        result = wrapper.predict_with_bounds(df)
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {e}")
