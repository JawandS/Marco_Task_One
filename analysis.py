import pandas as pd
from datetime import datetime

# read data
recession_data = pd.read_csv('data/recession_data.csv')
gdp_data = pd.read_csv('data/gdp_data.csv')

question_one = """
(a) When did each recession start, and how many months did each recession last?
(b) Make a figure of the annualized GDP growth rate from 1960Q1-2023Q4. In terms of
duration and magnitude, which two recessions were the most severe? Why
"""

# 1a
# note: recessions start at the peak of a business cycle and end at the trough
# go through each peak
def question_one_a():
    with open("question_one.txt", "w") as f:
        # iterate through recession data
        for i in range(len(recession_data)):
            # get start and end dates
            start = recession_data.iloc[i]['peak']
            end = recession_data.iloc[i]['trough']
            # convert to datetime
            start = datetime.strptime(start, '%Y-%m-%d')
            end = datetime.strptime(end, '%Y-%m-%d')
            # write to file
            f.write(f"Recession {i+1} started on {start} and ended on {end}. It lasted for {end-start} months.\n")

# 1b
def question_one_b():
    # go through each quarter's GDP and calculate percent change
    gdp_data['gdp'] = gdp_data['gdp'].pct_change()
    # annualize results
    gdp_data['gdp'] = (1 + gdp_data['gdp'])**4 - 1
    # plot and save to file
    gdp_data.plot(x='date', y='gdp').get_figure().savefig('gdp_growth.png')

# question_one_b()
    
question_two = """
(a) Make a figure of the inflation rate from 1959Q1 to 2023Q4.
(b) What is the average inflation rate from 1960Q1 to 1982Q4? from 1983Q1 to 2020Q1?
and from 2020Q2 to 2023Q4? What changes in the economy explain the difference
between the average inflation rates?
"""

# 2a
def question_two_a():
    # read data
    price_deflator = pd.read_csv('price_deflator.csv')
    # create a series of year over year inflation
    inflation_series = {}
    for i in range(4, len(price_deflator)):
        # get the year
        year = price_deflator.at[i, 'date'].split("-")[0]
        # get the inflation
        inflation = 100 * ((float(price_deflator.at[i, 'value']) / float(price_deflator.at[i-4, 'value'])) - 1)
        # add to series
        inflation_series[year] = inflation
    # plot and save to file
    inflation_series = pd.Series(inflation_series)
    inflation_series.plot().get_figure().savefig('inflation.png')

# question_two_a()
    
def question_two_b():
    # read data
    price_deflator = pd.read_csv('price_deflator.csv')
    # create a series of year over year inflation
    inflation_series = {}
    for i in range(4, len(price_deflator)):
        # get the year
        year = price_deflator.at[i, 'date'].split("-")[0]
        # get the inflation
        inflation = 100 * ((float(price_deflator.at[i, 'value']) / float(price_deflator.at[i-4, 'value'])) - 1)
        # add to series
        inflation_series[year] = inflation
    # calculate average inflation rates
    avg_inflation = {}
    avg_inflation['1960-1982'] = (inflation_series['1982'] - inflation_series['1960']) / (1982 - 1960)
    avg_inflation['1983-2020'] = (inflation_series['2020'] - inflation_series['1983']) / (2020 - 1983)
    avg_inflation['2020-2023'] = (inflation_series['2023'] - inflation_series['2020']) / (2023 - 2020)
    # write to file
    with open("question_two.txt", "w") as f:
        f.write(f"The average inflation rate from 1960Q1 to 1982Q4 was {avg_inflation['1960-1982']}\n")
        f.write(f"The average inflation rate from 1983Q1 to 2020Q1 was {avg_inflation['1983-2020']}\n")
        f.write(f"The average inflation rate from 2020Q2 to 2023Q4 was {avg_inflation['2020-2023']}\n")

# question_two_b()
        
question_three = """
(a) Make a figure with both unemployment rates on the same graph (hint: include a legend
and use different line types).
(b) What was the maximum unemployment rate in each recession? Recently, what has
happened to these unemployment rates?
"""

# 3a
def question_three_a():
    # read data
    headline_unemployment = pd.read_csv('data/headline_unemployment.csv')
    u6_unemployment = pd.read_csv('data/u6_unemployment.csv')
    # plot both in the same file
    headline_unemployment['date'] = pd.to_datetime(headline_unemployment['date'])
    u6_unemployment['date'] = pd.to_datetime(u6_unemployment['date'])
    ax = headline_unemployment.plot(x='date', y='value', label='headline')
    u6_unemployment.plot(x='date', y='value', ax=ax, label='u6')
    ax.get_figure().savefig('unemployment.png')

# question_three()
    
def question_three_b():
    # read data
    headline_unemployment = pd.read_csv('data/headline_unemployment.csv')
    u6_unemployment = pd.read_csv('data/u6_unemployment.csv')
    u6_unemployment['date'] = pd.to_datetime(u6_unemployment['date'])
    headline_unemployment['date'] = pd.to_datetime(headline_unemployment['date'])    
    # get the maximum unemployment rate in each recession
    with open("question_three.txt", "w") as f:
        for i in range(len(recession_data)):
            # get start and end dates
            start = recession_data.iloc[i]['peak']
            end = recession_data.iloc[i]['trough']
            # convert to datetime
            start = datetime.strptime(start, '%Y-%m-%d')
            end = datetime.strptime(end, '%Y-%m-%d')
            # get the maximum unemployment rate
            max_headline = -1
            max_headline_year = None
            max_u6 = -1
            max_u6_year = None
            for j in range(len(headline_unemployment)):
                if headline_unemployment.at[j, 'date'] >= start and headline_unemployment.at[j, 'date'] <= end:
                    max_headline = max(max_headline, float(headline_unemployment.at[j, 'value']))
                    max_headline_year = headline_unemployment.at[j, 'date'].year
                if u6_unemployment.at[j, 'date'] >= start and u6_unemployment.at[j, 'date'] <= end:
                    max_u6 = max(max_u6, float(u6_unemployment.at[j, 'value']))
                    max_u6_year = u6_unemployment.at[j, 'date'].year
            print(max_headline, max_u6)
            # write to file
            if not max_u6_year:
                continue
            f.write(f"Max headline unemployment {max_headline_year} {max_headline} and max u6 unemployment rate of {max_u6_year} {max_u6}\n")

question_three_b()