# -*- coding: utf-8 -*-

import pandas as pd

df = pd.read_csv('patent_data.csv')

print(df['Patent Title'])
