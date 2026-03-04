from flask import Flask, request, jsonify
from torchvision import models
from image_transformations import preprocess
from PIL import Image
import torch
import io
import base64
import logging

# Initialize Flask app | 初始化 Flask 应用
app = Flask(__name__)

# Set up logging | 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load the MobileNetV3 Large pre-trained model | 加载 MobileNetV3 Large 预训练模型
try:
    logger.info("Loading MobileNetV3 Large pre-trained model...")
    model = models.mobilenet_v3_large(weights=models.MobileNet_V3_Large_Weights.DEFAULT)
    model.eval()  # Set model to evaluation mode | 将模型设置为评估模式
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise RuntimeError("Failed to load the model.") from e

# Health endpoint | 健康检查端点
@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint to confirm the app is running.
    健康检查端点以确认应用正在运行。
    """
    response = {'status': 'healthy'}
    logger.info(f"Response for /health: {response}")
    return jsonify(response), 200

# Prediction endpoint | 预测端点
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract Base64 string from request JSON | 从请求 JSON 中提取 Base64 字符串
        data = request.json
        if 'image' not in data:
            logger.warning("No image provided in the request.")
            response = {'error': 'No image provided'}
            logger.info(f"Response for /predict: {response}")
            
            return jsonify(response), 400
        
        # Decode the Base64 image string | 解码 Base64 图像字符串
        image_data = base64.b64decode(data['image'])
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Preprocess the image | 预处理图像
        transformed_img = preprocess(image).unsqueeze(0)
        
        # Perform inference | 执行推理
        with torch.no_grad():
            logger.info("Performing inference...")
            output = model(transformed_img)
            _, predicted = torch.max(output.data, 1)
            logger.info(f"Inference complete. Predicted class: {predicted.item()}")
        
        # Return our prediction | 返回我们的预测
        response = {'prediction': predicted.item()}
        logger.info(f"Response for /predict: {response}")
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        response = {'error': str(e)}
        logger.info(f"Response for /predict: {response}")
        
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True)
