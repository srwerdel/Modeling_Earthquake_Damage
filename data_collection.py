import requests
import re
import pandas as pd

def get_data(url):
    '''Get the datasets from the Driven Data website by specific URLs and return a dataframe.'''

    html = requests.get(url)
    text = html.text.splitlines()

    # split each line into the columns, seperated by commas
    split_text = []
    for i in text:
        split_text.append(i.split(','))

    # get column names from first line
    col_names = split_text[0]

    value_dict = dict()
    # for each line add number of line as key and data as values to value_dictionary
    for i in range(1,len(split_text)):
        value_dict[i] = split_text[i]

    # create dataframe using column names and dictionary of data
    df = pd.DataFrame.from_dict(value_dict, orient='index', columns = col_names)

    # convert dtype into int or category
    pattern = re.compile(r'_id$|count_|age|_percentage$|has_|_grade$')
    for i in df.columns:
        if re.search(pattern, i):
            df[i] = df[i].astype(int)
        else:
            df[i] = df[i].astype('category')

    return df
