import pandas as pd

data = pd.DataFrame({"category":"A B C D E F U A B C A D E F U".split(),
                   "number":[10,1,12,23,1,0,4,6,8,21,1,4,34,0,8]},
                    index = pd.date_range("2016-01-01", periods = 15, freq = "D"))

pd.pivot_table(data, values="number",index = "category", aggfunc='mean')

test_data = pd.read_csv('https://stats.idre.ucla.edu/stat/data/binary.csv', nrows=270)