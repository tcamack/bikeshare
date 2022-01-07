"""Bikeshare data analysis."""

import os
import time

import pandas as pd


CITY_DATA = {**dict.fromkeys(['1', 'chicago'], 'data/chicago.csv'),
             **dict.fromkeys(['2', 'nyc', 'new york city', 'new york'], 'data/new_york_city.csv'),
             **dict.fromkeys(['3', 'washington'], 'data/washington.csv')}

MONTH_DATA = {**dict.fromkeys(['1', 'january'], 1),
              **dict.fromkeys(['2', 'february'], 2),
              **dict.fromkeys(['3', 'march'], 3),
              **dict.fromkeys(['4', 'april'], 4),
              **dict.fromkeys(['5', 'may'], 5),
              **dict.fromkeys(['6', 'june'], 6),
              **dict.fromkeys(['7', 'all'], 7)}

DAY_DATA = {**dict.fromkeys(['1', 'monday'], 1),
            **dict.fromkeys(['2', 'tuesday'], 2),
            **dict.fromkeys(['3', 'wednesday'], 3),
            **dict.fromkeys(['4', 'thursday'], 4),
            **dict.fromkeys(['5', 'friday'], 5),
            **dict.fromkeys(['6', 'saturday'], 6),
            **dict.fromkeys(['7', 'sunday'], 7),
            **dict.fromkeys(['8', 'all'], 8)}

MONTHS = {1: 'january',
          2: 'february',
          3: 'march',
          4: 'april',
          5: 'may',
          6: 'june',
          7: 'all'}

DAYS = {1: 'monday',
        2: 'tuesday',
        3: 'wednesday',
        4: 'thursday',
        5: 'friday',
        6: 'saturday',
        7: 'sunday',
        8: 'all'}


def clear():
    """Clear the terminal."""
    os.system('cls')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city_temp = ''
    month_temp = ''
    day_temp = ''
    clear()
    print('Hello! Let\'s explore some US bikeshare data!')

    while city_temp not in CITY_DATA.keys():
        print('Please choose your city from the following:')
        print('Note: You can use numbers or you can type the name.')
        print('1. Chicago')
        print('2. New York City')
        print('3. Washington')
        city_temp = input().lower()
        clear()

        if city_temp not in CITY_DATA.keys():
            clear()
            print('City name not recognized, please try again.')
            print('-' * 50)

    city = CITY_DATA[city_temp].replace('_', ' ').replace('data/', '').replace('.csv', '')

    while month_temp not in MONTH_DATA.keys():
        print(f'You have selected data in {city.title()}.')
        print('-' * 50)

        print('Please choose a month from the following:')
        print('Note: You can use numbers or you can type the name.')
        for key, value in MONTHS.items():
            if key:
                print(f'{key}. {value.title()}')
        month_temp = input().lower()
        clear()

        if month_temp not in MONTH_DATA.keys():
            clear()
            print('Month not recognized, please try again.')
            print('-' * 50)

    month = MONTHS[MONTH_DATA[month_temp]]

    while day_temp not in DAY_DATA:
        print(f'You have selected data in {city.title()} during the '
              f'month{f" of {month.title()}" if (MONTH_DATA[month_temp] != 7) else "s of January through June"}.')
        print('-' * 50)

        print('Please choose a day from the following:')
        print('Note: You can use numbers or you can type the name.')
        for key, value in DAYS.items():
            if key:
                print(f'{key}. {value.title()}')
        day_temp = input().lower()
        clear()

        if day_temp not in DAY_DATA.keys():
            clear()
            print('Day not recognized, please try again.')
            print('-' * 50)

    day = DAYS[DAY_DATA[day_temp]]

    return city, month, day


def load_data(city, month, day):
    """
    Load data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print(f'Loading data for {city.title()}...\n')

    try:
        df = pd.read_csv(CITY_DATA[city])

        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['day'] = df['Start Time'].dt.day_name()
        df['month'] = df['Start Time'].dt.month

        if month != 'all':
            df = df[df['month'] == MONTH_DATA[month]]

        if day != 'all':
            df = df[df['day'] == day.title()]
    except FileNotFoundError:
        df = None
        clear()
        print(f'Failed to locate ".{CITY_DATA[city]}" file.')
        print('Data files should be located in the ./data '
              'folder in the source directory.')
        print('-' * 50)
    except pd.errors.EmptyDataError:
        df = None
        clear()
        print(f'Error importing ".{CITY_DATA[city]}" file.')
        print('The file is empty or is missing headers.')
        print('-' * 50)

    if df is not None:
        print(f'Data successfully loaded for {city.title()}.')
        print('\n' + '-' * 50)

    return df


def time_stats(df):
    """Display statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['hour'] = df['Start Time'].dt.hour

    common_month = df['month'].mode()[0]
    common_day = df['day'].mode()[0]
    common_hour = df['hour'].mode()[0]

    # Display time statistics.
    print(f'Month with the most usage: {MONTHS[common_month].title()}')
    print(f'Day of the week with the most usage: {common_day}')
    print(f'Hour of the day with the most usage: {common_hour}:00')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 50)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df['Start -> End'] = df['Start Station'].str.cat(df['End Station'], sep=' -> ')

    common_start_station = df['Start Station'].mode()[0]
    common_end_station = df['End Station'].mode()[0]
    common_combination = df['Start -> End'].mode()[0]

    # Display station statistics.
    print(f'Most popular start station: {common_start_station}')
    print(f'Most popular end station: {common_end_station}')
    print(f'Most popular station combination: {common_combination}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 50)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time.
    total_travel_time = round(df['Trip Duration'].sum())
    total_minutes, total_seconds = divmod(total_travel_time, 60)
    if total_minutes > 60:
        total_hours, total_minutes = divmod(total_minutes, 60)
        print(f'The total trip duration is {total_hours} hours, '
              f'{total_minutes} minutes, and {total_seconds} seconds.')
    else:
        print(f'The total trip duration is {total_minutes} minutes '
              f'and {total_seconds} seconds.')

    # Display mean travel time.
    average_travel_time = round(df['Trip Duration'].mean())
    average_minutes, average_seconds = divmod(average_travel_time, 60)
    if average_minutes > 60:
        average_hours, average_minutes = divmod(average_minutes, 60)
        print(f'The average trip duration is {average_hours} hours, '
              f'{average_minutes} minutes, and {average_seconds} seconds.')
    else:
        print(f'The average trip duration is {average_minutes} minutes '
              f'and {average_seconds} seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 50)


def user_stats(df, city):
    """Display statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    user_type = df['User Type'].value_counts()

    print(f'The types of users by number are the following:\n{user_type}\n')

    # Display counts of gender, gender data is not always present.
    try:
        gender = df['Gender'].value_counts()
        print(f'The amount of users by gender are:\n{gender}\n')
    except KeyError:
        print(f'Data from {city.title()} does not contain gender data.')

    # Display birth year statistics, birth year data is not always present.
    try:
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f'The earliest birth year is: {oldest}')
        print(f'The most recent birth year is: {youngest}')
        print(f'The most common birth year is: {common_year}')
    except KeyError:
        print(f'Data from {city.title()} does not contain birth year data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 50)


def display_data(df):
    """Display rows of data from the .csv data file for the selected city."""
    line = 0

    while True:
        view_data = input('\nWould you like to view five lines of raw data? '
                          'Enter yes or no.\n')
        if view_data.lower() == 'yes':
            clear()
            print(df.head())
            while True:
                view_additional_data = input('\nWould you like to view five additional '
                                             'lines of raw data? Enter yes or no.\n')
                if view_additional_data.lower() == 'yes':
                    line += 5
                    clear()
                    print(df[line:line + 5])
                elif view_additional_data.lower() == 'no':
                    clear()
                    break
                else:
                    clear()
                    print('Input not recognized.')
            break
        elif view_data.lower() == 'no':
            clear()
            break
        else:
            clear()
            print('Input not recognized.')


def main():
    """Initialize main variables and dataframe from imported .csv file."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df is not None:
            display_data(df)
            print(f'\nDisplaying bikeshare data from {city.title()}'
                  f'{f" for every {day.title()}" if (day != "all") else ""} in '
                  f'{month.title() if (MONTH_DATA[month] != 7) else "January until June"}.\n')
            print('-' * 50)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            clear()
            break


if __name__ == "__main__":
    main()
