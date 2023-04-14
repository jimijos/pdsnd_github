import time
import pandas as pd


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['sunday', 'monday', 'tuesday',
        'wednesday', 'thursday', 'friday', 'saturday']

city_names = list(CITY_DATA.keys())


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            'Select the city you want to explore Chicago, new york city or Washington? \n> ').lower()
        if city in city_names:
            break
    # get user input for month (none, january, february, ... , june)
    while True:
        month = input(
            'Select a month or select \'none\' to apply no month filter. \n(e.g. none, january, february...etc) \n> ').lower()
        if month == 'none' or month in MONTHS:
            break
    # get user input for day of week (none, monday, tuesday, ... sunday)
    while True:
        day = input(
            'Select a day or select \'none\' to apply no day filter. \n(e.g. none,sunday, monday..etc ) \n> ').lower()
        if day == 'none' or day in DAYS:
            break

    print('-'*40)
    print('Calculating stats for city: {}, Month: {}, Day: {}'.format(
        city, month, day))
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Load data into a DataFrame from the specified city's CSV file
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime format for easier manipulation
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract the month and day of week and hour from the Start Time column to create new columns for easier filtering
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'none':
        # convert month name to its corresponding integer value
        month_index = MONTHS.index(month) + 1
        df = df[df['Start Time'].dt.month == month_index]

    # Filter by day of week if applicable
    if day != 'none':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print("The most common month is: {}".format(most_common_month.capitalize()))
    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of the week is: {}".format(
        most_common_day_of_week.capitalize()))
    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print("The most common start hour is: {}".format(most_common_start_hour))

    # Calculate total execution time
    total_time(start_time)
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is:", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is:", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[[
        'Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used Start and End stations are : {}, {}"
          .format(most_common_start_end_station[0], most_common_start_end_station[1]))

    total_time(start_time)
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel)

    total_time(start_time)
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count_stats(df)

    if 'Gender' in df.columns:
        gender_stats(df)

    if 'Birth Year' in df.columns:
        birth_year_stats(df)

    total_time(start_time)

    print('-'*20)
    # Simple chart
    print('\nUser Type Distribution:\n')
    user_types = df['User Type'].value_counts()
    max_count = max(user_types)
    for user_type, count in user_types.items():
        bar = ''.join(['█' for i in range(int(count/max_count*20))])
        print(f'{user_type}: {bar} {count}')
    print('-'*40)


def user_count_stats(df):
    print("Counts of user types:\n")
    user_counts = df['User Type'].value_counts()
    # Print the total numbers of user types
    for idx, user_count in enumerate(user_counts):
        print(" {}: {}".format(user_counts.index[idx], user_count))
    print('-'*20)


def gender_stats(df):
    # Display counts of gender
    print("Counts of gender:\n")
    gender_counts = df['Gender'].value_counts()
    # Print the total numbers of genders
    for idx, gender_count in enumerate(gender_counts):
        print(" {}: {}".format(gender_counts.index[idx], gender_count))
    print('-'*20)


def birth_year_stats(df):

    # Display earliest, most recent, and most common year of birth
    birth_year = df['Birth Year']
    # The most common birth year
    most_common_year = birth_year.mode()[0]
    print("The most common birth year is:", most_common_year)
    # The most recent birth year
    most_recent = birth_year.max()
    print("The most recent birth year is:", most_recent)
    # The most earliest birth year
    earliest_year = birth_year.min()
    print("The most earliest birth year is:", earliest_year)


def total_time(start_time):
    print("\nThis took %s seconds." % (time.time() - start_time))


def show_raw_data(df):
    """Displays raw data upon request by the user."""
    # Check if user wants to see raw data
    raw = input("Would you like to see raw data? (yes or no): ").lower()
    if raw != 'yes':
        return

    # Display raw data in batches of 5 rows until user stops requesting
    count = 0
    while True:
        print(df.iloc[count:count+5])
        count += 5
        more_raw = input(
            "Would you like to see more raw data? (yes or no): ").lower()
        if more_raw != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
