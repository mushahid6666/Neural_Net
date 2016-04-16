__author__ = 'mushahidalam'
import sys
import re
import math
import random
Attr_data = []
TrainDataSet = []
attributeCounter = 0
network = None

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
        self.weights = [weight] * (attributeCounter-1)
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
        # print("class1 = ",len(class1_list),"class2 = ",len(class1_list),self.folds)
        random.shuffle(class1_list)
        random.shuffle(class2_list)
        for i in range(len(class1_list)):
            # print(class1_list[0],i%self.folds)
            self.folds_list[i%self.folds].append(class1_list.pop(0))
        for i in range(len(class2_list)):
            # print(class2_list[0],i%self.folds)
            self.folds_list[i%self.folds].append(class2_list.pop(0))
        pass

        #Code to check the random shuffling
        # for i in range(0,len(self.folds_list)):
        #     rock_count = 0
        #     mine_count = 0
        #     for k in range(len(self.folds_list[i])):
        #         print self.folds_list[i][k]
        #         if self.folds_list[i][k][-1]=='Rock':
        #             rock_count+=1
        #         else:
        #             mine_count+=1
        #     print(rock_count,mine_count)


    def sigmod(self,output):
        return  1.0/(1.0+math.exp(-output))

    def networkcompute(self, input_vector):
        result  = 0
        for i in range(len(self.weights)):
            result += (self.weights[i]*1.0) * (input_vector[i]*1.0)
        result += self.biaz * 1.0
        return self.sigmod(result)

    def update_weights(self, vector, net_output, expected_output ):

        if expected_output == Attr_data[-1].values[0]:
            expected_output = float(0)
        else:
            expected_output = float(1)
        # print expected_output
        delta_j = net_output*(1-net_output)*(expected_output-net_output)
        for i in range(len(vector)-1):
            self.weights[i]+=self.learning_rate*delta_j*vector[i]
        self.biaz+=self.learning_rate*delta_j*1.0

    def online_learning(self):
        global network
        acc_data =[]
        #train for the number of epochs
        for i in range(len(self.folds_list)):
            random.shuffle(self.folds_list[i])
        for pass_count in range(self.folds-1,-1,-1):
            train_data = []
            test_data = []
            self.weights = [0.1] * (attributeCounter-1)
            self.biaz = 0.1

            for i in range(self.folds):
                if i!=pass_count:
                    for k in range(0,len(self.folds_list[i])):
                        train_data.append(self.folds_list[i][k])
                else:
                    for k in range(0,len(self.folds_list[i])):
                        test_data.append(self.folds_list[i][k])
            for m in range(self.epochs):
                random.shuffle(train_data)
                for vector in train_data:
                    net_output = network.networkcompute(vector)
                    network.update_weights(vector, net_output, vector[-1])
            correct = 0
            total =0
            for vector in test_data:
                total+=1
                confidence_of_prediction = network.networkcompute(vector)
                # print "%.12f"%net_output,
                if confidence_of_prediction < 0.5:
                    net_output = 'Rock'
                else:
                    net_output = 'Mine'
                if vector[-1]==net_output:
                    # print("correct expected",vector[-1],"predicted "+net_output)
                    correct+=1
                # print self.folds-pass_count,net_output,vector[-1],confidence_of_prediction
                # print "%s;%s" %(pass_count, net_output)
            accuracy = float(correct)/total
            # print("==========")
            print "accuracy =" ,accuracy
            acc_data.append(accuracy)
        average = 0
        for acc in acc_data:
            average+=acc
        average=average/self.folds
        print average






def main(args):
    if len(sys.argv) > 4:
        print "ERROR: Input format: neuralnet trainfile num_folds learning_rate num_epochs "
    # train_file = sys.argv[1]
    # folds = sys.argv[2]
    # learning_rate = sys.argv[3]
    # num_epochs = sys.argv[4]
    global network
    train_file = "sonar.arff"
    folds = 5
    learning_rate = 0.1
    num_epochs = 50

    InputParse(train_file)
    network = neural_net(folds, 0.1, learning_rate, num_epochs)
    network.stratified_sampling()
    network.online_learning()

main(None)

# if __name__=='__main__':
#     main(sys.argv)
