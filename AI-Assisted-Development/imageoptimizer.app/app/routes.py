# 导入必要的库 / Import necessary libraries
import logging  # 日志记录 / Logging
from flask import Blueprint, request, jsonify, send_file  # Flask核心组件 / Flask core components
import cv2  # OpenCV图像处理库 / OpenCV for image processing
import numpy as np  # NumPy数组处理 / NumPy for array operations
import io  # 字节流处理 / BytesIO stream handling
from werkzeug.utils import secure_filename  # 文件名安全处理 / Secure filename handling
from PIL import Image  # Pillow图像验证 / Pillow for image validation

# 配置日志系统 / Set up logging system
# level=logging.INFO 表示记录INFO级别及以上的日志
# This will record INFO level and above logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建蓝图(Blueprint)用于组织路由 / Create Blueprint to organize routes
# 蓝图是Flask中模块化应用的方式 / Blueprint is Flask's way to modularize applications
bp = Blueprint('main', __name__)

# ==================== 图片上传和优化接口 / Image Upload and Optimization API ====================
@bp.route('/upload', methods=['POST'])  # 定义路由，只接受POST请求 / Define route, accept POST only
def upload():
    """
    处理图片上传请求的主函数 / Main function to handle image upload requests
    
    功能流程 / Function workflow:
    1. 验证请求中是否包含图片文件 / Validate if image file is in request
    2. 检查文件扩展名和实际内容 / Check file extension and actual content
    3. 获取压缩质量参数 / Get quality parameter
    4. 使用OpenCV处理图片 / Process image with OpenCV
    5. 返回处理后的图片二进制数据 / Return processed image as binary data
    
    参数 / Parameters:
        request: Flask请求对象，包含图片文件和质量参数 / Flask request object with image and quality
    
    返回 / Returns:
        send_file: 成功时返回处理后的图片二进制数据 / Processed image binary on success
        jsonify: 失败时返回JSON格式的错误信息 / JSON error message on failure
    """
    try:  # 异常捕获，处理所有可能的错误 / Exception handling for all possible errors
        # ========== 步骤1: 验证请求中是否包含图片 / Step 1: Validate if image exists in request ==========
        if 'image' not in request.files:
            # 如果请求的files字典中没有'image'键，说明没有上传图片
            # If 'image' key is not in request.files, no image was uploaded
            logger.error('No image part in the request')  # 记录错误日志 / Log error
            return jsonify({'error': 'No image part in the request'}), 400  # 返回400错误 / Return 400 error

        image = request.files['image']  # 从请求中获取图片文件对象 / Get image file object from request

        # 检查是否选择了文件（文件名为空表示未选择）/ Check if a file was selected (empty filename means no file)
        if image.filename == '':
            logger.error('No image selected for uploading')
            return jsonify({'error': 'No image selected for uploading'}), 400

        # ========== 步骤2: 文件名安全处理和内容读取 / Step 2: Secure filename and read content ==========
        # 使用secure_filename()防止文件名注入攻击（仅用于日志记录）
        # Use secure_filename() to prevent filename injection attacks (for logging only)
        filename = secure_filename(image.filename)

        # 读取图片的二进制内容到内存 / Read image binary content into memory
        image_content = image.read()
        image.seek(0)  # 重置文件指针到开头，以便后续重新读取 / Reset file pointer for re-reading
        
        # ========== 步骤3: 使用Pillow验证图片真实性 / Step 3: Validate image authenticity with Pillow ==========
        try:
            # 用Pillow打开图片，这会解析图片头部信息 / Open image with Pillow to parse header
            img = Image.open(io.BytesIO(image_content))
            img.verify()  # 验证这确实是一个有效的图片文件 / Verify this is a valid image file
            
            # 根据图片实际解码出的格式验证（而不是文件扩展名）
            # Validate by actual decoded format (not filename extension)
            # 只接受PNG、JPEG、WEBP三种格式 / Accept only PNG, JPEG, WEBP formats
            if (img.format or '').lower() not in {'png', 'jpeg', 'webp'}:
                logger.error('Invalid image format for: %s', filename)
                return jsonify({'error': 'Invalid image format. Only PNG, JPEG and WEBP are supported.'}), 400
                
        except (IOError, SyntaxError) as e:
            # 捕获图片解析错误（文件损坏或非图片文件）/ Catch image parsing errors (corrupted or non-image)
            logger.error('Invalid image file: %s', e)
            return jsonify({'error': 'Invalid image file'}), 400
        
        # 再次重置文件指针，为OpenCV读取做准备 / Reset file pointer again for OpenCV reading
        image.seek(0)

        # ========== 步骤4: 获取和验证质量参数 / Step 4: Get and validate quality parameter ==========
        # 检查表单数据中是否包含quality参数 / Check if quality parameter exists in form data
        if 'quality' not in request.form:
            logger.error('Quality parameter is missing')
            return jsonify({'error': 'Quality parameter is required'}), 400

        # 从表单中获取quality参数并转换为整数 / Get quality from form and convert to integer
        quality = request.form.get('quality', type=int)
        
        # 验证quality必须是0-100之间的整数 / Validate quality must be integer between 0-100
        # 0表示最低质量（最小文件），100表示最高质量（最大文件）
        # 0 = lowest quality (smallest file), 100 = highest quality (largest file)
        if quality is None or quality < 0 or quality > 100:
            logger.error('Invalid quality value: %s', quality)
            return jsonify({'error': 'Quality must be an integer between 0 and 100'}), 400

        # ========== 步骤5: 使用OpenCV解码图片 / Step 5: Decode image with OpenCV ==========
        # 将图片二进制数据转换为NumPy数组 / Convert image binary to NumPy array
        img_array = np.frombuffer(image.read(), np.uint8)
        
        # 使用OpenCV解码图片数组为图像矩阵 / Decode image array to image matrix with OpenCV
        # cv2.IMREAD_UNCHANGED: 保持原始图片的所有通道（包括透明度）
        # cv2.IMREAD_UNCHANGED: Keep all original channels (including alpha transparency)
        img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)

        if img is None:
            # 解码失败，可能是图片格式不支持或文件损坏 / Decode failed, unsupported format or corrupted
            logger.error('Failed to decode image: %s', filename)
            return jsonify({'error': 'Failed to decode image'}), 400

        # ========== 步骤6: 使用OpenCV压缩图片 / Step 6: Compress image with OpenCV ==========
        # cv2.imencode()将图片编码为JPEG格式并压缩 / Encode image to JPEG format with compression
        # 参数说明 / Parameters:
        #   '.jpg': 输出格式为JPEG / Output format is JPEG
        #   img: 要编码的图片矩阵 / Image matrix to encode
        #   [cv2.IMWRITE_JPEG_QUALITY, quality]: JPEG压缩质量参数 / JPEG compression quality
        _, buffer = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])

        # 将压缩后的图片buffer转换为字节流对象 / Convert compressed buffer to BytesIO object
        img_io = io.BytesIO(buffer)

        # ========== 步骤7: 验证处理后的图片 / Step 7: Validate processed image ==========
        try:
            # 用Pillow再次验证处理后的图片是否有效 / Re-validate processed image with Pillow
            processed_img = Image.open(img_io)
            processed_img.verify()
        except (IOError, SyntaxError) as e:
            # 如果处理后的图片无效，返回错误 / Return error if processed image is invalid
            logger.error('Failed to process image: %s', e)
            return jsonify({'error': 'Failed to process image'}), 400

        # 重置BytesIO对象的指针到开头，准备发送 / Reset BytesIO pointer to beginning for sending
        img_io.seek(0)

        # ========== 步骤8: 返回处理后的图片 / Step 8: Return processed image ==========
        # send_file()将图片作为HTTP响应发送给客户端 / send_file() sends image as HTTP response to client
        # mimetype='image/jpeg': 设置响应的内容类型为JPEG图片 / Set response content type to JPEG
        return send_file(img_io, mimetype='image/jpeg')

    except Exception as e:
        # ========== 异常处理 / Exception Handling ==========
        # 捕获所有未预期的异常，防止服务器崩溃 / Catch all unexpected exceptions to prevent server crash
        # logger.exception()会自动记录完整的堆栈跟踪信息 / logger.exception() logs full stack trace
        logger.exception('An unexpected error occurred: %s', e)
        # 返回500服务器内部错误 / Return 500 Internal Server Error
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500
