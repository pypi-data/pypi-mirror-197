"""
This module contains Python wrapper for PAL accuracy measure algorithm.

The following function is available:

    * :func:`accuracy_measure`
"""

#pylint: disable=too-many-lines, line-too-long, relative-beyond-top-level
import logging
import uuid
try:
    import pyodbc
except ImportError as error:
    pass
from hdbcli import dbapi
from ..pal_base import (
    ParameterTable,
    arg,
    try_drop,
    ListOfStrings,
    require_pal_usable,
    call_pal_auto_with_hint
)
#pylint: disable=invalid-name
logger = logging.getLogger(__name__)

def accuracy_measure(data, evaluation_metric):
    """
    Measures are used to check the accuracy of the forecast made by PAL algorithms.

    Parameters
    ----------

    data : DataFrame

        Input data, should have two or three columns:

        - If ``data`` contains 2 columns, then the first column is of actual data while the second one
          is of forecasted data.
        - If ``data`` contains 3 columns, then the 1st column must be the ID column, 2nd column be
          the actual data, while the 3rd column be the forecasted data.

    evaluation_metric : str of ListOfStrings
        Specifies the accuracy measure name(s), with valid options listed as follows:

        - 'mpe': mean percentage error
        - 'mse': mean square error
        - 'rmse': root mean square error
        - 'et': error total
        - 'mad': mean absolute deviation
        - 'mase': out-of-sample mean absolute scaled error
        - 'wmape': weighted mean absolute percentage error
        - 'smape': symmetric mean absolute percentage error
        - 'mape': mean absolute percentage error
        - 'spec': stock-keeping-oriented prediction error costs

        .. note::

          If ``evaluation_metric`` is specified as 'spec' or contains 'spec' as one of its element, then
          ``data`` must have 3 columns(i.e. contain an ID column).

    Returns
    -------
    DataFrame
        Result of the forecast accuracy measurement, structured as follows:

        - STAT_NAME: Name of accuracy measures.
        - STAT_VALUE: Value of accuracy measures.

    Examples
    --------
    Data for accuracy measurement:

    >>> df.collect()
        ACTUAL  FORECAST
    0   1130.0    1270.0
    1   2410.0    2340.0
    2   2210.0    2310.0
    3   2500.0    2340.0
    4   2432.0    2348.0
    5   1980.0    1890.0
    6   2045.0    2100.0
    7   2340.0    2231.0
    8   2460.0    2401.0
    9   2350.0    2310.0
    10  2345.0    2340.0
    11  2650.0    2560.0

    Perform accuracy measurement on the input dataframe:

    >>> res = accuracy_measure(data=df,
                               evaluation_metric=['mse', 'rmse', 'mpe', 'et',
                                                  'mad', 'mase', 'wmape', 'smape',
                                                  'mape'])
    >>> res.collect()
      STAT_NAME   STAT_VALUE
    0        ET   412.000000
    1       MAD    83.500000
    2      MAPE     0.041063
    3      MASE     0.287931
    4       MPE     0.008390
    5       MSE  8614.000000
    6      RMSE    92.811637
    7     SMAPE     0.040876
    8     WMAPE     0.037316

    """
    conn = data.connection_context
    require_pal_usable(conn)
    metric_map = {'mpe': 'MPE', 'mse': 'MSE', 'rmse': 'RMSE',
                  'et': 'ET', 'mad': 'MAD', 'mase': 'MASE',
                  'wmape': 'WMAPE', 'smape': 'SMAPE', 'mape': 'MAPE',
                  'spec': 'SPEC'}
    if isinstance(evaluation_metric, str):
        evaluation_metric = [evaluation_metric]
    try:
        evaluation_metric = arg('evaluation_metric', evaluation_metric, ListOfStrings)
    except Exception as err:
        msg = ("`evaluation_metric` must be list of string or string.")
        logger.error(msg)
        raise TypeError(msg) from err
    if not all(m in metric_map for m in evaluation_metric):
        msg = ("Some input in `evaluation_metric` is invalid.")
        logger.error(msg)
        raise ValueError(msg)
    if 'spec' in evaluation_metric and len(data.columns) == 2:
        msg = 'If \'spec\' is specified in evaluation_metric, then ' +\
        'the input data must have 3 columns.'
        logger.error(msg)
        raise ValueError(msg)
    unique_id = str(uuid.uuid1()).replace('-', '_').upper()
    result_tbl = "#ACCURACY_MEASURE_RESULT_{}".format(unique_id)
    param_rows = []
    param_rows.extend([('MEASURE_NAME', None, None, metric_map[m]) for m in evaluation_metric])
    try:
        call_pal_auto_with_hint(conn,
                                None,
                                'PAL_ACCURACY_MEASURES',
                                data,
                                ParameterTable().with_data(param_rows),
                                result_tbl)
        return conn.table(result_tbl)
    except dbapi.Error as db_err:
        logger.exception(str(db_err))
        try_drop(conn, result_tbl)
        raise
    except pyodbc.Error as db_err:
        logger.exception(str(db_err.args[1]))
        try_drop(conn, result_tbl)
        raise
