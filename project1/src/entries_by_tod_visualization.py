from ggplot import *
from pandas import *
from datetime import datetime


def plot_weather_data(
        turnstile_weather, start_unit, end_unit, fill, title, filter_function=lambda x: True
    ):
    turnstile_weather = turnstile_weather[turnstile_weather['UNIT'] >= start_unit]
    turnstile_weather = turnstile_weather[turnstile_weather['UNIT'] <= end_unit]

    turnstile_weather = turnstile_weather[turnstile_weather.apply(filter_function, axis=1)]

    hourly_group = turnstile_weather[['Hour', 'ENTRIESn_hourly', 'UNIT']].groupby(['Hour', 'UNIT'])
    mean_hourly = hourly_group.mean()
    mean_hourly = mean_hourly.reset_index()
    
    plot = ggplot(mean_hourly, aes('Hour', 'ENTRIESn_hourly'))\
        + geom_bar(stat='identity', fill=fill)\
        + ggtitle(title)\
        + scale_x_continuous(limits=(-0.5, 23.5))\
        + facet_wrap('UNIT')

    return plot


def is_weekday(record):
    dt = datetime.strptime(record['DATEn'], '%Y-%m-%d')
    dow = dt.weekday()
    
    return dow < 5

def is_weekend(record):
    return not is_weekday(record)

if __name__ == '__main__':
    turnstile_weather = read_csv('../data/turnstile_data_master_with_weather.csv')
    print plot_weather_data(
        turnstile_weather, 'R540', 'R545', 'blue',
        'Average entries by time of day (Weekdays)',
        is_weekday
    )

    print plot_weather_data(
        turnstile_weather, 'R540', 'R545', 'red',
        'Average entries by time of day (Weekends)',
        is_weekend
    )

    print plot_weather_data(
        turnstile_weather, 'R310', 'R313', 'orange',
        'Average entries by time of day (Weekends)',
        is_weekend
    )
