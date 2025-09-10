from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

class PriceModelWithBounds:
    def __init__(self, model, reference_df: pd.DataFrame, price_col: str = "price"):
        self.model = model
        self.reference_df = reference_df.copy()
        self.price_col = price_col

        # ensure numeric + drop NaNs in price
        self.reference_df[self.price_col] = pd.to_numeric(
            self.reference_df[self.price_col], errors="coerce"
        )
        self.reference_df = self.reference_df.dropna(subset=[self.price_col])

    def predict_with_bounds(self, X: pd.DataFrame) -> Dict[str, Any]:
        pred = float(np.asarray(self.model.predict(X))[0])

        df = self.reference_df
        lower_df = df[df[self.price_col] < pred]
        upper_df = df[df[self.price_col] > pred]

        lower_row = (None if lower_df.empty
                     else lower_df.loc[[lower_df[self.price_col].idxmax()]] )
        upper_row = (None if upper_df.empty
                     else upper_df.loc[[upper_df[self.price_col].idxmin()]] )

        # convert rows to plain dicts (JSON-safe)
        to_rec = lambda r: None if r is None else r.to_dict(orient="records")[0]

        return {
            "prediction": round(pred, 2),
            "lower": to_rec(lower_row),
            "upper": to_rec(upper_row),
        }
