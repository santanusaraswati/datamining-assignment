from math import log
from info_gain import info_gain as ig
from os import listdir
from datamining.data_reader import read_data_attribute

# information gain using pypi package
from datamining.excel_writer import write_excel


def gain(classifier, attribute):
    return ig.info_gain(classifier, attribute)


def entropy(pj):
    total_entropy = 0
    for p in pj:
        if p != 0:
            p = p / sum(pj)
            total_entropy += -1 * p * log(p, 2)
        else:
            total_entropy += 0
    return total_entropy


def calc_gain(class_count, attr_count):
    total = 0
    for v in attr_count:
        print(entropy(v))
        total += sum(v) / sum(class_count) * entropy(v)
    print(entropy(class_count))
    return entropy(class_count) - total


def main():
    data_dir = "/home/santanu/study/mtech/semester2/Data Mining/data/"
    output_dir = "/home/santanu/study/mtech/semester2/Data Mining/"
    info_gains = []
    files = sorted(listdir(data_dir), key=lambda name: int(name.split('.')[0]))
    for i, file in enumerate(files):
        x, y = read_data_attribute(data_dir + file)
        # using pre-built function
        # for attr in x:
        #    print(gain(y, attr))

        #print(x[0])
        #print(y)
        # using custom implementation
        # first the count on 0 and 1 in classification
        class0_count = y.count(0)
        class1_count = y.count(1)
        info_gain = list()
        for attr in x:
            '''
            two cases here
            number of times y is 0 and y is 1 given x 0
            number of times y is 0 and y is 1 given x 1
            '''
            class0 = [y[i] for i, item in enumerate(attr) if item == 0]
            class1 = [y[i] for i, item in enumerate(attr) if item == 1]
            # given x = 0, how many y = 0
            class00_count = class0.count(0)
            # given x = 0, how many y = 1
            class01_count = class0.count(1)
            # given x = 1, how many y = 0
            class10_count = class1.count(0)
            # given x = 1, how many y = 1
            class11_count = class1.count(1)

            # print(class0)
            # print(class1)
            # print(class00_count, class01_count)
            # print(class10_count, class11_count)
            info_gain.append(calc_gain([class0_count, class1_count],
                                       [[class00_count, class01_count], [class10_count, class11_count]]))
        # adding the file name for nicer excel
        info_gain.insert(0, file)
        info_gains.append(info_gain)

    for info_gain in info_gains:
        print(info_gain)
    write_excel(output_dir + "InfoGain.xlsx", "Information Gain", [], info_gains)


if __name__ == '__main__':
    main()
