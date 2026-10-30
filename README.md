# Car Price Prediction System

An end-to-end machine learning project that estimates a used car's price.

## Structure
```
app.py               Streamlit web UI
src/config.py        Columns, paths, currency
src/generate_data.py Synthetic dataset generator (use if you have no real data)
src/train.py         Trains Ridge / RandomForest / GradientBoosting, keeps the best
src/predict.py       Prediction module + CLI
data/cars.csv        Dataset (generated or your own)
models/              Saved model + metrics
```

## Quick start
```bash
pip install -r requirements.txt
python src/generate_data.py      # skip if you have your own data/cars.csv
python src/train.py              # trains, compares, saves best model
python src/predict.py --brand BMW --age 3 --km_driven 30000 --engine_cc 2000 --power_hp 180
streamlit run app.py             # web interface
```

## Using real data
Place a CSV at `data/cars.csv` with columns: brand, fuel_type, transmission, owner_type,
age, km_driven, engine_cc, power_hp, mileage_kmpl, seats, price. Rename/adjust columns in
`src/config.py` as needed, then re-run `python src/train.py`.

## How it works
- Preprocessing: standard scaling for numeric features, one-hot encoding for categoricals.
- The model predicts log(price) so errors scale with price, then converts back.
- Models are tuned with 3-fold grid search; the lowest test RMSE wins.
- Metrics: MAE, RMSE, R², MAPE on a held-out 20% test set.

## Ideas to extend
Add car model/variant, location, or accident history; try XGBoost/LightGBM; add
SHAP explanations; expose a FastAPI endpoint; track experiments with MLflow.

## Deploy on Streamlit Community Cloud
1. Push this folder to a GitHub repo (keep `app.py` and `requirements.txt` at the repo root;
   commit `data/` and `models/` too).
2. Go to https://share.streamlit.io, sign in with GitHub, click **Create app**.
3. Choose the repo and branch, set **Main file path** to `app.py`, then **Deploy**.
4. If the saved model is missing or was built with a different scikit-learn version, the app
   retrains a quick model automatically on first launch (about a minute).

To retrain with full tuning after changing data, run `python src/train.py` locally and commit
the new `models/` files.
