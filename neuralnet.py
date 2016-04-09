__author__ = 'mushahidalam'
import sys
import re
import math
Attr_data = []
TrainDataSet = []
attributeCounter = 0


class Attribute():
    name = ''
    values = list()
    index = 0

    def __init__(self, str, values):
        global attributeCounter
        self.name = str
        self.values = values
        self.index = attributeCounter
        attributeCounter += 1
        self.values_count = {}
        for value in values:
            self.values_count[value] = [0, 0]


def InputParse(filename):
    global Attr_data
    global TrainDataSet

    try:
        finput = open(filename, 'r')
    except Exception as e:
        print "Error" + e
    # lines = [line.rstrip('\n') for line in finput]
    count = 1;
    for line in finput:
        line = line.rstrip('\n')
        if line.startswith('@attribute'):
            newlist = line.split(' ')
            if newlist[1] == "'Class'" or newlist[1] == 'Class' or newlist[1] == 'class' or newlist[1] == "'class'":
                values = re.findall(r'\{([^]]*)\}',line)
                values = values[0].split(',')
                values = [each.strip() for each in values]
                values = [each.strip("'") for each in values]
                newatr = Attribute(newlist[1], values)
                Attr_data.append(newatr)
                continue
            newlist = [each.strip() for each in newlist]
            newlist = [each.strip("'") for each in newlist]

            newatr = Attribute(newlist[1], newlist[2])
            Attr_data.append(newatr)
        if line.startswith('@attribute') or line.startswith('@relation') or line.startswith('%') or line.startswith(
                '@data'):
            continue
        else:
            line = line.strip()
            line = line.split(',')
            line = [each.strip() for each in line]
            line = [each.strip("'") for each in line]
            for k in range(len(line) - 1):
                line[k] = float(line[k])
            TrainDataSet.append(line)


class neural_net():
    learning_rate = 0
    biaz = 0
    weights = list()
    epochs = 0
    folds = 0
    folds_list = [[]]

    def __init__(self, fold, weight, learninrate, epoch):
        self.weights = [weight] * attributeCounter
        self.learning_rate = learninrate
        self.biaz = weight
        self.epochs = epoch
        self.folds = fold
        self.folds_list = [[] for i in range(fold)]

    def stratified_sampling(self):
        global TrainDataSet
        class1_list = list()
        class2_list = list()
        for instance in TrainDataSet:
            if instance[-1] == Attr_data[-1].values[0]:
                class1_list.append(instance)
            else:
                class2_list.append(instance)
        for i in range(len(class1_list)):
            self.folds_list[i%self.folds].append(class1_list.pop(0))
        for i in range(len(class2_list)):
            self.folds_list[i%self.folds].append(class2_list.pop(0))
        for i in range(0,len(self.folds_list)):
            print self.folds_list[i]
    def sigmod(self,ouput):
        return  1.0/(1.0+math.exp(ouput))

    def networkcompute(self, input_vector):
        result  = 0
        for i in range(len(self.weights)):
            result += self.weights[i] * input_vector[i]
        result += self.biaz
        return self.sigmod(result)

    def online_learning(self, input_vectors):


        output = neural_net



def main(args):
    if len(sys.argv) > 4:
        print "ERROR: Input format: neuralnet trainfile num_folds learning_rate num_epochs "
    # train_file = sys.argv[1]
    # folds = sys.argv[2]
    # learning_rate = sys.argv[3]
    # num_epochs = sys.argv[4]

    train_file = "sonar.arff"
    folds = 10
    learning_rate = 0.1
    num_epochs = 100
    InputParse(train_file)
    network = neural_net(folds, 0.1, learning_rate, num_epochs)
    network.stratified_sampling()
    network.online_learning()

main(None)

# if __name__=='__main__':
#     main(sys.argv)
