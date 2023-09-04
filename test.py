import cv2
import numpy as np

# 读取图像
image = cv2.imread("./test.png")
ball_color = 'yellow'
color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              'yellow': {'Lower': np.array([11, 43, 46]), 'Upper': np.array([34, 255, 255])}
              }

gs_frame = cv2.GaussianBlur(image, (5, 5), 0)  # 高斯模糊
hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细
inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
mask = max(cnts, key=cv2.contourArea)
rect = cv2.minAreaRect(mask)
box = cv2.boxPoints(rect)
box = np.intp(box)

# 计算边界框的中心点坐标
center_x = int((box[0][0] + box[2][0]) / 2)
center_y = int((box[0][1] + box[2][1]) / 2)

# 随机生成20个点位
points = []
for _ in range(20):
    x = np.random.randint(center_x - 5, center_x + 5)
    y = np.random.randint(center_y - 5, center_y + 5)
    points.append((x, y))

# 计算20个点位的平均颜色值
avg_color = np.zeros(3)
for point in points:
    color = image[point[1], point[0]]
    avg_color += color[:3][::-1]
avg_color = tuple(map(int, avg_color / len(points)))


process_image('./test.png', 'yellow')
