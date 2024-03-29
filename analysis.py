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
    with open("answers/question_one.txt", "w") as f:
        # iterate through recession data
        for i in range(len(recession_data)):
            # get start and end dates
            start = recession_data.iloc[i]['peak']
            end = recession_data.iloc[i]['trough']
            # convert to datetime
            start = datetime.strptime(start, '%Y-%m-%d')
            end = datetime.strptime(end, '%Y-%m-%d')
            length_in_months = (end.year - start.year) * 12 + end.month - start.month
            # write to file
            f.write(f"Recession {i+1} started on {start} and ended on {end}. It lasted for {length_in_months} months.\n")

# question_one_a()

# 1b
def question_one_b():
    # go through each quarter's GDP and calculate percent change
    gdp_data['gdp'] = gdp_data['gdp'].pct_change()
    # write percent change to file
    gdp_data.to_csv('data/gdp_data_percent.csv')
    # annualize results
    gdp_data['gdp'] = ((1 + gdp_data['gdp'])**4) - 1
    # Write the annualized GDP growth rate to a file
    gdp_data.to_csv('data/gdp_growth_annualized.csv')
    # scale by 100
    gdp_data['gdp'] = gdp_data['gdp'] * 100
    # plot using matplotlib
    gdp_data['date'] = pd.to_datetime(gdp_data['date'])
    ax = gdp_data.plot(x='date', y='gdp')
    # add grid to plot
    ax.grid()
    # add title and labels
    ax.set_title('Annualized GDP Growth Rate Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('GDP Growth Rate (%)')
    # save to file
    ax.get_figure().savefig('answers/gdp_growth.png')

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
    price_deflator = pd.read_csv('data/price_deflator.csv')
    # create a series of year over year inflation
    inflation_series = {}
    for i in range(4, len(price_deflator), 4):
        # get the year
        year = price_deflator.at[i, 'date'].split("-")[0]
        # get the inflation
        inflation = 100 * ((float(price_deflator.at[i, 'value']) / float(price_deflator.at[i - 4, 'value'])) - 1)
        # add to series
        inflation_series[year] = inflation
    # convert to series
    inflation_series = pd.Series(inflation_series)
    # set x axis to be the year
    inflation_series.index = pd.to_datetime(inflation_series.index)
    # save to file
    inflation_series.to_csv('data/inflation.csv')
    # plot
    inflation_series = pd.Series(inflation_series)
    ax = inflation_series.plot()
    # add grid
    ax.grid()
    # add title and labels
    ax.set_title('Inflation Rate Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Inflation Rate (%)')
    # save to file
    ax.get_figure().savefig('answers/inflation.png')

# question_two_a()
    
def question_two_b():
    # read data
    inflation_data = pd.read_csv('data/inflation.csv')
    # average from 1960 to 1982
    avg_one = inflation_data[(inflation_data['date'] >= '1960-01-01') & (inflation_data['date'] <= '1982-12-31')]['value'].mean()
    # average from 1983 to 2020
    avg_two = inflation_data[(inflation_data['date'] >= '1983-01-01') & (inflation_data['date'] <= '2020-12-31')]['value'].mean()
    # average from 2020 to 2023
    avg_three = inflation_data[(inflation_data['date'] >= '2020-01-01') & (inflation_data['date'] <= '2023-12-31')]['value'].mean()
    # write to file
    with open("answers/question_two.txt", "w") as f:
        f.write(f"Average inflation from 1960 to 1982: {avg_one}\n")
        f.write(f"Average inflation from 1983 to 2020: {avg_two}\n")
        f.write(f"Average inflation from 2020 to 2023: {avg_three}\n")

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
    # add grid
    ax.grid()
    # add title and labels
    ax.set_title('Unemployment Rates Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Unemployment Rate (%)')
    # save to file
    ax.get_figure().savefig('answers/unemployment.png')

# question_three_a()
    
def question_three_b():
    # read data
    headline_unemployment = pd.read_csv('data/headline_unemployment.csv')
    u6_unemployment = pd.read_csv('data/u6_unemployment.csv')
    u6_unemployment['date'] = pd.to_datetime(u6_unemployment['date'])
    headline_unemployment['date'] = pd.to_datetime(headline_unemployment['date'])    
    # get the maximum unemployment rate in each recession
    with open("answers/question_three.txt", "w") as f:
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

# question_three_b()