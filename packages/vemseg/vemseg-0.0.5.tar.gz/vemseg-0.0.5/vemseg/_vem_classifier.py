# Author: Matouš Elphick
# License: BSD 3 clause
import matplotlib.pyplot as plt
import numpy as np
import pyclesperanto_prototype as cle
from typing import Any, Optional, Sequence, Tuple, Union
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier, XGBModel
from xgboost.callback import TrainingCallback
from xgboost.core import Booster, ArrayLike
from ._utils import to_np, pre_process, generate_feature_stack


class VEMClassifier(XGBClassifier):
    def __init__(self,
                 *,
                 features: Optional[str] = 'original',
                 verbosity: Optional[int] = 0,
                 **kwargs: Any):
        """
        A XGBoost classifier with added functionality optimised
        for Volume Electron Microscopy data.

        Args:
            **kwargs: Parameters for XGBoost classifier.

        See Also:
            https://xgboost.readthedocs.io/en/stable/python/python_api.html#xgboost.XGBClassifier
        """
        self.features = features
        super().__init__(verbosity=verbosity, **kwargs)

    def plot_feature_importance(self, fig_size: Optional[tuple] = (10, 5)):
        """
        Function to plot the feature importance after training is completed.

        Args:
            fig_size: Size of the figure to be outputted.

        Returns:
            Figure showing the importance of features in descending order.
        """

        feature_names = self.features.split(' ')
        sorted_idx = super().feature_importances_.argsort()

        plt.figure(figsize=fig_size)
        plt.barh([feature_names[i] for i in sorted_idx], super().feature_importances_[sorted_idx])
        plt.xlabel("Xgboost Feature Importance")
        plt.tight_layout()
        plt.show()

    def GridSearchCV(self,
                     X: ArrayLike,
                     y: ArrayLike,
                     param_grid: dict,
                     *,
                     mask: Optional[ArrayLike] = None,
                     rem_membrane: Optional[bool] = False,
                     update_params: Optional[bool] = False,
                     **kwargs
                     ) -> "GridSearchCV":
        """
        Function to use sklearn GridSearchCV on
        an initialised VEMClassifier and optionally
        update the parameters of the VEMClassifier using
        the best parameters from the GridSearchCV.

        Args:
            X: Image feature matrix.
            y: Image Labels.
            param_grid: dict or list of dictionaries. Dictionary with
                parameters names (`str`) as keys and lists of parameter
                settings.
            mask: Apply binary mask to X.
            rem_membrane:  Remove membrane from X after applying mask.
            update_params: Option to take the parameters from GridSearch best
                VEMClassifier and update the current parameters.
            **kwargs: Custom arguments for the GridSearchCV

        Returns:
            Resulting GridSearchCV object.
        See Also:
            https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
        """

        # If feature set is already defined
        if X.ndim != 2 and y.ndim != 1:
            X = pre_process(X, mask=mask, rem_membrane=rem_membrane)

            train_features = np.asarray(generate_feature_stack(X, self.features))

            X_test, y_test, _ = to_np(train_features, y)
        else:
            X_test = X
            y_test = y

        grid_search = GridSearchCV(
            estimator=self,
            param_grid=param_grid,
            **kwargs,
        )

        grid_search.fit(X_test, y_test)

        if update_params:
            params = grid_search.best_estimator_.get_params()
            super().set_params(**params)

        return grid_search

    def fit(
            self,
            X: ArrayLike,
            y: ArrayLike,
            *,
            verbose: Optional[Union[bool, int]] = False,
            xgb_model: Optional[Union[Booster, str, XGBModel]] = None,
            callbacks: Optional[Sequence[TrainingCallback]] = None,
            mask: Optional[ArrayLike] = None,
            rem_membrane: bool = False,
    ) -> "XGBClassifier":
        """
        Function to fit VEMClassifier and optionally remove mask the
        inputs X dnd Y, and or remove the membrane.

        Note that calling fit() multiple times will cause the model
        object to be re-fit from scratch. To resume training from a
        previous checkpoint, explicitly pass xgb_model argument.

        Args:
            X: Image feature matrix.
            y: Image labels.
            verbose: If verbose is True and an evaluation set is used, the evaluation
                metric measured on the validation set is printed to stdout at each
                boosting stage. If verbose is an integer, the evaluation metric is
                printed at each verbose boosting stage. The last boosting stage /
                the boosting stage found by using early_stopping_rounds is also printed.
            xgb_model: file name of stored XGBoost model or ‘Booster’ instance XGBoost
                model to be loaded before training (allows training continuation).
            callbacks: Deprecated since version 1.6.0: Use `callbacks` in `__init__()` or
                `set_params()` instead.
            mask: Apply binary mask to X.
            rem_membrane: Remove membrane from X after applying mask.

        Returns:
            VEMClassifier
        See Also:
            https://xgboost.readthedocs.io/en/stable/python/python_api.html#xgboost.XGBClassifier.fit
        """

        if X.ndim == 2 and y.ndim == 1:
            return super().fit(X,
                               y,
                               sample_weight=None,
                               base_margin=None,
                               eval_set=None,
                               early_stopping_rounds=None,
                               verbose=verbose,
                               xgb_model=xgb_model,
                               sample_weight_eval_set=None,
                               base_margin_eval_set=None,
                               eval_metric=None,
                               feature_weights=None,
                               callbacks=callbacks)

        X = pre_process(X, mask=mask, rem_membrane=rem_membrane)
        train_features = generate_feature_stack(X, self.features)

        X_train, y_train, _ = to_np(train_features, y)

        return super().fit(X_train,
                           y_train,
                           sample_weight=None,
                           base_margin=None,
                           eval_set=None,
                           early_stopping_rounds=None,
                           verbose=verbose,
                           xgb_model=xgb_model,
                           sample_weight_eval_set=None,
                           base_margin_eval_set=None,
                           eval_metric=None,
                           feature_weights=None,
                           callbacks=callbacks)

    def predict(
            self,
            X: ArrayLike,
            *,
            output_margin: bool = False,
            validate_features: bool = True,
            iteration_range: Optional[Tuple[int, int]] = None,
            show: Optional[bool] = False,
            mask: Optional[np.ndarray] = None,
            rem_membrane: Optional[bool] = False
    ) -> np.ndarray:
        """
        Predict with X and optionally remove mask the inputs X dnd Y,
        and or remove the membrane. If the model is trained with early stopping,
        then best_iteration is used automatically. For tree models, when data
        is on GPU, like cupy array or cuDF dataframe and predictor is not
        specified, the prediction is run on GPU automatically,
        otherwise it will run on CPU.

        Args:
            X: Image feature matrix.
            output_margin: Whether to output the raw untransformed margin value.
            validate_features: When this is True, validate that the Booster’s
                and data’s feature_names are identical. Otherwise, it is assumed
                that the feature_names are the same.
            iteration_range: Specifies which layer of trees are used in prediction.
                For example, if a random forest is trained with 100 rounds. Specifying
                 `iteration_range=(10, 20)`, then only the forests built during [10, 20)
                 (half open set) rounds are used in this prediction.
            show: Output an image of the predictions.
            mask: Apply binary mask to X.
            rem_membrane: Remove membrane from X after applying mask.

        Returns:
            VEMClassifier prediction.
        See Also:
            https://xgboost.readthedocs.io/en/stable/python/python_api.html#xgboost.XGBClassifier.predict
        """

        if X.ndim == 2:
            predictions = super().predict(X,
                                          ntree_limit=None,
                                          output_margin=output_margin,
                                          validate_features=validate_features,
                                          base_margin=None,
                                          iteration_range=iteration_range)
            if show:
                cle.imshow(predictions.reshape(X.shape), labels=True)

            return predictions

        processed = pre_process(X, mask=mask, rem_membrane=rem_membrane)
        X_features = generate_feature_stack(processed, self.features)
        X_predict = to_np(X_features)

        predictions = super().predict(X_predict,
                                      ntree_limit=None,
                                      output_margin=output_margin,
                                      validate_features=validate_features,
                                      base_margin=None,
                                      iteration_range=iteration_range)
        predictions += 1

        if show:
            cle.imshow(predictions.reshape(X.shape), labels=True)

        return predictions.reshape(X.shape)

    def predict_proba(
            self,
            X: ArrayLike,
            validate_features: bool = True,
            iteration_range: Optional[Tuple[int, int]] = None,
            mask=None,
            rem_membrane: bool = False,
    ) -> np.ndarray:
        """
        Predict the probability of each `X` example being of a given class.
        Optionally remove mask the inputs X dnd Y, and or remove the membrane.

        Args:
            X: Image feature matrix.
            validate_features: When this is True, validate that the Booster’s
                and data’s feature_names are identical. Otherwise, it is assumed
                that the feature_names are the same.
            iteration_range: Specifies which layer of trees are used in prediction.
                For example, if a random forest is trained with 100 rounds. Specifying
                 `iteration_range=(10, 20)`, then only the forests built during [10, 20)
                 (half open set) rounds are used in this prediction.
            mask: Apply binary mask to X.
            rem_membrane: Remove membrane from X after applying mask.

        Returns:
            prediction :
            a four dimensional numpy array of shape array-like of shape (n_classes, Z, X, Y)
            with the probability of each data example being of a given class.
        """
        if X.ndim == 2:
            predictions = super().predict_proba(X,
                                                ntree_limit=None,
                                                validate_features=validate_features,
                                                base_margin=None,
                                                iteration_range=iteration_range)
            return predictions

        X = pre_process(X, mask=mask, rem_membrane=rem_membrane)

        X_features = generate_feature_stack(X, self.features)

        X_predict = to_np(X_features)

        predictions = super().predict_proba(X_predict,
                                            ntree_limit=None,
                                            validate_features=validate_features,
                                            base_margin=None,
                                            iteration_range=iteration_range)
        n_classes = predictions.shape[1]
        flattened_prob = []
        for i in range(n_classes):
            flattened_prob.append(predictions[:, i].reshape(X.shape))
        flattened_prob = np.array(flattened_prob)
        return flattened_prob
