import pandas as pd
import numpy as np

# 定义原始数据
dataFromExcel = pd.read_excel('C:\\Users\\IT\\Desktop\\awesome\\superToolMan\\dataafterETL.xlsx')

datas = np.array(dataFromExcel)

for data in datas:
    print(data)
    # dataMinFirst =[dataAll[0], dataAll[1], dataAll[7]]
    # dataMaxFirst =[dataAll[2], dataAll[3], dataAll[4], dataAll[5], dataAll[6]]

