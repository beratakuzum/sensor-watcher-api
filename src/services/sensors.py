import pandas as pd

from flask import current_app
from datetime import timedelta

from src.utils.dates import get_week_period
from src.utils.errors import API_ERROR


def _ensure_period_has_values(db_values, period_start, period_end, sensor_id, date_format):
    """Raises API error if there is no any sensor values in the specified period"""

    period_start = period_start.strftime(date_format)
    period_end = period_end.strftime(date_format)

    if not db_values:
        raise API_ERROR(
            error_type="sensorValuesError",
            message=f"There is no any values of the {sensor_id} sensor for {period_start} - {period_end} period",
            status_code=404
        )


def _calculate_moving_average(df):
    """Calculates moving average of a dataframe by resampling it to a daily frequency"""
    df.set_index('date_time', inplace=True)
    daily_resampled = df.sensor_value.resample('D').mean()

    # we don't have to use the rolling.mean(1) function because it gives the same value of daily_resampled
    return pd.DataFrame(daily_resampled)


def get_moving_average_diff_two_weeks(sensor_id, input_date_object):
    """
        gets sensor values from mongo db and calculates
        the average difference between moving average of week i and week i+1
     """

    # get start and end dates of week i
    week_1_start, week_1_end = get_week_period(input_date_object)

    # get start and end dates of week i+1
    week_2_start = week_1_start + timedelta(days=7)
    week_2_end = week_1_end + timedelta(days=7)

    mongo_db = current_app.mongo_db

    # get sensor_values of week i
    week_1_sensor_values = mongo_db.find(collection_name='sensor_values',
                                         where={
                                             'sensor_id': sensor_id,
                                             'date_time': {'$gte': week_1_start, '$lt': week_1_end}
                                         },
                                         select={"date_time": 1, "sensor_value": 1, "_id": 0}
                                         )

    _ensure_period_has_values(week_1_sensor_values, week_1_start, week_1_end, sensor_id, "%d/%m/%Y")

    # get sensor_values of week i+1
    week_2_sensor_values = mongo_db.find(collection_name='sensor_values',
                                         where={
                                             'sensor_id': sensor_id,
                                             'date_time': {'$gte': week_2_start, '$lt': week_2_end}
                                         },
                                         select={"date_time": 1, "sensor_value": 1, "_id": 0}
                                         )

    _ensure_period_has_values(week_2_sensor_values, week_2_start, week_2_end, sensor_id, "%d/%m/%Y")

    week_1_df = pd.DataFrame(week_1_sensor_values)
    week_2_df = pd.DataFrame(week_2_sensor_values)

    week_1_daily_ma = _calculate_moving_average(week_1_df)
    week_2_daily_ma = _calculate_moving_average(week_2_df)

    difference = week_2_daily_ma.mean() - week_1_daily_ma.mean()

    return {
        "difference": float(difference)
    }


def get_moving_average_diff_two_periods(periods, sensor_id):
    period_1_start = periods['period_1_start']
    period_1_end = periods['period_1_end']
    period_2_start = periods['period_2_start']
    period_2_end = periods['period_2_end']

    mongo_db = current_app.mongo_db

    # get sensor_values of period 1
    period_1_sensor_values = mongo_db.find(collection_name='sensor_values',
                                           where={
                                               'sensor_id': sensor_id,
                                               'date_time': {'$gte': period_1_start,
                                                             '$lte': period_1_end}
                                           },
                                           select={"date_time": 1, "sensor_value": 1, "_id": 0}
                                           )

    _ensure_period_has_values(period_1_sensor_values, period_1_start, period_1_end, sensor_id, "%d/%m/%Y %H:%M")

    period_2_sensor_values = mongo_db.find(collection_name='sensor_values',
                                           where={
                                               'sensor_id': sensor_id,
                                               'date_time': {'$gte': period_2_start,
                                                             '$lte': period_2_end}
                                           },
                                           select={"date_time": 1, "sensor_value": 1, "_id": 0}
                                           )

    _ensure_period_has_values(period_2_sensor_values, period_2_start, period_2_end, sensor_id, "%d/%m/%Y %H:%M")

    period_1_df = pd.DataFrame(period_1_sensor_values)
    period_2_df = pd.DataFrame(period_2_sensor_values)

    period_1_daily_ma = _calculate_moving_average(period_1_df)
    period_2_daily_ma = _calculate_moving_average(period_2_df)

    difference = period_2_daily_ma.mean() - period_1_daily_ma.mean()

    return {
        "difference": float(difference)
    }
