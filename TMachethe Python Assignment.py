"""
Created on Wed Feb 16 18:51:22 2022

@author: TMACHETHE
"""
import time
from datetime import date
import pandas as pd
from tabulate import tabulate


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

Months = ['january', 'february', 'march', 'april', 'may', 'june','all']

Week_day = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','all' ]

Cities = ['chicago','new york city','washington']



def get_filters():
    
    """
    Asks user to specify a city, month, and/or day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
    """
    print('\n Hello! Let\'s explore some US bikeshare data!')
    
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
       city = input('Which city do you want to explore Chicago, New York City or Washington? \n> ').lower()
       if city in Cities:
            break
       else: 
           print('The city name you entered is not in our current database, please follow \
              the instructions and specify one of the cities in the database')
              
    # get user input for month (all, january, february, ... , june)
    while True:
       month = input('Are interested in a particular month?, Provide us a month name (e.g. January,February,...or June) '\
                    'or just say \'all\' to apply no month filter. \n> ').lower()
           
       if month in Months:
            break
       else: 
           print('\n The month you entered is not in our current database, please enter a \
 month between Jan and Jun (NB: please ensure your spelling is correct ) \n ')
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
       day = input('Last question before we provide you with the relevant information,specify the week day(e.g. Sunday,Monday,...or Saturday)\
 you want to analyze.You can type \'all\' again to apply no day filter.\n> ').lower()
           
       if day in Week_day:
            break
       else: 
           print('\nYou didn''t enter a valid week day,please enter a day between Sunday \
                 and Saturday (NB:please ensure your spelling is correct ) \n ')
              
              
    print('-'*60)
    return city, month, day

def Load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
 # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month,day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    df['Start_Hour']  =df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def DataSet_overview(df, city):
    
    """Displays general overview about the Dataset from Bike share."""
    
    print('\nOverview of the {} dataset...\n'.format(city).title())
    
    #How many missing values are there in each column of the dataset 
    #1st line gives the total items and 2nd gives NaN values in each column 
    print('Number of items in the {} dataset for each column:\n{}'.format(city,df.count()))
    print('Number of NaN items in the {} dataset for each column:\n{}'.format(city,df.isnull().sum()))
    
    print('-'*70)
    
def Popular_time_of_travel(df):
    
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode().values.tolist()
    
    print("The most common month(s) is :", *most_common_month)

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode().values.tolist()
    print("The most common day of week is :", *most_common_day_of_week)

    # display the most common start hour
    most_common_start_hour = df['Start_Hour'].mode().values.tolist()
    print("The most common start hour is :", *most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    
    print('-'*70)

def Popular_station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Common_start_station = df['Start Station'].mode().values.tolist()
    print("The most commonly used start station(s) is :", *Common_start_station)

    # display most commonly used end station
    Common_end_station = df['End Station'].mode().values.tolist()
    print("The most commonly used end station(s) is :", *Common_end_station)

    # display most frequent combination of start station and end station trip
    
    Most_Common_Trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most common trip is from {} to {}".format(*Most_Common_Trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    
    print('-'*70)

def Trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

     # display total travel time
    Total_travel_time = (df['Trip Duration'].sum())*(1/3600)
    Earliest_date = df['Start Time'].dt.date.min()
    Latest_date = pd.to_datetime(df['End Time']).dt.date.max()
    print("Total travel time by all users from {} to {} is {:.2f} hours".format(Earliest_date,Latest_date,Total_travel_time))

    # display mean travel time
    Avg_Time_per_Trip = (df['Trip Duration'].mean())/60
    print("Mean travel time is {:.2f} mins.".format(Avg_Time_per_Trip))

    # display max travel time and longest trip details
    max_travel_time = (df['Trip Duration'].max())/60
    print("Max travel time was {:.2f} mins.".format(max_travel_time))
    
    start_location = df.loc[df['Trip Duration'] == max_travel_time*60,'Start Station'].item()
    End_location = df.loc[df['Trip Duration'] == max_travel_time*60,'End Station'].item()
    
    print("The longest trip was from {} to {},it took {:.2f} mins to complete.".format(start_location,End_location,max_travel_time))

    print('\nTravel stats for each user type available on Bike Share:\n')
    
    # display the mean trip duration for each user type using the platform.
    User_type = (df.groupby(['User Type'])['Trip Duration'].mean())/60
    for index, duration in enumerate(User_type):
        print("The average trip duration for {}s is {:.2f} mins".format(User_type.index[index], duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*70)


def User_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

     # Display counts of user types
    print("Counts of user types:\n")
    Type_user = df.groupby(['User Type']).size()
    
    # iteratively print out the total numbers of user types 
    for index, count in enumerate(Type_user):
        print("There are {} {}(s)".format(count,Type_user.index[index]))
        
    #Check if the city filtered for has data about the users's gender before evaluating the stats on gender
    if 'Gender' in df.columns:
        # Display counts of gender
        Gender_stats(df)
    else: 
      print('\nThe city you are analysing data for does not collect any data on gender.')
      
    #Check if the city filtered for has data about the users's gender before evaluating the stats on gender
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        Age_stats(df)
    else: 
      print('The city you are analysing data for does not collect any data on user birth year.')
      
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*70)

def Gender_stats(df):
    
    """Displays statistics of analysis based on the gender of bikeshare users."""

    # Display counts of gender
    print("\nCounts of gender:\n")
    Gender_count = df['Gender'].value_counts()
    
    # iteratively print out the total numbers of genders 
    for index, count in enumerate(Gender_count):
        print("There are {} {}s recorded on the platform".format(count,Gender_count.index[index]))
    
    
def Age_stats(df):
    
    """Displays statistics of analysis based on the birth years of bikeshare users."""
    # pd.to_date(df['Birth Year']).dt.date.max()
    # Display oldest, youngest, and most common year of birth
    current_year = date.today().year
    Earliest_year = df['Birth Year'].min()
    Latest_year = df['Birth Year'].max()
    Oldest_user_Age = current_year - Earliest_year
    Youngest_user_Age = current_year - Latest_year
    
    print('\nThe oldest user recorded on the platform is {} years old'.format(Oldest_user_Age))
    print('The youngest user recorded on the platform is {} years old'.format(Youngest_user_Age))
    
    # the most common birth year
    most_common_birth_year =df['Birth Year'].mode()
    print("The most common birth year(s) is/are:", *most_common_birth_year)

def Raw_data(df):
    
    """Displays raw bikeshare data."""
       
    #Number of rows in the dataset
    Row_length = df.shape[0]
        
    # iterates through the dataset in steps of 5 rows.
    for i in range(0, Row_length, 5):
        Raw_dataset_query = input('\nWould you like to see the raw dataset in subsets of 5 rows? Type \'yes\' or \'no\'\n> ')
        if Raw_dataset_query.lower() != 'yes':
            break
        
        # retrieve 5 rows of the raw dataset
        Raw_data = df.iloc[i: i + 5]
        Raw_data.drop(columns=df.columns[0], axis=1, inplace=True)
        
        print(tabulate(Raw_data, headers = 'keys', tablefmt = 'psql',showindex ='False',stralign=('left'),numalign='left'),)
         
        

def main():
    while True:
        city, month, day = get_filters()
        df = Load_data(city, month, day)
        
        DataSet_overview(df, city)
        Popular_time_of_travel(df)
        Popular_station_stats(df)
        Trip_duration_stats(df)
        User_stats(df)
        Raw_data(df)
        
        
        restart = input('\nWould you like to restart and apply new filters? Enter yes or no.\n>')
        if restart.lower() != 'yes':
            break
    
    print('Thank you for your engagement!.')
        
if __name__ == "__main__":
	main()
