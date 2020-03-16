import pandas as pd
import ast
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


def load_file(filepath):
    with open(filepath, 'r') as f:
        d = f.read()
        data = ast.literal_eval(d)

    return pd.DataFrame(data)

def calculation(df):

    list = []
    df = df['seq']
    for data in df:
        data_row = data['data']
        data_row = pd.DataFrame(data_row, index=[0])
        list.append(data_row)
    final = pd.concat(list)
    final = final.drop(['xGyro', 'yGyro', 'zGyro', 'xMag', 'yMag', 'zMag'], axis=1)

    x = final['xAccl'].as_matrix()
    y = final['yAccl'].as_matrix()
    z = final['zAccl'].as_matrix()

    xmean = np.mean(x)
    ymean = np.mean(y)
    zmean = np.mean(z)
    xstd = np.std(x)
    ystd = np.std(y)
    zstd = np.std(z)

    result = [xmean, ymean, zmean, xstd, ystd, zstd]

    return result

def smooth(data, type):
    time = data['time']
    mean = data.mean(axis=0)
    data = data.subtract(mean, axis = 1)
    data['time'] = time

    if type == 'accel':
        data['accel_x'] = data['accel_x'].rolling(window = 100).mean()
        data['accel_y'] = data['accel_y'].rolling(window=100).mean()
        data['accel_z'] = data['accel_z'].rolling(window=100).mean()
    else:
        data['gyro_x'] = data['gyro_x'].rolling(window=100).mean()
        data['gyro_y'] = data['gyro_y'].rolling(window=100).mean()
        data['gyro_z'] = data['gyro_z'].rolling(window=100).mean()
    return


def create_list(folderpath):
    pathlist = Path(folderpath).glob('**/*.txt')
    X = []
    Y = []
    for path in pathlist:
        path_in_str = str(path)
        data = load_file(path_in_str)
        data = smooth(data)
        if ("accel" in path_in_str):
            X.append(data)
        else:
            Y.append(data)

    return (X, Y)


if __name__ == '__main__':
    data = create_list('test_data/')
    accel = data[0]
    test = accel[3]
    x = test['accel_x']
    time = test['time']

    plt.plot(time, x)
    plt.show()
    gyro = data[1]
    # change the name of file of the formatted data here
    #x_file = open(r"X_test.txt", "w")
    #x_file.write(str(data[0]))
    # change the name of the file of the labels here
    #y_file = open(r"Y_train.txt", "w")
    #y_file.write(str(data[1]))

