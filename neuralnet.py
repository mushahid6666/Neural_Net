__author__ = 'mushahidalam'
import sys
import re
Attr_data=[]
TrainDataSet=[]

class Attribute():
    name=''
    values=list()
    index=0
    def __init__(self,str,values):
        global attributeCounter
        self.name=str
        self.values=values
        self.index=attributeCounter
        attributeCounter+=1
        self.values_count = {}
        for value in values:
            self.values_count[value]=[0,0]

def InputPares(filename):
    global Attr_data
    global TrainDataSet

    try:
        finput= open(filename,'r')
    except Exception as e:
        print "Error"+e
    # lines = [line.rstrip('\n') for line in finput]
    count = 1;
    for line in finput:
        line=line.rstrip('\n')
        if line.startswith('@attribute'):
            templist =  line.split(' ')
            values = re.findall(r'\{([^]]*)\}',line)
            newlist=values[0].split(",")
            newlist = [each.strip() for each in newlist]
            newlist = [each.strip("'") for each in newlist]
            # templist[1]=templist[1].replace('\\','').replace("'",'')
            templist[1]=templist[1].strip()
            newatr = Attribute(templist[1],newlist)
            Attr_data.append(newatr)
        if line.startswith('@attribute') or line.startswith('@relation') or line.startswith('%') or line.startswith('@data'):
            continue
        else:
            line=line.strip()
            line= line.split(',')
            line = [each.strip() for each in line]
            line = [each.strip("'") for each in line]
            TrainDataSet.append(line)
            if line[-1]==Attr_data[-1].values[0]:
                for i in range(len(line)):
                    Attr_data[i].values_count[line[i]][0]+=1
            else:
                for i in range(len(line)):
                    Attr_data[i].values_count[line[i]][1]+=1

def main(args):
    if len(sys.argv) > 4:
        print "ERROR: Input format: neuralnet trainfile num_folds learning_rate num_epochs "
    train_file = sys.argv[1]
    folds = sys.argv[2]
    learning_rate = sys.argv[3]
    num_epochs = sys.argv[4]
    InputPares(train_file)
    print Attr_data
    # print(TrainDataSet)


# if __name__=='__main__':
#     main(sys.argv)
