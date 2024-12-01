# Since the format of the data is in excel, I am converting it to be usable for my purposes::
import pandas as pd
import numpy as np

# literal hard coded results
data = {
    "Year": [1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 
             2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 
             2018, 2019, 2020, 2021, 2022, 2023],
    "Amtrak": [510, 503, 491, 487, 498, 504, 516, 523, 524, 535, 540, 530, 542, 516, 508, 510, 515, 512, 515, 514, 
               529, 531, 510, 508, 510, 511, 512, 511, 512, 516, 518, 521, 525, 527, 526, 526, 526, 526, 528, 528],
    "Rail Transit": [1822, 1895, 1920, 2164, 2027, 2143, 2169, 2192, 2240, 2286, 2376, 2382, 2325, 2391, 2524, 2567, 
                     2595, 2621, 2784, 2679, 2909, 2946, 2985, 2997, 3027, 3101, 3124, 3165, 3216, 3227, 3355, 3301, 
                     3381, 3399, 3448, 3630, 3663, 3801, 3792, np.nan],
    "Commuter Rail": [np.nan] * 13 + [864, 972, 979, 983, 986, 1143, 1071, 1153, 1164, 1169, 1172, 1189, 1214, 1225, 
                                      1219, 1234, 1232, 1245, 1246, 1261, 1262, 1280, 1300, 1311, 1392, 1315, np.nan],
    "Heavy Rail": [np.nan] * 13 + [997, 997, 1004, 1009, 1019, 994, 1057, 1023, 1042, 1042, 1042, 1041, 1041, 1041, 
                                   1041, 1044, 1044, 1130, 1051, 1051, 1054, 1054, 1055, 1057, 1055, 1055, np.nan],
    "Light Rail": [np.nan] * 13 + [530, 555, 584, 603, 613, 640, 541, 723, 730, 764, 773, 787, 836, 848, 895, 928, 
                                   941, 969, 993, 1058, 1072, 1106, 1267, 1287, 1346, 1414, np.nan]
}
#Miss counted now checking
print(len(data["Year"]))
print(len(data["Amtrak"]))
print(len(data["Commuter Rail"]))
print(len(data["Heavy Rail"]))
print(len(data["Light Rail"]))
print(len(data["Rail Transit"]))


#convert to data frame
df = pd.DataFrame(data)

#save to csv
df.to_csv("Amtrak_Active_Railroads.csv", index=False)