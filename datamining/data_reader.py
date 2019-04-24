import pandas as pd
import numpy


def read_data_attribute(filename):
    data = pd.read_csv(filename, header=None)
    df = pd.DataFrame(data)

    class_data, attr_cols = split_classifier(df)
    y = discretize(class_data, lambda i: 1 if i > 0 else 0)

    x = list()
    for index in attr_cols:
        median = attr_cols[index].median()
        x.append(discretize(attr_cols[index], lambda i: 1 if i >= median else 0))

    return x, y


def read_data_row(filename):
    x,y = read_data_attribute(filename)
    # here we get x as a list of lists where each inner list is values of a single attribute
    # for by row partitioning, we need to join them and then partition by row
    x_matrix = numpy.array(x)
    x_rows = x_matrix.reshape([len(x_matrix[0]), len(x_matrix)], order='F')
    return x_rows, y


def split_classifier(df):
    return df.iloc[:,-1], df.drop(df.columns[len(df.columns)-1], axis=1)


def discretize(column_data, threshold_func):
    f = lambda i: 1 if threshold_func(i) else 0
    return list(map(f, column_data))
