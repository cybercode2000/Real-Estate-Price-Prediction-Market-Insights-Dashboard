# Real Estate Price Prediction & Recommendation API 🏡

## Overview
This project implements a **Real Estate Price Prediction system** using the **Kaggle House Prices dataset**, powered by **XGBoost** Linear regression for accurate property valuation.  
Beyond predictions, it also provides **property recommendations** (slightly below or above the target price in a given city).

The solution is deployed as a **REST API (FastAPI)**, making it easy for developers to integrate into real estate platforms.

---

## 🔑 Features
- **Price Prediction**: Predicts house prices with high accuracy using XGBoost.  
- **Recommendation Engine**: Suggests houses priced slightly below or above a given budget in a chosen city.  
- **API Endpoint**:  
  - `/predict` → Input property details → Get price prediction + related recommendations.  
- **EDA Insights**: Explored and analyzed price drivers such as size, quality, and location.  

---

## 🛠️ Tech Stack
- Python (Pandas, NumPy, Scikit-learn)  
- XGBoost  
- FastAPI (for API deployment)  
- Kaggle dataset  

---

## 📂 Codebase & Model
The full codebase and the trained `.joblib` model have been pushed to this **public GitHub repo**.  
👉 Anyone interested can clone the repo and give it a quick look.  

```bash
git clone <your-repo-url>
cd <your-repo>
uvicorn app:app --reload --port 8000
```

---

**Response:**
```json
{
  "predicted_price": 302500,
  "recommendations": [
    {"id": 1, "city": "Leeds", "price": 295000, "bedrooms": 3, "bathrooms": 2, "size_sqft": 1750},
    {"id": 2, "city": "Leeds", "price": 310000, "bedrooms": 4, "bathrooms": 3, "size_sqft": 1900}
  ]
}
```
---

## 💡 Looking for Suggestions
Any recommendations for a **JavaScript library** that can display property cards based on parameters like bedrooms, bathrooms, and size?

Potential options I’m exploring:  
- **Material UI (MUI)** → Great for responsive property cards.  
- **Ant Design** → Professional tables & filters.  
- **Leaflet.js (with React-Leaflet)** → For adding geolocation & maps.  

---

## 🙌 Contributions
Contributions, suggestions, and feedback are welcome!  
Fork the repo, open issues, or submit PRs.

---
