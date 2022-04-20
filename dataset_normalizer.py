import re

import pandas as pd
from pandas import read_csv

regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regex_number = r'^(?:\+)?(?:38)(?:\[0-9]\{3}[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|[0-9]{3}[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|[0-9]{3}[0-9]{7})(?:;)?$'
regex_website = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'


def split_contacts(row):
    if not isinstance(row, float):
        phone_numbers = re.findall(regex_number, row)
        emails = re.findall(regex_email, row)
        websites = re.findall(regex_website, row)
        return phone_numbers, emails, websites
    return [], [], []


def normalize(data):
    result_data = pd.DataFrame(
        columns=["зареєстровано", 'date', 'some_number', 'some_string', "another_string", 'phone_number', 'email', 'website']
    )
    for index, row in data.iterrows():
        phone_numbers, emails, websites = split_contacts(row[data.columns[-1]])
        custom_row = pd.DataFrame({
            "зареєстровано": row[data.columns[0]],
            'date':row[data.columns[1]],
            'some_number': row[data.columns[2]],
            'some_string': row[data.columns[3]],
            'another_string': row[data.columns[4]],
            'phone_number': '; '.join(phone_numbers),
            'email': '; '.join(emails),
            'website': '; '.join(websites)
        }, index=[0])
        result_data = pd.concat([result_data, custom_row], ignore_index=True, sort=False)
        print(index/len(data) * 100, "%", sep="")
    phone_numbers, emails, websites = split_contacts(data.columns[-1])
    custom_row = pd.DataFrame({
        "зареєстровано": data.columns[0],
        'date': data.columns[1],
        'some_number': data.columns[2],
        'some_string': data.columns[3],
        'another_string': data.columns[4],
        'phone_number': '; '.join(phone_numbers),
        'email': '; '.join(emails),
        'website': '; '.join(websites)
    }, index=[0])
    result_data = pd.concat([result_data, custom_row], ignore_index=True, sort=False)
    result_data.to_csv('result.csv', index=False)


if __name__ == "__main__":
    data = read_csv("dataset.csv", sep='\t', error_bad_lines=False)
    normalize(data=data)
