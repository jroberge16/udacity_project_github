import time
import pandas as pd
import numpy as np

# these dictionaries are used for refereces thoughout the python file
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

cities = {'1': 'chicago',
          '2': 'new york city',
          '3': 'washington'}

months = {'january': '1', 'feburary': '2', 'march': '3',
          'april': '4', 'may': '5', 'june': '6', 'july': '7',
          'august': '8', 'september': '9', 'october': '10',
          'november': '11', 'december': '12', 'all': '13'}

days_of_week = {'monday': '1', 'tuesday': '2', 'wednesday': '3',
                'thursday': '4', 'friday': '5', 'saturday': '6',
                'sunday': '7', 'all': '8'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    while True:
        print('Hello! Let\'s explore some US bikeshare data!')
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        print("Please choose  one of the follwing cities:\n")
        print(' 1.\t Chicago\n 2.\t New York City\n 3.\t washington\n')
        city = input().lower()
        if city not in cities.values() and city not in cities.keys():
            print(f"Input {city} is invalid. Please type a the name of the city or a line number")
            continue
        elif city in cities.keys():
            city = cities[city]
        break

    # get user input for month (all, january, february, ... , june)
    while True:
        print("Please Select a month from the follwing list")
        print(' 1.\t January\n 2.\t Febuary\n 3.\t March\n 4.\t April')
        print(' 5.\t May\n 6.\t June\n 7.\t July\n 8.\t Agust')
        print(' 9.\t September\n 10.\t Octoberge\n 11.\t November\n 12.\t December\n 13.\t all')
        month = input().lower()
        if month not in months.values() and month not in months.keys():
            print(f"Input {month} is invalid. Please type a the name of the month or a line number")
            continue
        elif month in months.keys():
            month = months[month]
        break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print('Please Select a day of the week from the follwing list:')
        print(' 1.\t Monday\n 2.\t Tuesday\n 3.\t Wednesday\n 4.\t Thursday\n 5.\t Friday\n 6.\t Saturday\n 7.\t Sunday\n 8.\t all')
        day = input().lower()
        if day not in days_of_week.values() and day not in days_of_week.keys():
            print(f"Input {day} is invalid. Please type a the name of the weekday or a line number")
            continue
        elif day in days_of_week.keys():
            day = days_of_week[day]
        break
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # getting city data and converting column into datetime object
    df = pd.read_csv(CITY_DATA[city])
    # ft engineering
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['dayofweek'] = df['Start Time'].dt.dayofweek + 1  # zero index for this mneasurment I disagree with
    df['End Time'] = pd.to_datetime(df['End Time'])
    # filtering out by month
    if month != '13':
        df = df[df['month'] == int(month)]
    # filtering out day of week
    if day != '8':
        df = df[df['dayofweek'] == int(day)]
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mode_month = df['month'].mode().astype(str).map({v: k for k, v in months.items()}).values
    print(f"The most occuring month:\t {mode_month}")

    # display the most common day of week
    mode_day = df['dayofweek'].mode().astype(str).map({v: k for k, v in days_of_week.items()}).values
    print(f"The most occuring day of week:\t {mode_day}")

    # display the most common start hour
    mode_hr = df['Start Time'].dt.hour.mode().values
    print(f"The most occuring hour:\t {mode_hr}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"Most common start station:\t{df['Start Station'].mode().values}\n")

    # display most commonly used end station
    print(f"Most common end station:\t{df['End Station'].mode().values}\n")

    # display most frequent combination of start station and end station trip
    temp_table = df[['Start Station', 'End Station']].copy()
    temp_table.loc[:,'counter'] = 1
    temp_table = temp_table.groupby(['Start Station', 'End Station'], as_index=False)\
                           .count().sort_values('counter').iloc[-1] # Used to gather number of occurcence

    print(f"Most frequent combination of start station and end station trip:")
    print(f'\t*Start Station:\t{temp_table["Start Station"]}')
    print(f'\t*End Station:\t{temp_table["End Station"]}')
    print(f"Total Trips:\t {temp_table['counter']}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['duration'] = df['End Time'] - df['Start Time']

    # display total travel time
    print(f"Total Travel Time:\t {df['duration'].sum()}")

    # display mean travel time
    print(f"Average Travel Time:\t {df['duration'].mean()}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"User type count:\n {df['User Type'].value_counts()}\n")

    # Display counts of gender
    print(f"User type count:\n {df['Gender'].value_counts()}\n")

    # Display earliest, most recent, and most common year of birth
    print("birthday info:")
    print(f"\t*earliest year:\t{int(df['Birth Year'].min())}")
    print(f"\t*most recent year:\t{int(df['Birth Year'].max())}")
    print(f"\t*most common:\t{df['Birth Year'].mode().astype(int).values}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_header(df):
    """Displays the first five rows"""

    print("Do you wish to see the first five rows? (yes/no)")
    user_answ = input()
    if user_answ == 'yes':
        starting = 0
        while True:
            starting+=5
            print(df.iloc[starting-5:starting])
            while True:
                print("do you wish to see the next five rows (yes/no)")
                user_answ = input()
                if user_answ == 'yes' or user_answ == 'no':
                    break
                else:
                    print("please type yes or no")
                    continue
            if user_answ == 'no':
                print("terminating program")
                break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if 'Gender' in df.columns:
            user_stats(df)
        get_header(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
