import pandas as pd
import os

COLS = ['img',
        'left_15',
        'left_30',
        'left_45',
        'left_60',
        'left_75',
        'right_15',
        'right_30',
        'right_45',
        'right_60',
        'right_75',
        'speed',
        'label',
        'steer']
final_df = pd.DataFrame(columns=COLS)

for csv in os.listdir('./readings'):
    df = pd.read_csv('./readings/{}'.format(csv))
    final_df = pd.concat([final_df, df])

final_df.to_csv("Train_data.csv", index=False)