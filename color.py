import cv2
import numpy as np


def main(image_path):
    # 读取图像
    image = cv2.imread(image_path)
    ball_color = ['yellow', 'pink']  # 需要识别的颜色 支持多个颜色
    color_dist = {
        'pink': {'Lower': np.array([150, 43, 46]), 'Upper': np.array([175, 255, 255])},
        'yellow': {'Lower': np.array([21, 43, 46]), 'Upper': np.array([34, 255, 255])},
        'purple': {'Lower': np.array([125, 43, 46]), 'Upper': np.array([155, 255, 255])}
    }

    gs_frame = cv2.GaussianBlur(image, (5, 5), 0)  # 高斯模糊
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
    erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细
    colorArr = []
    for colorValue in ball_color:
        inRange_hsv = cv2.inRange(erode_hsv, color_dist[colorValue]['Lower'], color_dist[colorValue]['Upper'])
        c = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        colorArr += c
    mask = max(colorArr, key=cv2.contourArea)
    rect = cv2.minAreaRect(mask)
    box = cv2.boxPoints(rect)
    box = np.intp(box)

    # 计算边界框的中心点坐标
    center_x = int((box[0][0] + box[2][0]) / 2)
    center_y = int((box[0][1] + box[2][1]) / 2)

    # 随机生成20个点位
    points = []
    for _ in range(20):
        x = np.random.randint(center_x - 8, center_x + 8)
        y = np.random.randint(center_y - 8, center_y + 8)
        points.append((x, y))

    # 计算20个点位的平均颜色值
    avg_color = np.zeros(3)
    for point in points:
        color = hsv[point[1], point[0]]
        avg_color += color
    avg_color = tuple(map(int, avg_color / len(points)))

    # 打印平均颜色值
    print("平均颜色值：", avg_color)

    # 判断平均颜色值接近黄色还是接近紫色
    yellow_dist = np.linalg.norm(avg_color - color_dist['yellow']['Lower'])
    purple_dist = np.linalg.norm(avg_color - color_dist['purple']['Lower'])

    # 接口应在这里返回结果
    if yellow_dist < purple_dist:
        print("平均颜色值接近黄色----阴性")
        # return '阴性'
    else:
        print("平均颜色值接近紫色----阳性")
        # return '阳性'
    # 绘制矩形和随机点位
    cv2.drawContours(image, [np.intp(box)], -1, (0, 255, 255), 2)
    for point in points:
        cv2.circle(image, point, 3, (0, 0, 255), -1)

    # 显示图像
    cv2.namedWindow("img", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.imshow('img', image)
    # cv2.imshow('img', inRange_hsv)
    cv2.waitKey(0)


if __name__ == '__main__':
    main("./t2.jpg")
