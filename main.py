import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# 读取CSV文件
file_path = 'LT1NL.csv' 
data = pd.read_csv(file_path)

detector_top=3.434
LT_1_range=(3.35182-0.365091)
LT_1_min=0.365091
correction_factor=1995/1977

# 提取数据列
calibration_distance = np.array(data['calibration distance'])
calibration_LT1 =  np.array(data['calibration LT-1'])
detector_draining_LT1 =  np.array(data['detector draining LT-1'])
detector_draining_height =  np.array(data['detector draining height'])
detector_filling_LT1 =  np.array(data['detector filling LT-1'])
detector_filling_height = np.array( data['detector filling height'])

drain_cal_dis = np.array(data['draining cal dis'])
drain_cal_cur = np.array(data['draining cal cur'])

fill_cal_dis = np.array(data['filling cal dis'])
fill_cal_cur = np.array(data['filling cal cur'])

ini_PT5=np.array(data['initial filling PT5'])
ini_LT1=(0.9948*np.array(data['initial filling LT1'])-1.1699+1.191)/1.004444468

draining_ADC = ((detector_draining_LT1-LT_1_min)/(LT_1_range)*2000)*correction_factor
filling_ADC = ((detector_filling_LT1-LT_1_min)/(LT_1_range)*2000)*correction_factor
ini_ADC = ((ini_LT1-LT_1_min)/(LT_1_range)*2000)*correction_factor


corrected_detector_draining_LT1 = np.convolve((draining_ADC/2000)*(LT_1_range)+LT_1_min, np.ones(21)/21, mode='valid')
corrected_detector_filling_LT1 = np.convolve((filling_ADC/2000)*(LT_1_range)+LT_1_min, np.ones(21)/21, mode='valid')
corrected_ini_LT1 = np.convolve((ini_ADC/2000)*(LT_1_range)+LT_1_min, np.ones(21)/21, mode='valid')
corrected_ini_PT5 = np.convolve(((ini_PT5+0.0524)*correction_factor)-0.0524, np.ones(21)/21, mode='valid')

new_cal_height_trans=detector_top-(185.5-np.array(data['new cal coordi']))/100
new_cal_LT1_trans =(np.array(data['new cal LT1'])+1.1546)/0.9952+detector_top-3


# plt.plot(detector_draining_LT1,label="LT-1 level(m)")
# plt.plot(detector_draining_height,label="UT-1 depth(m)")
# plt.xlabel('seconds since start time')
# plt.ylabel('Values')
# plt.ylim(3.1,3.4)
# plt.legend()
# plt.show()

# plt.plot(detector_filling_LT1,label="LT-1 level(m)")
# plt.plot(detector_filling_height,label="UT-1 depth(m)")
# plt.xlabel('seconds since start time')
# plt.ylabel('Values')
# plt.ylim(3.1,3.4)
# plt.legend()
# plt.show()



print(np.nanmax(drain_cal_cur,),np.nanmax(fill_cal_cur))


# 创建图形
plt.figure(figsize=(12, 8))



#绘制calibration数据
plt.plot(detector_top-calibration_LT1/100,detector_top-calibration_distance/100,  label='3m calibration', color='b', marker='o')
plt.plot(detector_top-(0.416-drain_cal_cur/20*0.316),detector_top-drain_cal_dis/100, label='31.6cm draining calibration translated', color='SkyBlue', marker='v')
plt.plot(detector_top-(0.416-fill_cal_cur/20*0.316),detector_top-fill_cal_dis/100,  label='31.6cm filling calibration translated', color='SkyBlue', marker='^')
plt.plot(new_cal_LT1_trans,new_cal_height_trans,label='30cm draining calibration translated', color='purple', marker='x')

# 绘制detector draining数据
plt.plot(detector_draining_LT1, detector_draining_height, label='Detector Draining(height refering to UT1)', color='lightcoral')
plt.plot(corrected_detector_draining_LT1, detector_draining_height[10:-10], label='Detector Draining corrected(height refering to UT1)', color='r')
# 绘制detector filling数据
plt.plot(detector_filling_LT1, detector_filling_height, label='Detector Filling(height refering to UT1)', color='lightgreen')
plt.plot(corrected_detector_filling_LT1, detector_filling_height[10:-10], label='Detector Filling corrected(height refering to UT1)', color='g')

plt.plot(ini_LT1,ini_PT5,label='initial Filling (height refering to PT5)', color='gray')
plt.plot(corrected_ini_LT1,corrected_ini_PT5,label='initial Filling corrected(height refering to corrected PT5)', color='black')


# 添加图例和标签
plt.xlabel('LT-1 measurement/m')
plt.ylabel('Height/m')
plt.title('Calibration, Detector Draining, and Detector Filling Measurements')
plt.legend()
plt.grid(True)
plt.xlim(3.275,3.36)
plt.ylim(3.24,3.36)
# 显示图形
plt.show()