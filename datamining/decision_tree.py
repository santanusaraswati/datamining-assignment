from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from os import listdir

from datamining.data_reader import read_data_row
from datamining.excel_writer import write_excel


def train(x_train, y_train):
    decision_tree = DecisionTreeClassifier(criterion="entropy", random_state=70)
    decision_tree.fit(x_train, y_train)
    return decision_tree


def split_data(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=100)
    return x_train, x_test, y_train, y_test


def validate_decision_tree(decision_tree, x_test, y_test):
    y_est = predict(decision_tree, x_test)
    # print(y_est, y_test)
    tn, fp, fn, tp = confusion_matrix(y_test, y_est).ravel()

    accuracy = (tn+tp)/(tn+tp+fn+fp)
    fmeasure = (2*tp)/((2*tp)+fp+fn)
    return accuracy,fmeasure


def predict(decision_tree, x_test):
    y_est = decision_tree.predict(x_test)
    return y_est


def main():
    data_dir = "/home/santanu/study/mtech/semester2/Data Mining/data/"
    output_dir = "/home/santanu/study/mtech/semester2/Data Mining/"
    validation_results = []
    files = sorted(listdir(data_dir), key=lambda name: int(name.split('.')[0]))
    for i, file in enumerate(files):
        x,y = read_data_row(data_dir + file)
        x_train, x_test, y_train, y_test = split_data(x, y)
        decision_tree = train(x_train, y_train)
        validation_result = list(validate_decision_tree(decision_tree, x_test, y_test))
        # adding the file name for nicer excel
        validation_result.insert(0, file)
        validation_results.append(validation_result)

    for validation_result in validation_results:
        print(validation_result)
    write_excel(output_dir + "DecisionTree.xlsx", "Decision Tree", ["File Name", "Accuracy", "F-Measure"], validation_results)


if __name__ == '__main__':
    main()