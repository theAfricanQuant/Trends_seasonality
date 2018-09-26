import os
import pandas as pd
import numpy as np

def read_file(path):
    file = pd.read_csv(
        path,
        names=["Date", "Time", "Open", "High", "Low", "Close", "Volume"]
    )
    del file['Time']
    file['Date'] = pd.to_datetime(file['Date'])
    file['Year'] = file.Date.dt.year
    file['Month'] = file.Date.dt.month
    file['Week_day'] = file.Date.dt.weekday_name
    file['Week_year'] = file.Date.dt.weekofyear
    file['Day'] = file.Date.dt.day
    file['Returns'] = (file.Close/file.Close.shift(1)) - 1
    file['Direction'] = np.where(file.Returns >0,'Bull', 'Bear')
    file_A = file[['Date','Year', 'Month', 'Day', 'Week_day', 'Week_year', 'Open', 'High', 'Low', 'Close', 'Volume', 'Returns', 'Direction']]

    present = file_A.loc[file_A['Week_year']== 38,]
    bulls = present.loc[present['Direction'] == 'Bull',:]
    bears = present.loc[present['Direction'] == 'Bear',:]
    op_1 = bulls.loc[bulls['Week_day'] == 'Wednesday', :]
    op_2 = bears.loc[bears['Week_day'] == 'Wednesday', :]

    bull_Confidence =len(op_1)/(len(op_1) + len(op_2))
    print('Bull confidence: {0}'.format(bull_Confidence))

    bear_Confidence  = len(op_2)/(len(op_2) + len(op_1))
    print('Bear confidence: {0}'.format(bear_Confidence))

list_of_files = os.listdir()
print('*'*50)
for file in list_of_files:
    if '.csv' in file:
        print('Analysis for filename: {0}\n'.format(file))
        read_file(file)
        print('*'*50)