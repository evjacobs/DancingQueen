import pandas as pd
import numpy as np
import itertools
from sklearn import linear_model
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC

from sklearn.model_selection import GridSearchCV


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def load_file(filepath):
    data = pd.read_csv(filepath)
    return data


def log_reg(X_train, Y_train, X_test):
    parameters = {'C':[0.01, 0.1, 1, 10, 20, 30], 'penalty':['l2','l1']}
    log_reg_grid = GridSearchCV(linear_model.LogisticRegression(), param_grid=parameters,
                                cv=3, verbose=1, n_jobs=-1)
    log_reg_grid.fit(X_train, Y_train.values.ravel())
    y_pred = log_reg_grid.predict(X_test)
    return y_pred

def lin_svc(X_train, Y_train, X_test):
    parameters = {'C':[0.125, 0.5, 1, 2, 8, 16]}
    lr_svc_grid = GridSearchCV(LinearSVC(tol=0.00005), param_grid=parameters, n_jobs=-1, verbose=1)
    lr_svc_grid.fit(X_train, Y_train.values.ravel())
    y_pred = lr_svc_grid.predict(X_test)
    return y_pred


if __name__ == '__main__':
    X_train = load_file('X_train.txt')
    Y_train = load_file('Y_train.txt')
    Y_train['1'] = Y_train['1'].astype(str)
    X_test = load_file('X_test.txt')
    Y_test = load_file('Y_test.txt')
    Y_test = Y_test.values.astype(str)


    class_labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']

    prediction = lin_svc(X_train, Y_train, X_test)
    accuracy = metrics.accuracy_score(y_true=Y_test, y_pred=prediction)
    print('---------------------')
    print('|      Accuracy      |')
    print('---------------------')
    print('\n    {}\n\n'.format(accuracy))

    cm = metrics.confusion_matrix(Y_test, prediction)
    plt.figure(figsize=(8,8))
    plt.grid(b=False)
    plot_confusion_matrix(cm, classes=class_labels, normalize=True, title='Normalized confusion matrix')
    plt.show()
