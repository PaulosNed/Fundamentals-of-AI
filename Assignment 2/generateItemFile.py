import random
total=input("Total number of items: ")
size=input("Maximum size the sack can support: ")
filename = str(total) + "items.txt"
newFile=open(filename,"w")
newFile.write(size)
newFile.write("\n")
newFile.write("item,weight,value\n")
for i in range(int(total)):
    weight=random.uniform(1.0,20)
    weight = round(weight, 2)
    w = str(weight)
    value=random.choice(range(1,1000))
    v = str(value)
    l = "item" + str(i+1)
    final = l +"," + w + "," + v + "\n"
    newFile.write(final)
