from test import process_image

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/process_image', methods=['POST'])
def api_process_image():
    print(request)
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'})

    image = request.files['image']
    ball_color = request.form.get('ball_color', 'yellow')

    # 保存图像到临时文件
    image_path = '/tmp/image.jpg'
    image.save(image_path)

    # 调用方法并获取平均颜色值
    avg_color = process_image(image_path, ball_color)

    # 返回平均颜色值
    return jsonify({'avg_color': avg_color})


if __name__ == '__main__':
    app.run()
