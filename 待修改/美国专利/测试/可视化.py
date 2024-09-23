# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# 示例数据
x = list(range(1, 11))
print(x)

y = [50, 50, 50, 50, 50, 5, 50, 50, 50, 2]

# 创建折线图
plt.plot(x, y, marker='o', linestyle='--', color='#b83b5e')

# 去掉上边框和右边框
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.title('500次连续采集成功次数', fontsize=14)
plt.xlabel('序号', fontsize=12)
plt.ylabel('成功次数（50）', fontsize=12)


# 显示图形
plt.show()
