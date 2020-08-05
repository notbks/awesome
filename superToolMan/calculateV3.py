import numpy as np
import pandas as pd

# V3优化点：
# 1、输入方式变为自动读取excel
# 2、calculate函数应该有更优雅的写法。比如使用枚举替换if


#level是评价等级
#data是实际评分
def calculateMinFirst(level, data):

    s1 =20
    s2 =40
    s3 =60
    s4 =80
    s40 =60
    s5 = 100

    temp =0

    #等级为1时
    if (level ==1):
        #实际值各种取值情况
        if (data <= s1):
            return 1
        elif (s2>= data and data >s1 ):
            temp =2*(data -s1)
            return 1+(temp/(s1-s2))
        else:
            return -1

    #等级为2时
    if (level ==2):
        #实际值各种取值情况
        if (data >=s1 and data <= s2):
            return 1
        elif (data <s1 ):
            temp =2*(data -s1)
            return 1+(temp/s1)
        elif (data>=s2 and data <s3):
            temp =2*(data -s2)
            return 1+(temp/(s2-s3))
        else:
            return -1

    # 等级为3时
    if (level == 3):
        # 实际值各种取值情况
        if (data >= s2 and data <= s3):
            return 1
        elif (data > s1 and data <s2):
            temp = 2 * (data - s2)
            return 1 + (temp / (s2-s1))
        elif (data >= s3 and data < s4):
            temp = 2 * (data - s3)
            return 1 + (temp / (s3 - s4))
        else:
            return -1

    # 等级为4时
    if (level == 4):
        # 实际值各种取值情况
        if (data >= s3 and data <= s4):
            return 1
        elif (data > s2 and data <s3):
            temp = 2 * (data - s3)
            return 1 + (temp / (s3-s2))
        elif (data > s4):
            temp = 2 * (data - s4)
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return 1 - (temp / (s4 - s40))
        else:
            return -1

    #等级为5时
    if (level ==5):
        #实际值各种取值情况
        if (data >= s4 ):
            return 1
        elif (s4>= data and data >s3 ):
            temp =2*(data -s3)
            return 1+(temp/(s3-s4))
        else:
            return -1

def calculateMaxFirst(level, data):

    s0 = 100
    s1 = 80
    s2 = 60
    s3 = 40
    s4 = 20
    s5 = 0

    temp = 0

    # 等级为1时
    if (level == 1):
        # 实际值各种取值情况
        if (data >= s1):
            return 1
        elif (s1 > data and data >= s2):
            temp = 2 * (data - s1)
            return 1 + (temp / (s1 - s2))
        else:
            return -1

    # 等级为2时
    if (level == 2):
        # 实际值各种取值情况
        if (data >= s2 and data < s1):
            return 1
        elif (data > s1):
            temp = 2 * (data - s1)
            return 1 + (temp / (s1-s0))
        elif (data >= s3 and data < s2):
            temp = 2 * (data - s2)
            return 1 + (temp / (s2 - s3))
        else:
            return -1

    # 等级为3时
    if (level == 3):
        # 实际值各种取值情况
        if (data >= s3 and data <= s2):
            return 1
        elif (data > s2 and data <= s1):
            temp = 2 * (data - s2)
            return 1 + (temp / (s2 - s1))
        elif (data >= s4 and data < s3):
            temp = 2 * (data - s3)
            return 1 + (temp / (s3 - s4))
        else:
            return -1

    # 等级为4时
    if (level == 4):
        # 实际值各种取值情况
        if (data >= s4 and data <= s3):
            return 1
        elif (data > s3 and data <= s2):
            temp = 2 * (data - s3)
            return 1 + (temp / (s3 - s2))
        elif (data < s4):
            temp = 2*(data -s4)
            return 1 + (temp / (s4 -s5))
        else:
            return -1

    #等级为5时
    if (level ==5):
        #实际值各种取值情况
        if (data <= s4 ):
            return 1
        elif (s3>= data and data >s4 ):
            temp =2*(data -s3)
            return 1+(temp/(s3-s4))
        else:
            return -1

# 定义原始数据
dataFromExcel = pd.read_excel('C:\\Users\\IT\\Desktop\\awesome\\superToolMan\\dataafterETL.xlsx')
datas =np.array(dataFromExcel)
for dataAll in datas:
    print('行数据：')
    print(dataAll)

    dataMinFirst =[dataAll[0], dataAll[1], dataAll[7]]
    dataMaxFirst =[dataAll[2], dataAll[3], dataAll[4], dataAll[5], dataAll[6]]
    # print('原始数据')
    # print(dataAll)
    # print(dataMinFirst)
    # print(dataMaxFirst)
    # print()
    dictMin =np.zeros([3,5])
    dictMax =np.zeros([5,5])

    # i循环是二级指标的循环
    # i=1表示初始投资，是越小越优
    for i in range(0,3):
        # l循环是评价等级
        tempArr = []
        for l in range(1,6):
            tempArr.append(calculateMinFirst(l, dataMinFirst[i]))
        dictMin[i] =tempArr
    # print("越小越优：")
    # print('原始数据：')
    # print(dataMinFirst)
    # print(dictMin)

    for i in range(0,5):
        # l循环是评价等级
        tempArr = []
        for l in range(1,6):
            tempArr.append(calculateMaxFirst(l, dataMaxFirst[i]))
        dictMax[i] =tempArr
    # print("越大越优：")
    # print('原始数据：')
    # print(dataMaxFirst)
    # print(dictMax)

    print('终极矩阵：')
    resultArr =np.vstack((dictMin, dictMax))
    realResultArr = resultArr[[0,1,3,4,5,6,7,2]]
    print(realResultArr)





# 暂时不考虑
weightArr =[0.557,0.137,0.134,0.042,0.032,0.057,0.032,0.009]
tempWeightArr = np.tile(weightArr,[5,1])
weightArrs =np.array(tempWeightArr).T
# print('权重矩阵：')
# print(weightArrs)
# print()

finalArr =realResultArr*weightArrs
# print('最终结果矩阵：')
# print(finalArr)
# print()

print()
done =finalArr.max()
# print('最终结果矩阵的最大值：%f'% done)

level =np.where(finalArr ==done)
# print('等级为：%d' % (level[1][0] +1))