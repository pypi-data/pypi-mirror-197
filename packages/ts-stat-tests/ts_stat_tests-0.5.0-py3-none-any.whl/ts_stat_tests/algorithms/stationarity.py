# from pmdarima.arima.stationarity import PPTest, ADFTest, KPSSTest
# from statsmodels.tsa.api import adfuller, kpss
# """
# For a really good article on ADF & KPSS tests, check: [When A Time Series Only Quacks Like A Duck: Testing for Stationarity Before Running Forecast Models. With Python. And A Duckling Picture.](https://towardsdatascience.com/when-a-time-series-only-quacks-like-a-duck-10de9e165e)
# """


# ---------------------------------------------------------------------------- #
#                                                                              #
#    Setup                                                                  ####
#                                                                              #
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
# Imports                                                                   ####
# ---------------------------------------------------------------------------- #


# Python ----
from typing import Dict, Tuple, Union

# Packages ----
from arch.unitroot import (
    DFGLS as _ers,
    VarianceRatio as _vr,
)
from pmdarima.arima import PPTest
from statsmodels.stats.diagnostic import ResultsStore
from statsmodels.tools.validation import (
    array_like,
    bool_like,
    dict_like,
    float_like,
    int_like,
    string_like,
)
from statsmodels.tsa.stattools import (
    adfuller as _adfuller,
    kpss as _kpss,
    range_unit_root_test as _rur,
    zivot_andrews as _za,
)

# Locals ----


# ---------------------------------------------------------------------------- #
# Exports                                                                   ####
# ---------------------------------------------------------------------------- #

__all__ = ["adf", "kpss", "rur", "za", "pp", "ers", "vr"]


# ---------------------------------------------------------------------------- #
#                                                                              #
#    Algorithms                                                             ####
#                                                                              #
# ---------------------------------------------------------------------------- #


def adf(
    x: array_like,
    maxlag: int_like = None,
    regression: string_like = "c",
    autolag: string_like = "AIC",
    store: bool_like = False,
    regresults: bool_like = False,
) -> Union[
    Tuple[float_like, float_like, int_like, dict_like, float_like],
    Tuple[float_like, float_like, int_like, dict_like, float_like, ResultsStore],
]:
    """
    !!! summary "Summary"
        The Augmented Dickey-Fuller test can be used to test for a unit root in a univariate process in the presence of serial correlation.

    ???+ info "Details"

        The Augmented Dickey-Fuller (ADF) test is a statistical test used to determine whether a time series is stationary or not. Stationarity refers to the property of a time series where the statistical properties, such as mean and variance, remain constant over time. Stationarity is important for time series forecasting as it allows for the use of many popular forecasting models, such as ARIMA.

        The ADF test is an extension of the Dickey-Fuller test and involves regressing the first-difference of the time series on its lagged values, and then testing whether the coefficient of the lagged first-difference term is statistically significant. If it is, then the time series is considered non-stationary.

        The null hypothesis of the ADF test is that the time series has a unit root, which means that it is non-stationary. The alternative hypothesis is that the time series is stationary. If the p-value of the test is less than a chosen significance level, typically 0.05, then we reject the null hypothesis and conclude that the time series is stationary.

        In practical terms, if a time series is found to be non-stationary by the ADF test, one can apply differencing to the time series until it becomes stationary. This involves taking the difference between consecutive observations and potentially repeating this process until the time series is stationary.

    Params:
        x (array_like):
            The data series to test.
        maxlag (int_like, optional):
            Maximum lag which is included in test, default value of $12 \\times (\\frac{nobs}{100})^{\\frac{1}{4}}$ is used when `None`.<br>
            Defaults to `None`.
        regression (string_like, optional):
            Constant and trend order to include in regression.

            - `"c"`: constant only (default).
            - `"ct"`: constant and trend.
            - `"ctt"`: constant, and linear and quadratic trend.
            - `"n"`: no constant, no trend.

            Defaults to `"c"`.
        autolag (string_like, optional):
            Method to use when automatically determining the lag length among the values $0, 1, ..., maxlag$.

            - If `"AIC"` (default) or `"BIC"`, then the number of lags is chosen to minimize the corresponding information criterion.
            - `"t-stat"` based choice of `maxlag`. Starts with `maxlag` and drops a lag until the t-statistic on the last lag length is significant using a 5%-sized test.
            - If `None`, then the number of included lags is set to `maxlag`.

            Defaults to `"AIC"`.
        store (bool_like, optional):
            If `True`, then a result instance is returned additionally to the `adf` statistic.<br>
            Defaults to `False`.
        regresults (bool_like, optional):
            If `True`, the full regression results are returned.<br>
            Defaults to `False`.

    Returns:
        adf (float):
            The test statistic.
        pvalue (float):
            MacKinnon's approximate p-value based on MacKinnon (1994, 2010).
        uselag (int):
            The number of lags used.
        nobs (int):
            The number of observations used for the ADF regression and calculation of the critical values.
        critical_values (dict):
            Critical values for the test statistic at the $1\\%$, $5\\%$, and $10\\%$ levels. Based on MacKinnon (2010).
        icbest (float):
            The maximized information criterion if `autolag` is not `None`.
        resstore (Optional[ResultStore]):
            A dummy class with results attached as attributes.

    !!! example "Examples"
        _description_
        ```python linenums="1" title="Python"
        >>> _description_
        ```

    !!! success "Credit"
        - All credit goes to the [`statsmodels`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.adfuller.html) library.

    ???+ calculation "Equation"

        The mathematical equation for the Augmented Dickey-Fuller (ADF) test for stationarity in time series forecasting is:

        $$
        Δy_t = α + βy_{t-1} + \\sum_{i=1}^p  δ_iΔy_{t-i} + ε_t
        $$

        where:

        - $y_t$ is the value of the time series at time $t$
        - $Δy_t$ is the first difference of $y_t$, which is defined as $Δy_t = y_t - y_{t-1}$
        - $α$ is the constant term
        - $β$ is the coefficient on $y_{t-1}$
        - $δ_i$ are the coefficients on the lagged differences of $y$
        - $ε_t$ is the error term

        The ADF test involves testing the null hypothesis that $β = 0$, or equivalently, that the time series has a unit root. If $β$ is significantly different from $0$, then the null hypothesis can be rejected and the time series is considered stationary.

        Here are the detailed steps for how to calculate the ADF test:

        1. Collect your time series data and plot it to visually check for any trends, seasonal patterns, or other patterns that could make the data non-stationary. If you detect any such patterns, you will need to pre-process your data (e.g., detrending, deseasonalizing, etc.) to remove these effects.

        1. Calculate the first differences of the time series, which is simply the difference between each observation and the previous observation. This step is performed to transform the original data into a stationary process. The first difference of $y_t$ is defined as $Δy_t = y_t - y_{t-1}$.

        1. Estimate the parameters $α$, $β$, and $δ_i$ using the least squares method. This involves regressing $Δy_t$ on its lagged values, $y_{t-1}$, and the lagged differences of $y, Δy_{t-1}, Δy_{t-2}, ..., Δy_{t-p}$, where $p$ is the number of lags to include in the model. The estimated equation is:

            $$
            Δy_t = α + βy_{t-1} + \\sum_{i=1}^p δ_iΔy_{t-i} + ε_t
            $$

        1. Calculate the test statistic, which is given by:

            $$
            ADF = \\frac {β-1} {SE(β)}
            $$

            - where $SE(β)$ is the standard error of the coefficient on $y_{t-1}$.

            The test statistic measures the number of standard errors by which $β$ deviates from $1$. If ADF is less than the critical values from the ADF distribution table, we can reject the null hypothesis and conclude that the time series is stationary.

        1. Compare the test statistic to the critical values in the ADF distribution table to determine the level of significance. The critical values depend on the sample size, the level of significance, and the number of lags in the model.

        1. Finally, interpret the results and draw conclusions about the stationarity of the time series. If the null hypothesis is rejected, then the time series is stationary and can be used for forecasting. If the null hypothesis is not rejected, then the time series is non-stationary and requires further pre-processing before it can be used for forecasting.

    ??? info "Notes"
        The null hypothesis of the Augmented Dickey-Fuller is that there is a unit root, with the alternative that there is no unit root. If the pvalue is above a critical size, then we cannot reject that there is a unit root.

        The p-values are obtained through regression surface approximation from MacKinnon 1994, but using the updated 2010 tables. If the p-value is close to significant, then the critical values should be used to judge whether to reject the null.

        The autolag option and maxlag for it are described in Greene.

    ??? question "References"
        - Baum, C.F. (2004). ZANDREWS: Stata module to calculate Zivot-Andrews unit root test in presence of structural break," Statistical Software Components S437301, Boston College Department of Economics, revised 2015.
        - Schwert, G.W. (1989). Tests for unit roots: A Monte Carlo investigation. Journal of Business & Economic Statistics, 7: 147-159.
        - Zivot, E., and Andrews, D.W.K. (1992). Further evidence on the great crash, the oil-price shock, and the unit-root hypothesis. Journal of Business & Economic Studies, 10: 251-270.

    ??? tip "See Also"
        - [`statsmodels.tsa.stattools.adfuller`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.adfuller.html)
        - [`statsmodels.tsa.stattools.kpss`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.kpss.html)
        - [`statsmodels.tsa.stattools.range_unit_root_test`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.range_unit_root_test.html)
        - [`statsmodels.tsa.stattools.zivot_andrews`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.zivot_andrews.html)
        - [`pmdarima.arima.PPTest`](https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.PPTest.html)
        - [`ts_stat_tests.algorithms.stationarity.adf`](#)
        - [`ts_stat_tests.algorithms.stationarity.kpss`](#)
        - [`ts_stat_tests.algorithms.stationarity.rur`](#)
        - [`ts_stat_tests.algorithms.stationarity.za`](#)
        - [`ts_stat_tests.algorithms.stationarity.pp`](#)
    """
    return _adfuller(
        x=x,
        maxlag=maxlag,
        regression=regression,
        autolag=autolag,
        store=store,
        regresults=regresults,
    )


def kpss(
    x: array_like,
    regression: string_like = "c",
    nlags: Union[string_like, int_like] = None,
    store: bool_like = False,
) -> Union[
    Tuple[float_like, float_like, int_like, dict_like],
    Tuple[float_like, float_like, int_like, dict_like, ResultsStore],
]:
    """
    !!! summary "Summary"
        Computes the Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test for the null hypothesis that `x` is level or trend stationary.

    ???+ info "Details"

        The Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test is another statistical test used to determine whether a time series is stationary or not. The KPSS test is the opposite of the Augmented Dickey-Fuller (ADF) test, which tests for the presence of a unit root in the time series.

        The KPSS test involves regressing the time series on a constant and a time trend. The null hypothesis of the test is that the time series is stationary. The alternative hypothesis is that the time series has a unit root, which means that it is non-stationary.

        The test statistic is calculated by taking the sum of the squared residuals of the regression. If the test statistic is greater than a critical value at a given significance level, typically 0.05, then we reject the null hypothesis and conclude that the time series is non-stationary. If the test statistic is less than the critical value, then we fail to reject the null hypothesis and conclude that the time series is stationary.

        In practical terms, if a time series is found to be non-stationary by the KPSS test, one can apply differencing to the time series until it becomes stationary. This involves taking the difference between consecutive observations and potentially repeating this process until the time series is stationary.

        Overall, the ADF and KPSS tests are both important tools in time series analysis and forecasting, as they help identify whether a time series is stationary or non-stationary, which can have implications for the choice of forecasting models and methods.

    Params:
        x (array_like):
            The data series to test.
        regression (string_like, optional):
            The null hypothesis for the KPSS test.

            - `"c"`: The data is stationary around a constant (default).
            - `"ct"`: The data is stationary around a trend.

            Defaults to `"c"`.
        nlags (Union[string_like, int_like], optional):
            Indicates the number of lags to be used.

            - If `"auto"` (default), `lags` is calculated using the data-dependent method of Hobijn et al. (1998). See also Andrews (1991), Newey & West (1994), and Schwert (1989).
            - If set to `"legacy"`, uses $int(12 \\times (\\frac{n}{100})^{\\frac{1}{4}})$, as outlined in Schwert (1989).

            Defaults to `None`.
        store (bool_like, optional):
            If `True`, then a result instance is returned additionally to the KPSS statistic.<br>
            Defaults to `False`.

    Returns:
        kpss_stat (float):
            The KPSS test statistic.
        p_value (float):
            The p-value of the test. The p-value is interpolated from Table 1 in Kwiatkowski et al. (1992), and a boundary point is returned if the test statistic is outside the table of critical values, that is, if the p-value is outside the interval (0.01, 0.1).
        lags (int):
            The truncation lag parameter.
        crit (dict):
            The critical values at $10\\%$, $5\\%$, $2.5\\%$ and $1\\%$. Based on Kwiatkowski et al. (1992).
        resstore (Optional[ResultStore]):
            An instance of a dummy class with results attached as attributes.

    !!! example "Examples"
        _description_
        ```python linenums="1" title="Python"
        >>> _description_
        ```

    !!! success "Credit"
        - All credit goes to the [`statsmodels`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.kpss.html) library.

    ???+ calculation "Equation"

        The mathematical equation for the KPSS test for stationarity in time series forecasting is:

        $$
        y_t = μ_t + ε_t
        $$

        where:

        - $y_t$ is the value of the time series at time $t$
        - $μ_t$ is the trend component of the time series
        - $ε_t$ is the error term

        The KPSS test involves testing the null hypothesis that the time series is trend stationary, which means that the trend component of the time series is stationary over time. If the null hypothesis is rejected, then the time series is non-stationary and requires further pre-processing before it can be used for forecasting.

        Here are the detailed steps for how to calculate the KPSS test:

        1. Collect your time series data and plot it to visually check for any trends, seasonal patterns, or other patterns that could make the data non-stationary. If you detect any such patterns, you will need to pre-process your data (e.g., detrending, deseasonalizing, etc.) to remove these effects.

        1. Divide your time series data into multiple overlapping windows of equal size. The length of each window depends on the length of your time series and the level of detail you want to capture.

        1. Calculate the trend component $μ_t$ for each window using a trend estimation method. There are several methods for estimating the trend component, such as the Hodrick-Prescott filter, the Christiano-Fitzgerald filter, or simple linear regression. The choice of method depends on the characteristics of your data and the level of accuracy you want to achieve.

        1. Calculate the residual series $ε_t$ by subtracting the trend component from the original time series:

            $$
            ε_t = y_t - μ_t
            $$

        1. Estimate the variance of the residual series using a suitable estimator, such as the Newey-West estimator or the Bartlett kernel estimator. This step is necessary to correct for any serial correlation in the residual series.

        1. Calculate the test statistic, which is given by:

            $$
            KPSS = T \\times \\sum_{t=1}^T \\frac {S_t^2} {σ^2}
            $$

            where:

            - $T$ is the number of observations in the time series
            - $S_t$ is the cumulative sum of the residual series up to time $t$, i.e., $S_t = \\sum_{i=1}^t ε_i$
            - $σ^2$ is the estimated variance of the residual series

            The test statistic measures the strength of the trend component relative to the residual series. If KPSS is greater than the critical values from the KPSS distribution table, we can reject the null hypothesis and conclude that the time series is non-stationary.

        1. Finally, interpret the results and draw conclusions about the stationarity of the time series. If the null hypothesis is rejected, then the time series is non-stationary and requires further pre-processing before it can be used for forecasting. If the null hypothesis is not rejected, then the time series is trend stationary and can be used for forecasting.

    ??? info "Notes"
        To estimate $sigma^2$ the Newey-West estimator is used. If `lags` is `"legacy"`, the truncation lag parameter is set to $int(12 \\times (\\frac{n}{100})^{\\frac{1}{4}})$, as outlined in Schwert (1989). The p-values are interpolated from Table 1 of Kwiatkowski et al. (1992). If the computed statistic is outside the table of critical values, then a warning message is generated.

        Missing values are not handled.

    ??? question "References"
        - Andrews, D.W.K. (1991). Heteroskedasticity and autocorrelation consistent covariance matrix estimation. Econometrica, 59: 817-858.
        - Hobijn, B., Frances, B.H., & Ooms, M. (2004). Generalizations of the KPSS-test for stationarity. Statistica Neerlandica, 52: 483-502.
        - Kwiatkowski, D., Phillips, P.C.B., Schmidt, P., & Shin, Y. (1992). Testing the null hypothesis of stationarity against the alternative of a unit root. Journal of Econometrics, 54: 159-178.
        - Newey, W.K., & West, K.D. (1994). Automatic lag selection in covariance matrix estimation. Review of Economic Studies, 61: 631-653.
        - Schwert, G. W. (1989). Tests for unit roots: A Monte Carlo investigation. Journal of Business and Economic Statistics, 7 (2): 147-159.

    ??? tip "See Also"
        - _description_
    """
    return _kpss(
        x=x,
        regression=regression,
        nlags=nlags,
        store=store,
    )


def rur(
    x: array_like,
    store: bool_like = False,
) -> Union[
    Tuple[float_like, float_like, dict_like],
    Tuple[float_like, float_like, dict_like, ResultsStore],
]:
    r"""
    !!! summary "Summary"
        Computes the Range Unit-Root (RUR) test for the null hypothesis that x is stationary.

    ???+ info "Details"

        The Range Unit-Root (RUR) test is a statistical test used to determine whether a time series is stationary or not. It is based on the range of the time series and does not require any knowledge of the underlying stochastic process.

        The RUR test involves dividing the time series into non-overlapping windows of a fixed size and calculating the range of each window. Then, the range of the entire time series is calculated. If the time series is stationary, the range of the entire time series should be proportional to the square root of the window size. If the time series is non-stationary, the range of the entire time series will grow with the window size.

        The null hypothesis of the RUR test is that the time series is stationary. The alternative hypothesis is that the time series is non-stationary. If the test statistic, which is the ratio of the range of the entire time series to the square root of the window size, is greater than a critical value at a given significance level, typically 0.05, then we reject the null hypothesis and conclude that the time series is non-stationary. If the test statistic is less than the critical value, then we fail to reject the null hypothesis and conclude that the time series is stationary.

        In practical terms, if a time series is found to be non-stationary by the RUR test, one can apply differencing to the time series until it becomes stationary. This involves taking the difference between consecutive observations and potentially repeating this process until the time series is stationary.

        The RUR test is a simple and computationally efficient test for stationarity, but it may not be as powerful as other unit root tests in detecting non-stationarity in some cases. It is important to use multiple tests to determine the stationarity of a time series, as no single test is perfect in all situations.

    Params:
        x (array_like):
            The data series to test.
        store (bool_like, optional):
            If `True`, then a result instance is returned additionally to the RUR statistic.<br>
            Defaults to `False`.

    Returns:
        rur_stat (float):
            The RUR test statistic.
        p_value (float):
            The p-value of the test. The p-value is interpolated from Table 1 in Aparicio et al. (2006), and a boundary point is returned if the test statistic is outside the table of critical values, that is, if the p-value is outside the interval (0.01, 0.1).
        crit (dict):
            The critical values at $10\%$, $5\%$, $2.5\%$ and $1\%$. Based on Aparicio et al. (2006).
        resstore (Optional[ResultStore]):
            An instance of a dummy class with results attached as attributes.

    !!! example "Examples"
        _description_
        ```python linenums="1" title="Python"
        >>> _description_
        ```

    !!! success "Credit"
        - All credit goes to the [`statsmodels`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.range_unit_root_test.html) library.

    ???+ calculation "Equation"

        The mathematical equation for the RUR test is:

        $$
        y_t = ρ y_{t-1} + ε_t
        $$

        where:

        - $y_t$ is the value of the time series at time $t$
        - $ρ$ is the parameter of the unit root process
        - $y_{t-1}$ is the value of the time series at time $t-1$
        - $ε_t$ is a stationary error term with mean zero and constant variance

        The null hypothesis of the RUR test is that the time series is stationary, and the alternative hypothesis is that the time series is non-stationary with a unit root.

        Here are the detailed steps for how to calculate the RUR test:

        1. Collect your time series data and plot it to visually check for any trends, seasonal patterns, or other patterns that could make the data non-stationary. If you detect any such patterns, you will need to pre-process your data (e.g., detrending, deseasonalizing, etc.) to remove these effects.

        1. Estimate the parameter $ρ$ using the ordinary least squares method. This involves regressing $y_t$ on $y_{t-1}$. The estimated equation is:

            $$
            y_t = α + ρ y_{t-1} + ε_t
            $$

            where:

            - $α$ is the intercept, and
            - $ε_t$ is the error term

        1. Calculate the range of the time series, which is the difference between the maximum and minimum values of the time series:

            $$
            R = max(y_t) - min(y_t)
            $$

        1. Calculate the expected range of the time series under the null hypothesis of stationarity, which is given by:

            $$
            E(R) = (T - 1) / (2 √(T))
            $$

            where:

            - $T$ is the sample size

        1. Calculate the test statistic, which is given by:

            $$
            RUR = (R - E(R)) / E(R)
            $$

        1. Compare the test statistic to the critical values in the RUR distribution table to determine the level of significance. The critical values depend on the sample size and the level of significance.

        1. Finally, interpret the results and draw conclusions about the stationarity of the time series. If the null hypothesis is rejected, then the time series is non-stationary with a unit root. If the null hypothesis is not rejected, then the time series is stationary.

        In practice, the RUR test is often conducted using software packages such as R, Python, or MATLAB, which automate the estimation of parameters and calculation of the test statistic.

    ??? info "Notes"
        The p-values are interpolated from Table 1 of Aparicio et al. (2006). If the computed statistic is outside the table of critical values, then a warning message is generated.

        Missing values are not handled.

    ??? question "References"
        - Aparicio, F., Escribano A., Sipols, A.E. (2006). Range Unit-Root (RUR) tests: robust against nonlinearities, error distributions, structural breaks and outliers. Journal of Time Series Analysis, 27 (4): 545-576.

    ??? tip "See Also"
        - _description_
    """
    return _rur(
        x=x,
        store=store,
    )


def za(
    x: array_like,
    trim: float_like = 0.15,
    maxlag: int_like = None,
    regression: string_like = "c",
    autolag: string_like = "AIC",
) -> Tuple[float_like, float_like, dict_like, int_like, int_like]:
    """
    !!! summary "Summary"
        The Zivot-Andrews (ZA) test tests for a unit root in a univariate process in the presence of serial correlation and a single structural break.

    ???+ info "Details"
        The Zivot-Andrews (ZA) test is a statistical test used to determine whether a time series is stationary or not in the presence of structural breaks. Structural breaks refer to significant changes in the underlying stochastic process of the time series, which can cause non-stationarity.

        The ZA test involves running a regression of the time series on a constant and a linear time trend, and testing whether the residuals of the regression are stationary or not. The null hypothesis of the test is that the time series is stationary with a single break point, while the alternative hypothesis is that the time series is non-stationary with a single break point.

        The test statistic is calculated by first estimating the break point using a likelihood ratio test. Then, the test statistic is calculated based on the estimated break point and the residuals of the regression. If the test statistic is greater than a critical value at a given significance level, typically 0.05, then we reject the null hypothesis and conclude that the time series is non-stationary with a structural break. If the test statistic is less than the critical value, then we fail to reject the null hypothesis and conclude that the time series is stationary with a structural break.

        In practical terms, if a time series is found to be non-stationary with a structural break by the ZA test, one can apply methods to account for the structural break, such as including dummy variables in the regression or using time series models that allow for structural breaks.

        Overall, the ZA test is a useful tool in time series analysis and forecasting when there is a suspicion of structural breaks in the data. However, it is important to note that the test may not detect multiple break points or breaks that are not well-separated in time.

    Params:
        x (array_like):
            The data series to test.
        trim (float_like, optional):
            The percentage of series at begin/end to exclude from break-period calculation in range [0, 0.333].<br>
            Defaults to `0.15`.
        maxlag (int_like, optional):
            The maximum lag which is included in test, default is $12 \\times (\\frac{nobs}{100})^{\\frac{1}{4}} (Schwert, 1989).<br>
            Defaults to `None`.
        regression (string_like, optional):
            Constant and trend order to include in regression.

            - `"c"`: constant only (default).
            - `"t"`: trend only.
            - `"ct"`: constant and trend.

            Defaults to `"c"`.
        autolag (string_like, optional):
            The method to select the lag length when using automatic selection.

            - If `None`, then `maxlag` lags are used,
            - If `"AIC"` (default) or `"BIC"`, then the number of lags is chosen to minimize the corresponding information criterion,
            - `"t-stat"` based choice of `maxlag`. Starts with maxlag and drops a lag until the t-statistic on the last lag length is significant using a 5%-sized test.

            Defaults to `"AIC"`.

    Returns:
        zastat (float):
            The test statistic.
        pvalue (float):
            The pvalue based on MC-derived critical values.
        cvdict (dict):
            The critical values for the test statistic at the $1/%$, $5/%$, and $10/%$ levels.
        baselag (int):
            The number of lags used for period regressions.
        pbidx (int):
            The index of `x` corresponding to endogenously calculated break period with values in the range $[0..nobs-1]$.

    !!! example "Examples"
        _description_
        ```python linenums="1" title="Python"
        >>> _description_
        ```

    !!! success "Credit"
        - All credit goes to the [`statsmodels`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.zivot_andrews.html) library.

    ???+ calculation "Equation"

        The mathematical equation for the Zivot-Andrews test is:

        $$
        y_t = α + β t + γ y_{t-1} + δ_1 D_t + δ_2 t D_t + ε_t
        $$

        where:

        - $y_t$ is the value of the time series at time $t$
        - $α$ is the intercept
        - $β$ is the slope coefficient of the time trend
        - $γ$ is the coefficient of the lagged dependent variable
        - $D_t$ is a dummy variable that takes a value of $1$ after the suspected structural break point, and $0$ otherwise
        - $δ_1$ and $δ_2$ are the coefficients of the dummy variable and the interaction term of the dummy variable and time trend, respectively
        - $ε_t$ is a stationary error term with mean zero and constant variance

        The null hypothesis of the Zivot-Andrews test is that the time series is non-stationary, and the alternative hypothesis is that the time series is stationary with a single structural break.

        Here are the detailed steps for how to calculate the Zivot-Andrews test:

        1. Collect your time series data and plot it to visually check for any trends, seasonal patterns, or other patterns that could make the data non-stationary. If you detect any such patterns, you will need to pre-process your data (e.g., detrending, deseasonalizing, etc.) to remove these effects.

        1. Estimate the parameters of the model using the least squares method. This involves regressing $y_t$ on $t$, $y_{t-1}$, $D_t$, and $t D_t$. The estimated equation is:

            $$
            y_t = α + β t + γ y_{t-1} + δ_1 D_t + δ_2 t D_t + ε_t
            $$

        1. Perform a unit root test on the residuals to check for stationarity. The most commonly used unit root tests for this purpose are the Augmented Dickey-Fuller (ADF) test and the Phillips-Perron (PP) test.

        1. Calculate the test statistic, which is based on the largest root of the following equation:

            $$
            ∆y_t = α + β t + γ y_{t-1} + δ_1 D_t + δ_2 t D_t + ε_t
            $$

            where:

            - $∆$ is the first difference operator.

        1. Determine the critical values of the test statistic from the Zivot-Andrews distribution table. The critical values depend on the sample size, the level of significance, and the number of lagged dependent variables in the model.

        1. Finally, interpret the results and draw conclusions about the stationarity of the time series. If the null hypothesis is rejected, then the time series is stationary with a structural break. If the null hypothesis is not rejected, then the time series is non-stationary and may require further processing to make it stationary.

        In practice, the Zivot-Andrews test is often conducted using software packages such as R, Python, or MATLAB, which automate the estimation of parameters and calculation of the test statistic.

    ??? info "Notes"
        H0 = unit root with a single structural break

        Algorithm follows Baum (2004/2015) approximation to original Zivot-Andrews method. Rather than performing an autolag regression at each candidate break period (as per the original paper), a single autolag regression is run up-front on the base model (constant + trend with no dummies) to determine the best lag length. This lag length is then used for all subsequent break-period regressions. This results in significant run time reduction but also slightly more pessimistic test statistics than the original Zivot-Andrews method, although no attempt has been made to characterize the size/power trade-off.

    ??? question "References"
        - Baum, C.F. (2004). ZANDREWS: Stata module to calculate Zivot-Andrews unit root test in presence of structural break," Statistical Software Components S437301, Boston College Department of Economics, revised 2015.
        - Schwert, G.W. (1989). Tests for unit roots: A Monte Carlo investigation. Journal of Business & Economic Statistics, 7: 147-159.
        - Zivot, E., and Andrews, D.W.K. (1992). Further evidence on the great crash, the oil-price shock, and the unit-root hypothesis. Journal of Business & Economic Studies, 10: 251-270.

    ??? tip "See Also"
        - _description_
    """
    return _za(
        x=x,
        trim=trim,
        maxlag=maxlag,
        regression=regression,
        autolag=autolag,
    )


def pp(
    x: array_like,
    alpha: float_like = 0.05,
    lshort: bool_like = True,
) -> Tuple[float_like, bool_like]:
    """
    !!! summary "Summary"
        Conduct a Phillips-Perron (PP) test for stationarity.

        In statistics, the Phillips-Perron test (named after Peter C. B. Phillips and Pierre Perron) is a unit root test. It is used in time series analysis to test the null hypothesis that a time series is integrated of order $1$. It builds on the Dickey-Fuller test of the null hypothesis $p=0$.

    ???+ info "Details"

        The Phillips-Perron (PP) test is a statistical test used to determine whether a time series is stationary or not. It is similar to the Augmented Dickey-Fuller (ADF) test, but it has some advantages, especially in the presence of autocorrelation and heteroscedasticity.

        The PP test involves regressing the time series on a constant and a linear time trend, and testing whether the residuals of the regression are stationary or not. The null hypothesis of the test is that the time series is non-stationary, while the alternative hypothesis is that the time series is stationary.

        The test statistic is calculated by taking the sum of the squared residuals of the regression, which is adjusted for autocorrelation and heteroscedasticity. The PP test also accounts for the bias in the standard errors of the test statistic, which can lead to incorrect inference in small samples.

        If the test statistic is less than a critical value at a given significance level, typically 0.05, then we reject the null hypothesis and conclude that the time series is stationary. If the test statistic is greater than the critical value, then we fail to reject the null hypothesis and conclude that the time series is non-stationary.

        In practical terms, if a time series is found to be non-stationary by the PP test, one can apply differencing to the time series until it becomes stationary. This involves taking the difference between consecutive observations and potentially repeating this process until the time series is stationary.

        Overall, the PP test is a powerful and robust test for stationarity, and it is widely used in time series analysis and forecasting. However, it is important to use multiple tests and diagnostic tools to determine the stationarity of a time series, as no single test is perfect in all situations.

    Params:
        x (array_like):
            The time series vector.
        alpha (float_like, optional):
            Level of the test.<br>
            Defaults to `0.05`.
        lshort (bool_like, optional):
            Whether or not to truncate the `l` value in the C code.<br>
            Defaults to `True`.

    Returns:
        pval (float):
            The computed P-value of the test.
        sig (bool):
            Whether the P-value is significant at the alpha level. More directly, whether to difference the time series.

    !!! example "Examples"
        _description_
        ```python linenums="1" title="Python"
        >>> _description_
        ```

    !!! success "Credit"
        - All credit goes to the [`pmdarima`](https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.PPTest.html) library.

    ???+ calculation "Equation"

        The Phillips-Perron (PP) test is a commonly used test for stationarity in time series forecasting. The mathematical equation for the PP test is:

        $$
        y_t = δ + πt + ρy_{t-1} + ε_t
        $$

        where:

        - $y_t$ is the value of the time series at time $t$
        - $δ$ is a constant term
        - $π$ is a coefficient that captures the trend in the data
        - $ρ$ is a coefficient that captures the autocorrelation in the data
        - $y_{t-1}$ is the lagged value of the time series at time $t-1$
        - $ε_t$ is a stationary error term with mean zero and constant variance

        The PP test is based on the idea that if the time series is stationary, then the coefficient $ρ$ should be equal to zero. Therefore, the null hypothesis of the PP test is that the time series is stationary, and the alternative hypothesis is that the time series is non-stationary with a non-zero value of $ρ$.

        Here are the detailed steps for how to calculate the PP test:

        1. Collect your time series data and plot it to visually check for any trends, seasonal patterns, or other patterns that could make the data non-stationary. If you detect any such patterns, you will need to pre-process your data (e.g., detrending, deseasonalizing, etc.) to remove these effects.

        1. Estimate the regression model by regressing y_t on a constant, a linear trend, and the lagged value of $y_{t-1}$. The regression equation is:

            $$
            y_t = δ + πt + ρy_{t-1} + ε_t
            $$

        1. Calculate the test statistic, which is based on the following equation:

            $$
            z = \\left( T^{-\\frac{1}{2}} \\right) \\times \\left( \\sum_{t=1}^T \\left( y_t - δ - πt - ρy_{t-1} \\right) - \\left( \\frac{1}{T} \\right) \\times \\sum_{t=1}^T \\sum_{s=1}^T K \\left( \\frac{s-t}{h} \\right) (y_s - δ - πs - ρy_{s-1}) \\right)
            $$

            where:

            - $T$ is the sample size
            - $K()$ is the kernel function, which determines the weight of each observation in the smoothed series. The choice of the kernel function depends on the degree of serial correlation in the data. Typically, a Gaussian kernel or a Bartlett kernel is used.
            - $h$ is the bandwidth parameter, which controls the degree of smoothing of the series. The optimal value of $h$ depends on the sample size and the noise level of the data.

        1. Determine the critical values of the test statistic from the PP distribution table. The critical values depend on the sample size and the level of significance.

        1. Finally, interpret the results and draw conclusions about the stationarity of the time series. If the null hypothesis is rejected, then the time series is non-stationary with a non-zero value of $ρ$. If the null hypothesis is not rejected, then the time series is stationary.

        In practice, the PP test is often conducted using software packages such as R, Python, or MATLAB, which automate the estimation of the regression model and calculation of the test statistic.

    ??? info "Notes"
        This test is generally used indirectly via the [`pmdarima.arima.ndiffs()`](https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.ndiffs.html) function, which computes the differencing term, `d`.

        The R code allows for two types of tests: `'Z(alpha)'` and `'Z(t_alpha)'`. Since sklearn does not allow extraction of std errors from the linear model fit, `t_alpha` is much more difficult to achieve, so we do not allow that variant.

    ??? question "References"
        - R's tseries PP test source code: http://bit.ly/2wbzx6V

    ??? tip "See Also"
        - _description_
    """
    return PPTest(alpha=alpha, lshort=lshort).is_stationary(x=x)


def ers(
    y: array_like,
    lags: int_like = None,
    trend: string_like = "c",
    max_lags: int_like = None,
    method: string_like = "aic",
    low_memory: bool_like = None,
) -> Tuple[float, float]:
    """
    !!! summary "Summary"
        Elliott, Rothenberg and Stock's GLS detrended Dickey-Fuller.

    ???+ info "Details"

        The Elliott-Rothenberg-Stock (ERS) test is a statistical test used to determine whether a time series is stationary or not. It is a robust test that is able to handle a wide range of non-stationary processes, including ones with structural breaks, heteroscedasticity, and autocorrelation.

        The ERS test involves fitting a local-to-zero regression of the time series on a constant and a linear time trend, using a kernel function to weight the observations. The test statistic is then calculated based on the sum of the squared residuals of the local-to-zero regression, which is adjusted for the bandwidth of the kernel function and for the correlation of the residuals.

        If the test statistic is less than a critical value at a given significance level, typically 0.05, then we reject the null hypothesis and conclude that the time series is stationary. If the test statistic is greater than the critical value, then we fail to reject the null hypothesis and conclude that the time series is non-stationary.

        In practical terms, if a time series is found to be non-stationary by the ERS test, one can apply differencing to the time series until it becomes stationary. This involves taking the difference between consecutive observations and potentially repeating this process until the time series is stationary.

        Overall, the ERS test is a powerful and flexible test for stationarity, and it is widely used in time series analysis and forecasting. However, it is important to use multiple tests and diagnostic tools to determine the stationarity of a time series, as no single test is perfect in all situations.

    Params:
        y (array_like):
            The data to test for a unit root.
        lags (int_like, optional):
            The number of lags to use in the ADF regression. If omitted or `None`, method is used to automatically select the lag length with no more than `max_lags` are included.<br>
            Defaults to `None`.
        trend (string_like, optional):
            The trend component to include in the test

            - `"c"`: Include a constant (Default)
            - `"ct"`: Include a constant and linear time trend

            Defaults to `"c"`.
        max_lags (int_like, optional):
            The maximum number of lags to use when selecting lag length. When using automatic lag length selection, the lag is selected using OLS detrending rather than GLS detrending.<br>
            Defaults to `None`.
        method (string_like, optional):
            The method to use when selecting the lag length

            - `"AIC"`: Select the minimum of the Akaike IC
            - `"BIC"`: Select the minimum of the Schwarz/Bayesian IC
            - `"t-stat"`: Select the minimum of the Schwarz/Bayesian IC

            Defaults to `"aic"`.
        low_memory (bool_like, optional):
            Flag indicating whether to use the low-memory algorithm for lag-length selection.
            Defaults to `None`.

    Returns:
        pvalue (float):
            The p-value for the test statistic.
        stat (float):
            The test statistic for a unit root.

    !!! example "Examples"
        _description_
        ```python linenums="1" title="Python"
        >>> _description_
        ```

    !!! success "Credit"
        - All credit goes to the [`arch`](https://arch.readthedocs.io/en/latest/unitroot/generated/arch.unitroot.DFGLS.html) library.

    ???+ calculation "Equation"

        The mathematical equation for the ERS test is:

        $$
        y_t = μ_t + ε_t
        $$

        where:

        - $y_t$ is the value of the time series at time $t$
        - $μ_t$ is a time-varying mean function
        - $ε_t$ is a stationary error term with mean zero and constant variance

        The ERS test is based on the idea that if the time series is stationary, then the mean function should be a constant over time. Therefore, the null hypothesis of the ERS test is that the time series is stationary, and the alternative hypothesis is that the time series is non-stationary with a time-varying mean function.

        Here are the detailed steps for how to calculate the ERS test:

        1. Collect your time series data and plot it to visually check for any trends, seasonal patterns, or other patterns that could make the data non-stationary. If you detect any such patterns, you will need to pre-process your data (e.g., detrending, deseasonalizing, etc.) to remove these effects.

        1. Estimate the time-varying mean function using a local polynomial regression method. The choice of the polynomial degree depends on the complexity of the mean function and the sample size. Typically, a quadratic or cubic polynomial is used. The estimated mean function is denoted as $μ_t$.

        1. Calculate the test statistic, which is based on the following equation:

            $$
            z = \\left( \\frac {T-1} {( \\frac {1} {12π^2 \\times Δ^2} )} \\right) ^{\\frac{1}{2}} \\times \\left( \\sum_{t=1}^T \\frac {(y_t - μ_t)^2} {T-1} \\right)
            $$

            where:

            - $T$ is the sample size
            - $Δ$ is the bandwidth parameter, which controls the degree of smoothing of the mean function. The optimal value of $Δ$ depends on the sample size and the noise level of the data.
            - $π$ is the constant pi

        1. Determine the critical values of the test statistic from the ERS distribution table. The critical values depend on the sample size and the level of significance.

        1. Finally, interpret the results and draw conclusions about the stationarity of the time series. If the null hypothesis is rejected, then the time series is non-stationary with a time-varying mean function. If the null hypothesis is not rejected, then the time series is stationary.

        In practice, the ERS test is often conducted using software packages such as R, Python, or MATLAB, which automate the estimation of the time-varying mean function and calculation of the test statistic.

    ??? info "Notes"
        The null hypothesis of the Dickey-Fuller GLS is that there is a unit root, with the alternative that there is no unit root. If the pvalue is above a critical size, then the null cannot be rejected and the series appears to be a unit root.

        DFGLS differs from the ADF test in that an initial GLS detrending step is used before a trend-less ADF regression is run.

        Critical values and p-values when trend is "c" are identical to the ADF. When trend is set to "ct", they are from …

    ??? question "References"
        - Elliott, G. R., T. J. Rothenberg, and J. H. Stock. 1996. Efficient bootstrap for an autoregressive unit root. Econometrica 64: 813-836.
        - Perron, P., & Qu, Z. (2007). A simple modification to improve the finite sample properties of Ng and Perron’s unit root tests. Economics letters, 94(1), 12-19.

    ??? tip "See Also"
        - _description_
    """
    ers = _ers(
        y=y,
        lags=lags,
        trend=trend,
        max_lags=max_lags,
        method=method,
        low_memory=low_memory,
    )
    return ers.pvalue, ers.stat


def vr(
    y: array_like,
    lags: int_like = 2,
    trend: string_like = "c",
    debiased: bool_like = True,
    robust: bool_like = True,
    overlap: bool_like = True,
) -> Tuple[float, float, float]:
    """
    !!! summary "Summary"
        Variance Ratio test of a random walk.

    ???+ info "Details"

        The Variance Ratio (VR) test is a statistical test used to determine whether a time series is stationary or not based on the presence of long-term dependence in the series. It is a non-parametric test that can be used to test for the presence of a unit root or a trend in the series.

        The VR test involves calculating the ratio of the variance of the differences of the logarithms of the time series over different time intervals. The variance of the differences of the logarithms is a measure of the volatility of the series, and the ratio of the variances over different intervals is a measure of the long-term dependence in the series.

        If the series is stationary, then the variance ratio will be close to one for all intervals. If the series is non-stationary, then the variance ratio will tend to increase as the length of the interval increases, reflecting the presence of long-term dependence in the series.

        The VR test involves comparing the observed variance ratio to the distribution of variance ratios expected under the null hypothesis of stationarity. If the observed variance ratio is greater than the critical value at a given significance level, typically 0.05, then we reject the null hypothesis and conclude that the time series is non-stationary. If the observed variance ratio is less than the critical value, then we fail to reject the null hypothesis and conclude that the time series is stationary.

        In practical terms, if a time series is found to be non-stationary by the VR test, one can apply differencing to the time series until it becomes stationary. This involves taking the difference between consecutive observations and potentially repeating this process until the time series is stationary.

        Overall, the VR test is a useful and relatively simple test for stationarity that can be applied to a wide range of time series. However, it is important to use multiple tests and diagnostic tools to confirm the stationarity of a time series, as no single test is perfect in all situations.

    Params:
        y (array_like):
            The data to test for a random walk.
        lags (int_like, optional):
            The number of periods to used in the multi-period variance, which is the numerator of the test statistic. Must be at least 2.<br>
            Defaults to `2`.
        trend (string_like, optional):
            `"c"` allows for a non-zero drift in the random walk, while `"n"` requires that the increments to `y` are mean `0`.<br>
            Defaults to `"c"`.
        debiased (bool_like, optional):
            Indicates whether to use a debiased version of the test. Only applicable if `overlap` is `True`.<br>
            Defaults to `True`.
        robust (bool_like, optional):
            Indicates whether to use heteroskedasticity robust inference.<br>
            Defaults to `True`.
        overlap (bool_like, optional):
            Indicates whether to use all overlapping blocks. If `False`, the number of observations in $y-1$ must be an exact multiple of `lags`. If this condition is not satisfied, some values at the end of `y` will be discarded.<br>
            Defaults to `True`.

    Returns:
        pvalue (float):
            The p-value for the test statistic.
        stat (float):
            The test statistic for a unit root.
        vr (float):
            The ratio of the long block lags-period variance.

    !!! example "Examples"
        _description_
        ```python linenums="1" title="Python"
        >>> _description_
        ```

    !!! success "Credit"
        - All credit goes to the [`arch`](https://arch.readthedocs.io/en/latest/unitroot/generated/arch.unitroot.VarianceRatio.html) library.

    ???+ calculation "Equation"

        The Variance Ratio (VR) test is a statistical test for stationarity in time series forecasting that is based on the idea that if the time series is stationary, then the variance of the returns should be constant over time. The mathematical equation for the VR test is:

        $$
        VR(k) = \\frac {σ^2(k)} {kσ^2(1)}
        $$

        where:

        - $VR(k)$ is the variance ratio for the time series over $k$ periods
        - $σ^2(k)$ is the variance of the returns over $k$ periods
        - $σ^2(1)$ is the variance of the returns over $1$ period

        The VR test involves comparing the variance ratio to a critical value, which is derived from the null distribution of the variance ratio under the assumption of a random walk with drift.

        Here are the detailed steps for how to calculate the VR test:

        1. Collect your time series data and compute the log returns, which are defined as:

            $$
            r_t = log(y_t) - log(y_{t-1})
            $$

            where:

            - $y_t$ is the value of the time series at time $t$.

        1. Compute the variance of the returns over $k$ periods, which is defined as:

            $$
            σ^2(k) = \\left( \\frac {1} {n-k} \\right) \\times \\sum_{t=k+1}^n (r_t - μ_k)^2
            $$

            where:

            - $n$ is the sample size
            - $μ_k$ is the mean of the returns over k periods, which is defined as:

                $μ_k = \\left( \\frac{1} {n-k} \\right) \\times \\sum_{t=k+1}^n r_t$

        1. Compute the variance of the returns over 1 period, which is defined as:

            $$
            σ^2(1) = \\left( \\frac{1} {n-1} \\right) \\times \\sum_{t=2}^n (r_t - μ_1)^2
            $$

            where

            - $μ_1$ is the mean of the returns over $1$ period, which is defined as:

                $μ_1 = \\left( \\frac{1} {n-1} \\right) \\times \\sum_{t=2}^n r_t$

        1. Compute the variance ratio for each value of $k$, which is defined as:

            $$
            VR(k) = \\frac {σ^2(k)} {kσ^2(1)}
            $$

        1. Determine the critical values of the variance ratio from the null distribution table of the VR test, which depend on the sample size, the level of significance, and the lag length $k$.

        1. Finally, compare the variance ratio to the critical value. If the variance ratio is greater than the critical value, then the null hypothesis of a random walk with drift is rejected, and the time series is considered stationary. If the variance ratio is less than or equal to the critical value, then the null hypothesis cannot be rejected, and the time series is considered non-stationary.

        In practice, the VR test is often conducted using software packages such as R, Python, or MATLAB, which automate the calculation of the variance ratio and the determination of the critical value.

    ???+ info "Details"
        The null hypothesis of a VR is that the process is a random walk, possibly plus drift. Rejection of the null with a positive test statistic indicates the presence of positive serial correlation in the time series.

    ??? question "References"
        - Campbell, John Y., Lo, Andrew W. and MacKinlay, A. Craig. (1997) The Econometrics of Financial Markets. Princeton, NJ: Princeton University Press.

    ??? tip "See Also"
        - _description_
    """
    vr = _vr(
        y=y,
        lags=lags,
        trend=trend,
        debiased=debiased,
        robust=robust,
        overlap=overlap,
    )
    return vr.pvalue, vr.stat, vr.vr
