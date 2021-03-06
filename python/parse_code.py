import pandas as pd
import numpy as np
import ast
from pathlib import Path
import matplotlib.pyplot as plt


def load_file(filepath):
    with open(filepath, 'r') as f:
        d = f.read()
        data = ast.literal_eval(d)

    return pd.DataFrame(data)

def dance_timing(row):
    if row['time'] < .858:
        return '1'
    elif row['time'] < 1.294:
        return '2'
    elif row['time'] < 1.898:
        return '3'
    elif row['time'] < 2.549:
        return '4'
    elif row['time'] < 3.008:
        return '5'
    elif row['time'] < 3.396:
        return '6'
    elif row['time'] < 4.227:
        return '7'
    elif row['time'] < 4.930:
        return '8'
    elif row['time'] < 6.512:
        return '9'
    elif row['time'] < 7.386:
        return '10'
    elif row['time'] < 8.130:
        return '11'
    elif row['time'] < 8.938:
        return '12'
    elif row['time'] < 9.751:
        return '13'
    elif row['time'] < 10.564:
        return '14'
    elif row['time'] < 11.376:
        return '15'
    elif row['time'] < 12.900:
        return '16'
    elif row['time'] < 13.765:
        return '17'
    elif row['time'] < 14.591:
        return '18'
    else:
        return 19

def move_classify(data):
    data['move_label'] = data.apply(lambda row: dance_timing(row), axis=1)
    return data

def smooth(data):
    time = data['time']
    mean = data.mean(axis=0)
    data = data.subtract(mean, axis = 1)
    data['time'] = time

    data['accel_x'] = data['accel_x'] / data['accel_x'].max()
    data['accel_y'] = data['accel_y'] / data['accel_y'].max()
    data['accel_z'] = data['accel_z'] / data['accel_z'].max()
    data['gyro_x'] = data['gyro_x'] / data['gyro_x'].max()
    data['gyro_y'] = data['gyro_y'] / data['gyro_y'].max()
    data['gyro_z'] = data['gyro_z'] / data['gyro_z'].max()

    data['accel_x'] = data['accel_x'].rolling(window=15).mean()
    data['accel_y'] = data['accel_y'].rolling(window=15).mean()
    data['accel_z'] = data['accel_z'].rolling(window=15).mean()
    data['accel_x_std'] = data['accel_x'].rolling(window=15).std()
    data['accel_y_std'] = data['accel_y'].rolling(window=15).std()
    data['accel_z_std'] = data['accel_z'].rolling(window=15).std()
    data['gyro_x'] = data['gyro_x'].rolling(window=15).mean()
    data['gyro_y'] = data['gyro_y'].rolling(window=15).mean()
    data['gyro_z'] = data['gyro_z'].rolling(window=15).mean()
    data['gyro_x_std'] = data['gyro_x'].rolling(window=15).std()
    data['gyro_y_std'] = data['gyro_y'].rolling(window=15).std()
    data['gyro_z_std'] = data['gyro_z'].rolling(window=15).std()
    return data


def create_list(folderpath):


    pathlist = Path(folderpath).glob('**/*.txt')
    accel = []
    gyro = []
    for path in pathlist:
        path_in_str = str(path)
        data = load_file(path_in_str)
        if "accel" in path_in_str:
            single_entry = {"entry": path_in_str.split('/')[2],
                            "data": data}
            accel.append(single_entry)
        else:
            single_entry = {"entry": path_in_str.split('/')[2],
                            "data": data}
            gyro.append(single_entry)


    X = pd.DataFrame()
    for file1 in accel:
        for file2 in gyro:
            if file1['entry'] == file2['entry']:
                data2 = file2['data']
                data = pd.concat([file1['data'], data2['gyro_x'],
                                  data2['gyro_y'], data2['gyro_z']], axis=1)
                data = smooth(data)
                start_time = data['time'].iloc[0]
                data['time'] = data['time'] - start_time
                data = move_classify(data).dropna()

                '''
                fig, (ax0, ax1, ax2) = plt.subplots(nrows=3,
                                                    figsize=(15, 10),
                                                    sharex=True)
                ax0.plot(data['time'], data['accel_x'])
                ax1.plot(data['time'], data['accel_y'])
                ax2.plot(data['time'], data['accel_z'])
                plt.subplots_adjust(hspace=0.2)
                plt.subplots_adjust(top=0.90)
                plt.show()
                '''

                if X.empty == True:
                    X = data
                else:
                    X = X.append(data)

    Y = X.move_label
    X = X.drop(['move_label'], axis=1)

    return X, Y

def plot_axis(ax, x, y, title):

    ax.plot(x, y, 'r')
    ax.set_title(title)
    ax.xaxis.set_visible(False)
    ax.set_ylim([min(y) - np.std(y), max(y) + np.std(y)])
    ax.set_xlim([min(x), max(x)])
    ax.grid(True)

if __name__ == '__main__':
    data = create_list('../data/')

    # change the name of file of the formatted data here
    data[0].to_csv(r'X_train.txt', index=False, header=False)
    # change the name of the file of the labels here
    data[1].to_csv(r'Y_train.txt', index=False, header=False)



