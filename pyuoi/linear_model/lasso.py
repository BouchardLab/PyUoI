import numpy as np

from sklearn.linear_model import Lasso, LinearRegression
from sklearn.linear_model.coordinate_descent import _alpha_grid

from .base import AbstractUoILinearRegressor


class UoI_Lasso(AbstractUoILinearRegressor, LinearRegression):

    def __init__(self, n_boots_sel=48, n_boots_est=48, selection_frac=0.9,
                 estimation_frac=0.9, n_lambdas=48, stability_selection=1.,
                 eps=1e-3, warm_start=True, estimation_score='r2',
                 copy_X=True, fit_intercept=True, standardize=True,
                 random_state=None, max_iter=1000,
                 comm=None):
        super(UoI_Lasso, self).__init__(
            n_boots_sel=n_boots_sel,
            n_boots_est=n_boots_est,
            selection_frac=selection_frac,
            estimation_frac=estimation_frac,
            stability_selection=stability_selection,
            copy_X=copy_X,
            fit_intercept=fit_intercept,
            standardize=standardize,
            random_state=random_state,
            comm=comm,
            estimation_score=estimation_score,
            max_iter=max_iter
        )
        self.n_lambdas = n_lambdas
        self.eps = eps
        self.__selection_lm = Lasso(
            max_iter=max_iter,
            warm_start=warm_start,
            random_state=random_state
        )
        self.__estimation_lm = LinearRegression()

    @property
    def estimation_lm(self):
        return self.__estimation_lm

    @property
    def selection_lm(self):
        return self.__selection_lm

    def get_reg_params(self, X, y):
        alphas = _alpha_grid(
            X=X, y=y,
            l1_ratio=1.0,
            fit_intercept=self.fit_intercept,
            eps=self.eps,
            n_alphas=self.n_lambdas,
        )
        return [{'alpha': a} for a in alphas]

    def _fit_intercept(self, X, y):
        """Fit the intercept."""
        if self.fit_intercept:
            self.intercept_ = y.mean() - np.dot(X.mean(axis=0), self.coef_)
        else:
            self.intercept = np.zeros(1)
