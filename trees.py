import csv
import math
import operator	
import pprint
	
def read_data(filename):
	dataset=[]
	csvfile=open(filename,'rU')
	lines=csv.reader(csvfile)
	dataset=list(lines)
	return dataset	
	
def calculate_entropy_values(dataset):
	entropy=0
	class_list=[example[0] for example in dataset]
	unique_list=set(class_list)  
	count_ofclasses={}
	for class_name in class_list:
		if class_name not in count_ofclasses.keys():
			count_ofclasses[class_name]=0
		count_ofclasses[class_name]+=1
	for class_name in unique_list:
		prob=float(count_ofclasses[class_name])/len(dataset)
		entropy-=prob*math.log(prob,2)
	return entropy
	
def split_data_set(dataset,attribute,value):
	specific_attribute_dataset=[]
	for x in dataset:
		if x[attribute]==value:
			seperated_data_set=x[:attribute]
			seperated_data_set.extend(x[attribute+1:])
			specific_attribute_dataset.append(seperated_data_set)
	return specific_attribute_dataset
	
def best_attribute_tosplit(dataset):
	best_attribute=-1
	highest_IG=0.0
	baseEntropy=calculate_entropy_values(dataset)
	for x in range(1,len(dataset[0])):
		newentropy=0
		attribute_values=[example[x] for example in dataset]
		unique_av=set(attribute_values)
		for value in unique_av:
			splitted_data=split_data_set(dataset,x,value)
			prob=float(len(splitted_data))/len(dataset)
			newentropy+=prob*calculate_entropy_values(splitted_data)
		ig=baseEntropy-newentropy
		if ig>highest_IG:
			highest_IG=ig
			best_attribute=x
	return best_attribute	

	
def tree_algorithm(dataset,label):
	class_names=[example[0] for example in dataset]
	if class_names.count(class_names[0])==len(class_names):
		return class_names[0]
	best_attribute=best_attribute_tosplit(dataset)
	b_column=label[best_attribute]
	tree={b_column:{}}
	attribute_values=[example[best_attribute] for example in dataset]
	unique_av=set(attribute_values)
	for value in unique_av:
		splitted_data=split_data_set(dataset,best_attribute,value)
		reduced_classL=label[:]
		tree[b_column][value]=tree_algorithm(splitted_data,reduced_classL)
	return tree

def prediction(inst,tree):
     
	for nodes in tree.keys():  
		if(nodes=="cap_shape"):
			value=inst[0]
			#print(value)
		elif(nodes=="cap_surface"):
			value=inst[1]
		elif(nodes=="cap_color"):
			value=inst[2]
			#print(value)
		elif(nodes=="bruises"):
			value=inst[3]
			#print(value)
		elif(nodes=="ordor"):
			value=inst[4]
			#print(value)
		tree=tree[nodes][value]
		p=0			
		if type(tree) is dict:
			p=prediction(inst, tree)
		else:
			p=tree						
			return p
			
def accuracy(predicted,original_answers):
	count=0
	for i in range(len(predicted)):
		if(predicted[i]==original_answers[i]):
			count=count+1
	accuracy=count/len(predicted)*100
	return accuracy
	
	
def main():
	train_data_file=input("Input the trainingset data filename: ")
	test_data_file=input("Input the test data filename: ")
	trainingset=read_data(train_data_file)
	original_testset=read_data(test_data_file)
	test_data=[]
	test_set=[]
	for i in range(len(original_testset)):
		test_set.append(original_testset[i][0])
		temp=[]
		for j in range (1,len(original_testset[0])):
			temp.append(original_testset[i][j])
		test_data.append(temp)
	if(len(trainingset[0])==6):
		label=["class","cap_shape","cap_surface","cap_color","bruises","ordor"]
	else:
		label=["class","cap_shape","cap_surface","cap_color","bruises"]
	tree=tree_algorithm(trainingset,label)
	print("Generated decision tree:")
	pprint.pprint(tree)
	p=[]
	for i in range(len(test_data)):
		p.append(prediction(test_data[i],tree))
	print("Predicted values for the test set:")
	print(p)
	a=accuracy(p,test_set)
	print("accuracy:"+str(a)+"%")
main()