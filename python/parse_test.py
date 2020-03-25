import pandas as pd
import ast
from pathlib import Path

def load_file(filepath):
    with open(filepath, 'r') as f:
        d = f.read()
        data = ast.literal_eval(d)

    return pd.DataFrame(data)

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
    for path in pathlist:
        path_in_str = str(path)
        data = load_file(path_in_str)
        if "accel" in path_in_str:
            accel = data
        else:
            gyro= data
    final = pd.concat([accel, gyro['gyro_x'],
                      gyro['gyro_y'], gyro['gyro_z']], axis=1)
    final = smooth(final)
    start_time = final['time'].iloc[0]
    final['time'] = final['time'] - start_time
    final = final.dropna()

    return final


if __name__ == '__main__':
    data = create_list('../examples/test/')
    # change the name of file of the formatted data here
    data.to_csv(r'X_test.txt', index=False, header=False)



