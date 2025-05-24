print("=========HNU杨氏模量试验数据拯救者===========")
print("==========================================")
print("输入的长度单位应为mm，质量单位应为g")
line1 = input("请输入竖直标尺读数（用空格分隔，一共10个数据）: ")
nums1 = list(map(float, line1.split())) # 竖直标尺读数

line2 = input("请输入水平标尺读数（用空格分隔，一共10个数据）: ")
nums2 = list(map(float, line2.split())) # 水平标尺读数

g = 9.7915

line3 = input("请输入悬臂梁厚度（用空格分隔，一共5个数据）: ")
nums3 = list(map(float, line3.split())) # 悬臂梁厚度

d = 0
for num in nums3:
    d += num
d = d / 5
alpha_d = 0
for num in nums3:
    alpha_d += (d - num) ** 2
alpha_d = alpha_d / 5

b = float(input("请输入截面宽度b："))
a = float(input("请输入砝码宽度a："))
l = float(input("请输入悬臂长度L："))
m = float(input("请输入砝码质量m："))

alpha_l = 0.3
alpha_b = 0.02
alpha_m = 0.06

ratio1 = [nums2[i]/nums1[i] for i in range(len(nums1))]
formatted_ratio1 = [f"{x:.4f}" for x in ratio1]

print("\n表格第三行为：")
print("  ".join(formatted_ratio1))

tan = float(formatted_ratio1[0])
ratio2 = [(tan - float(formatted_ratio1[i])) / (1 + tan * float(formatted_ratio1[i])) for i in range(len(formatted_ratio1))]
formatted_ratio2 = [f"{x:.4f}" for x in ratio2]

print("\n表格第四行为：")
print("  ".join(formatted_ratio2))

import numpy as np

y_values = [float(x) for x in formatted_ratio2]
x = np.arange(len(y_values))

slope, intercept = np.polyfit(x, y_values, 1)
residuals = y_values - (slope * x + intercept)
std_error = np.sqrt(np.sum(residuals**2) / (len(x) - 2))
mean_x = np.mean(x)
std_slope = std_error / np.sqrt(np.sum((x - mean_x)**2))

print(f"\n拟合斜率: {slope:.4f}")
print(f"斜率的标准误差: {std_slope:.4f}")
# print(f"剩余标准差: {std_error:.4f}")

E = (12 * m * 0.001 * g * (l * 0.001 - a * 0.001 / 2) ** 2) / (b * 0.001 * ((d * 0.001) ** 3) * slope)
print(f"\nE的值为: {E:.4f}")

temp = (alpha_m / m) ** 2 + (alpha_b / b) ** 2 + (3 * alpha_d / d) ** 2 + (std_slope / slope) ** 2 + (2 * alpha_l / (l - a / 2)) ** 2
temp = temp ** 0.5
print(f"相对不确定度为: {temp:.4f}")

alpha_E = temp * E
print(f"不确定度为: {alpha_E:.4f}")
print("================================")
print("测量结果为：")
print(f"E={E:.4f} +- {alpha_E:.4f}")
print(f"E_k = {temp * 100:.4f}%")