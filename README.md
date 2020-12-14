# CS451 Project: Tweet Stock Predictor

## Dataset

The [Chirps Dataset](https://github.com/vered1986/Chirps/tree/master/resource) must be available at `datasets/Chirps`.

## Order of Execution

All packages in `requirements.txt` must be installed.

Ensure that the following folders exist:
```
analytics/Chirps
models/arima
models/stage1
```
Change the number of workers in `[Model] Stage 2 T*` to the number of GPU
machines on your cluster.

Execute the notebooks in the following order: (with estimated runtime)

1. `[Preproc] Chirps - Preprocessing`: 10 minutes
2. `[Preproc] Stocks - Data Extraction`: 2 minutes
3. `[Model] Baseline - Arima`: 5 minutes
4. `[Model] Stage1 - WordEmbedding`: 40 minutes
5. `[Model] Stage1C- Caching`: 240 minutes
6. `[Model] Stage2 T1 - CNN`: 5 minutes (loading data) + 400 minutes (training)
7. `[Model] Stage2 T2 - CNN-Attention`: 5 minutes (loading data) + 400 minutes (training)
8. `[Eval] DNN Evaluations`: 30 minutes
9. `[Eval] Model Evaluations`: 5 minutes (loading data)

The results can be found in `[Eval] Model Evaluations` and `analytics/`

## Possible improvements:

1. Model architecture tuning
2. Add more randomness to the input. In particular remove the 1C Caching stage since it caches some of the randomness.
