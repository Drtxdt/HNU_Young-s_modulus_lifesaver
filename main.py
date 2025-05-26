print("=========HNU杨氏模量试验数据拯救者===========")
print("==========================================")
print("输入的长度单位应为mm，质量单位应为g")

def get_valid_input(prompt, expected_length, check_positive=False, allow_zero=False):
    while True:
        line = input(prompt)
        try:
            nums = list(map(float, line.split()))
            if len(nums) != expected_length:
                print(f"错误：必须输入{expected_length}个数值，请重新输入。")
                continue
            if check_positive:
                if any(x < 0 for x in nums):
                    print("错误：数值不能为负数，请重新输入。")
                    continue
                if not allow_zero and any(x == 0 for x in nums):
                    print("错误：数值不能为零，请重新输入。")
                    continue
            return nums
        except ValueError:
            print("错误：输入包含非数值数据，请重新输入。")

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("错误：请输入一个正数。")
                continue
            return value
        except ValueError:
            print("错误：请输入有效的数值。")

# 获取竖直标尺读数（必须10个正数，不能有零）
nums1 = get_valid_input("请输入竖直标尺读数（用空格分隔，一共10个数据）: ", 10, check_positive=True, allow_zero=False)

# 获取水平标尺读数（必须10个数，允许零）
nums2 = get_valid_input("请输入水平标尺读数（用空格分隔，一共10个数据）: ", 10)

g = 9.7915

# 获取悬臂梁厚度（必须5个正数）
nums3 = get_valid_input("请输入悬臂梁厚度（用空格分隔，一共5个数据）: ", 5, check_positive=True, allow_zero=False)

# 计算厚度平均值和不确定度
d = sum(nums3) / 5
alpha_d = sum((d - num)**2 for num in nums3) / 5

# 获取其他参数
b = get_positive_float("请输入截面宽度b：")
a = get_positive_float("请输入砝码宽度a：")
l = get_positive_float("请输入悬臂长度L：")
m = get_positive_float("请输入砝码质量m：")

# 检查物理参数合理性
if l <= a / 2:
    print(f"错误：悬臂长度L ({l}mm) 必须大于砝码宽度a/2 ({a/2}mm)。")
    exit()

alpha_l = 0.3
alpha_b = 0.02
alpha_m = 0.06

# 计算比值表格
try:
    ratio1 = [nums2[i]/nums1[i] for i in range(10)]
except ZeroDivisionError:
    print("错误：竖直标尺读数包含零，请检查数据输入。")
    exit()

formatted_ratio1 = [f"{x:.4f}" for x in ratio1]
print("\n表格第三行为：")
print("  ".join(formatted_ratio1))

try:
    tan = float(formatted_ratio1[0])
    ratio2 = [(tan - float(r)) / (1 + tan * float(r)) for r in formatted_ratio1]
except (ValueError, ZeroDivisionError) as e:
    print(f"计算过程中发生错误：{str(e)}")
    exit()

formatted_ratio2 = [f"{x:.4f}" for x in ratio2]
print("\n表格第四行为：")
print("  ".join(formatted_ratio2))

import numpy as np

# 线性回归计算
y_values = [float(x) for x in formatted_ratio2]
x = np.arange(len(y_values))

try:
    slope, intercept = np.polyfit(x, y_values, 1)
except np.linalg.LinAlgError:
    print("错误：无法计算线性回归，数据可能存在奇异矩阵。")
    exit()

if abs(slope) < 1e-10:
    print("错误：拟合斜率过小，可能导致计算结果不准确。")
    exit()

residuals = y_values - (slope * x + intercept)
std_error = np.sqrt(np.sum(residuals**2) / (len(x) - 2))
mean_x = np.mean(x)
std_slope = std_error / np.sqrt(np.sum((x - mean_x)**2))

print(f"\n拟合斜率: {slope:.4f}")
print(f"斜率的标准误差: {std_slope:.4f}")

# 计算杨氏模量
try:
    E = (12 * m * 0.001 * g * (l * 0.001 - a * 0.001 / 2) ** 2) / (b * 0.001 * ((d * 0.001) ** 3) * slope)
except ZeroDivisionError:
    print("错误：计算过程中发生除零错误，请检查输入参数。")
    exit()

# 计算不确定度
try:
    temp = (alpha_m / m) ** 2 + (alpha_b / b) ** 2 + (3 * alpha_d / d) ** 2 
    temp += (std_slope / slope) ** 2 + (2 * alpha_l / (l - a / 2)) ** 2
    temp = np.sqrt(temp)
except ZeroDivisionError as e:
    print(f"不确定度计算错误：{str(e)}")
    exit()

alpha_E = temp * E
print("\n================================")
print("测量结果为：")
print(f"E = {E:.4f} ± {alpha_E:.4f} (Pa)")
print(f"相对不确定度 = {temp * 100:.4f}%")
print("================================")