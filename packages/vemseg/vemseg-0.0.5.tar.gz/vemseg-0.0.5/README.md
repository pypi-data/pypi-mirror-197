[//]: # (<img width="250"  src="https://github.com/MatousE/vemseg/blob/main/imgs/VEMSEG-FINAL.svg"> )

# Volume Electron Microscopy SEGmentation
[![tests](https://github.com/MatousE/vemseg/workflows/tests/badge.svg)](https://github.com/MatousE/vemseg/actions)

A package for the segmentation of volume electron microscopy images using XGBoost.

## Installation

You can install `vemseg` via [pip]:

    pip install vemseg

## Usage
Shown below are some example uses of the VEMClassifier and some other functionality provided 
by the `vemseg` package.

```python
import vemseg as vem
from skimage.io import imread

X = imread("train_image.tiff")
y = imread("train_labels.tiff")
mask = imread('train_mask.tiff')

clf = vem.VEMClassifier(max_depth=4,
                         n_estimators=400,
                         learning_rate=0.01,
                         verbosity=0)

features = clf.set_features(
    ["sobel_of_gaussian_blur","laplace_box_of_gaussian_blur", "original"], 
    range(1, 4)
)

clf.fit(X, y, mask=mask)
```
We then use `clf.predict` to get the prediction from the trained
classifier. We can use the `show` flag to generate an image of the
predictions.
```python
prediction = clf.predict(X, show=True, mask=mask)
```
<img width="400"  src="https://github.com/MatousE/vemseg/blob/main/imgs/example_output.tiff">

We can then plot the features importance like so, with fig size indicating the size of the plot.
```python

clf.feature_importance(fig_size=(20, 10))
```

<img width="800"  src="https://github.com/MatousE/vemseg/blob/main/imgs/example_feature_graph.tiff">

Deciding what hyperparameters to use can often be very difficult, so we can use an adaptation
of sklearns GridSearchCV to determine which hyperparameters work best.

```python
parameters = {
    'max_depth': range(2, 5, 1),
    'n_estimators': range(200, 500, 100)
}

grid_search = clf.GridSearchCV(
    X,
    y,
    param_grid=parameters,
    n_jobs=10,
    cv=10,
    verbose=True,
    update_params=True,
    mask=mask,
)

print(grid_search.best_estimator_)
```
Will output
```
Fitting 10 folds for each of 9 candidates, totalling 90 fits
VEMClassifier(base_score=0.5, booster='gbtree', callbacks=None,
              colsample_bylevel=1, colsample_bynode=1, colsample_bytree=1,
              early_stopping_rounds=None, enable_categorical=False,
              eval_metric=None, feature_types=None, gamma=0, gpu_id=-1,
              grow_policy='depthwise', importance_type=None,
              interaction_constraints='', learning_rate=0.300000012,
              max_bin=256, max_cat_threshold=64, max_cat_to_onehot=4,
              max_delta_step=0, max_depth=3, max_leaves=0, min_child_weight=1,
              missing=nan, monotone_constraints='()', n_estimators=200,
              n_jobs=0, num_parallel_tree=1, objective='binary:logistic',
              predictor='auto', ...)
```
After completing training one can save the model to be reused like so.
```python
clf.save_model('model.json')
```
And to reload the model from the JSON file one simply has to initialise a new
VEMClassifier and then load the model.

```python
import vemseg

pre_trained_model = vem.VEMClassifier()
pre_trained_model.load_model('model.json')
```
## License

Distributed under the terms of the [BSD-3] license,
"napari-vemseg" is free and open source software

## Contribute to VEMseg
Contributions are very welcome.

## Similar Software
Full credit to the following software for inspiration and use within this tool.
* [apoc](https://github.com/haesleinhuepf/apoc)
* [XGBoost](https://github.com/dmlc/xgboost)
* [scikit-learn](https://scikit-learn.org/stable/)

## Reference

[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[pip]: https://pypi.org/project/pip/
