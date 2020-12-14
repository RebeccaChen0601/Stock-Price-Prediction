# CS451 Project: Tweet Stock Predictor

## Dataset

The [Chirps Dataset](https://github.com/vered1986/Chirps/tree/master/resource) must be available at `datasets/Chirps`.

## Order of Execution

Ensure that the folders exist:
```
analytics/Chirps
models/arima
models/stage1
```

Execute the notebooks in the following order: (with estimated runtime)



1. `[Preproc] Chirps - Preprocessing`: 10 minutes
2. `[Preproc] Stocks - Data Extraction`: 2 minutes
3. `[Model] Baseline - Arima`: 5 minutes
4. `[Model] Stage1 - WordEmbedding`: 40 minutes
5. `[Model] Stag1C- Caching`: 240 minutes
6. `[Model] Stage2 T1 - CNN`: 5 minutes (loading data) + 400 minutes (training)
7. `[Model] Stage2 T1 - CNN-Attention`: 5 minutes (loading data) + 400 minutes (training)
8. `[Eval] DNN Evaluations`: 30 minutes
9. `[Eval] Model Evaluations`: 5 minutes (loading data)

The results can be found in `[Eval] Model Evaluations`.