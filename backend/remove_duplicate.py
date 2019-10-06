import csv

with open("originalinfo.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    column1 = [row[0] for row in reader]
    # print(column1)
    set1 = set(column1)
    # print(column1[0] in set1)
    # print(set1)
    print(len(set1))
with open("originalinfo.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    data = []  # 创建列表准备接收csv各行数据
    # data = [row for row in reader]
    for one_line in reader:
        data.append(one_line)
    #print(data)
    i = 1
    file = open("originalinfo_new.csv", "a")
    writer = csv.writer(file)
    for i in range(len(data)):
        #print(data[i][0])
        if data[i][0] in set1:
            set1.remove(data[i][0])
            writer.writerow(data[i])





