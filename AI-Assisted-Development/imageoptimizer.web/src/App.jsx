// 导入React核心Hooks / Import React core Hooks
// useState: 用于管理组件状态 / For managing component state
// useEffect: 用于处理副作用（如清理内存）/ For handling side effects (like memory cleanup)
import { useState, useEffect } from 'react'
import './App.css'  // 导入样式文件 / Import CSS styles


/**
 * 图片优化器主应用组件 / Main application component for image optimization
 * 
 * 功能说明 / Features:
 * 1. 图片选择和验证 / Image selection and validation
 * 2. 质量调整（0-100）/ Quality adjustment (0-100)
 * 3. 图片优化处理 / Image optimization processing
 * 4. 原图与优化图对比显示 / Display comparison of original and optimized images
 * 5. 文件大小和压缩率计算 / File size and compression ratio calculation
 *
 * @returns {JSX.Element} 渲染的应用组件 / The rendered application component
 */
function App() {
  // ==================== 状态管理 / State Management ====================
  // useState是React Hook，用于在函数组件中添加状态
  // useState is a React Hook for adding state to functional components
  
  // 选中的图片文件对象 / Selected image file object
  const [selectedImage, setSelectedImage] = useState(null);
  
  // 选中图片的预览URL（用于显示）/ Preview URL of selected image (for display)
  const [selectedImageUrl, setSelectedImageUrl] = useState(null);
  
  // 选中图片的文件大小（字节）/ File size of selected image (in bytes)
  const [selectedImageSize, setSelectedImageSize] = useState(null);
  
  // 压缩质量参数（0-100），默认80 / Compression quality (0-100), default 80
  const [quality, setQuality] = useState(80);
  
  // 优化后图片的预览URL / Preview URL of optimized image
  const [optimizedImageUrl, setOptimizedImageUrl] = useState(null);
  
  // 优化后图片的文件大小 / File size of optimized image
  const [optimizedImageSize, setOptimizedImageSize] = useState(null);
  
  // 是否正在优化中（用于按钮加载状态）/ Whether optimizing is in progress (for button loading state)
  const [isOptimizing, setIsOptimizing] = useState(false);
  
  // 错误信息（用于显示错误提示）/ Error message (for displaying error alerts)
  const [errorMessage, setErrorMessage] = useState('');

  // 后端API地址 / Backend API URL
  // 这个地址必须与Flask后端运行的地址一致 / This must match the Flask backend address
  const API_URL = 'http://127.0.0.1:5000/upload';

  // ==================== 工具函数 / Utility Functions ====================
  /**
   * 将字节数格式化为易读的文件大小字符串 / Format bytes to human-readable file size string
   * 
   * 转换逻辑 / Conversion logic:
   * - 1024 bytes = 1 KB
   * - 1024 KB = 1 MB
   * - 1024 MB = 1 GB
   *
   * @param {number} bytes - 文件大小（字节）/ The file size in bytes
   * @returns {string} 格式化的文件大小（如 "2.5 MB"）/ Formatted file size (e.g., "2.5 MB")
   */
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';  // 特殊处理0字节 / Special case for 0 bytes
    const k = 1024;  // 1KB = 1024字节 / 1KB = 1024 bytes
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];  // 单位数组 / Unit array
    // 计算应该使用哪个单位（通过对数运算）/ Calculate which unit to use (via logarithm)
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    // 计算数值并保留2位小数 / Calculate value and keep 2 decimal places
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // ==================== 事件处理函数 / Event Handlers ====================
  /**
   * 处理图片选择事件 / Handle image selection event
   * 
   * 流程 / Workflow:
   * 1. 获取用户选择的文件 / Get user-selected file
   * 2. 验证文件类型 / Validate file type
   * 3. 创建预览URL / Create preview URL
   * 4. 更新状态 / Update state
   * 
   * @param {Event} e - 文件输入框的change事件 / File input change event
   */
  const handleImageSelect = (e) => {
    const file = e.target.files[0];  // 获取第一个选中的文件 / Get first selected file
    if (file) {
      // 定义允许的文件类型 / Define allowed file types
      // 只接受JPEG、PNG、WEBP格式 / Only accept JPEG, PNG, WEBP formats
      const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
      
      // 验证文件类型 / Validate file type
      if (!allowedTypes.includes(file.type)) {
        setErrorMessage('Unsupported file type. Please upload JPG, PNG or WEBP.');
        // 清空所有图片相关状态 / Clear all image-related state
        setSelectedImage(null);
        setSelectedImageUrl(null);
        setSelectedImageSize(null);
        setOptimizedImageUrl(null);
        setOptimizedImageSize(null);
        return;  // 提前返回，不继续处理 / Early return, don't proceed
      }

      // 文件类型有效，清空错误信息 / File type is valid, clear error message
      setErrorMessage('');
      
      // 保存文件对象 / Save file object
      setSelectedImage(file);
      
      // 保存文件大小 / Save file size
      setSelectedImageSize(file.size);
      
      // 创建可用于<img>标签的本地URL / Create local URL for <img> tag
      // URL.createObjectURL()创建一个指向内存中文件的URL / Creates a URL pointing to file in memory
      setSelectedImageUrl(URL.createObjectURL(file));
      
      // 清空之前的优化结果 / Clear previous optimization results
      setOptimizedImageUrl(null);
      setOptimizedImageSize(null);
    }
  };

  /**
   * 处理表单提交（优化图片）/ Handle form submission (optimize image)
   * 
   * 流程 / Workflow:
   * 1. 验证是否选择了图片 / Validate if image is selected
   * 2. 构建FormData发送到后端 / Build FormData to send to backend
   * 3. 等待后端处理 / Wait for backend processing
   * 4. 显示优化结果 / Display optimization result
   * 
   * @param {Event} e - 表单提交事件 / Form submit event
   */
  const handleSubmit = async (e) => {
    e.preventDefault();  // 阻止表单默认提交行为（避免页面刷新）/ Prevent default form submission (avoid page refresh)

    // 验证是否选择了图片 / Validate if image is selected
    if (!selectedImage) {
      alert('Please select an image first');
      return;  // 未选择图片，直接返回 / No image selected, return early
    }

    // 设置加载状态 / Set loading state
    setIsOptimizing(true);  // 按钮显示"Optimizing..." / Button shows "Optimizing..."
    setErrorMessage('');  // 清空之前的错误信息 / Clear previous error messages

    // 构建FormData对象（用于发送文件）/ Build FormData object (for sending files)
    // FormData是浏览器提供的API，用于构造multipart/form-data类型的请求
    // FormData is a browser API for constructing multipart/form-data requests
    const formData = new FormData();
    formData.append('image', selectedImage);  // 添加图片文件 / Add image file
    formData.append('quality', quality);  // 添加质量参数 / Add quality parameter

    try {  // 异常捕获 / Exception handling
      // 发送HTTP POST请求到Flask后端 / Send HTTP POST request to Flask backend
      // fetch()是浏览器提供的API，用于发送网络请求 / fetch() is browser API for network requests
      // await表示等待异步操作完成 / await means wait for async operation to complete
      const response = await fetch(API_URL, {
        method: 'POST',  // 使用POST方法 / Use POST method
        body: formData,  // 请求体为FormData / Request body is FormData
      });

      // 检查响应状态 / Check response status
      if (response.ok) {  // response.ok表示状态码200-299 / response.ok means status code 200-299
        // 获取响应的二进制数据（图片）/ Get response binary data (image)
        const blob = await response.blob();
        
        // 创建本地URL用于显示图片 / Create local URL for displaying image
        const imageUrl = URL.createObjectURL(blob);
        
        // 更新优化后的图片URL / Update optimized image URL
        setOptimizedImageUrl(imageUrl);
        
        // 更新优化后的文件大小 / Update optimized file size
        setOptimizedImageSize(blob.size);
      } else {  // 请求失败 / Request failed  // 请求失败 / Request failed
        // 构建错误信息 / Build error message
        let message = `Upload failed with status ${response.status}`;
        try {
          // 尝试解析JSON格式的错误信息 / Try to parse JSON error message
          const data = await response.json();
          message = data.error || message;  // 使用后端返回的错误信息 / Use error from backend
        } catch {
          // 如果响应不是JSON格式，保持默认错误信息 / Keep default message if response is not JSON
        }
        setErrorMessage(message);  // 显示错误信息 / Display error message
        console.error('Upload failed:', message);  // 控制台打印错误 / Log error to console
      }
    } catch (error) {  // 捕获网络错误（如后端未运行）/ Catch network errors (e.g., backend not running)
      // 提示用户检查后端是否运行 / Prompt user to check if backend is running
      setErrorMessage('Cannot connect to backend. Please confirm Flask is running on http://127.0.0.1:5000');
      console.error('Error uploading image:', error);  // 控制台打印错误详情 / Log error details to console
    } finally {  // 无论成功失败都执行 / Execute regardless of success or failure
      setIsOptimizing(false);  // 结束加载状态 / End loading state
    }
  };

  // ==================== 副作用处理 / Side Effects ====================
  /**
   * useEffect Hook用于处理副作用 / useEffect Hook for handling side effects
   * 
   * 这里用于清理内存：当组件卸载时释放URL对象 / Used here for memory cleanup: release URL objects when component unmounts
   * URL.createObjectURL()创建的URL会占用内存，必须手动释放 / URLs created by URL.createObjectURL() occupy memory and must be manually released
   */
  useEffect(() => {
    // 返回清理函数 / Return cleanup function
    // 这个函数会在组件卸载或依赖项改变时执行 / This function runs when component unmounts or dependencies change
    return () => {
      // 清理选中图片的URL / Cleanup selected image URL
      if (selectedImageUrl) {
        URL.revokeObjectURL(selectedImageUrl);  // 释放内存 / Release memory
      }
      // 清理优化图片的URL / Cleanup optimized image URL
      if (optimizedImageUrl) {
        URL.revokeObjectURL(optimizedImageUrl);  // 释放内存 / Release memory
      }
    };
  }, [selectedImageUrl, optimizedImageUrl]);  // 依赖项数组：当这些值变化时重新执行 / Dependency array: re-run when these values change

  // ==================== JSX渲染 / JSX Rendering ====================
  // return语句返回要渲染的JSX（类似HTML的语法）/ return statement returns JSX to render (HTML-like syntax)
  return (
    <div className="container">  {/* 最外层容器 / Outermost container */}
      <header className="header">  {/* 头部区域 / Header section */}
        <h1>Image Optimizer</h1>  {/* 标题 / Title */}
      </header>

      <main className="main-content">  {/* 主内容区域 / Main content area */}
        {/* 表单：包含上传、质量调整和提交按钮 / Form: contains upload, quality adjustment and submit button */}
        <form onSubmit={handleSubmit} className="upload-form">
          {/* 上传区域 / Upload section */}
          <div className="upload-section">
            <label htmlFor="image-upload">Upload Image</label>  {/* 标签 / Label */}
            {/* 文件输入框,限制只接受JPEG、PNG、WEBP格式 / File input, restricted to JPEG, PNG, WEBP formats */}
            <input
              id="image-upload"
              type="file"
              accept=".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp"
              onChange={handleImageSelect}
            />
          </div>

          {/* 质量调整区域 / Quality adjustment section */}
          <div className="quality-section">
            <label htmlFor="quality">Quality: {quality}%</label>  {/* 显示当前质量值 / Display current quality value */}
            {/* 滑块输入,范围0-100：0=最低质量,100=最高质量 / Slider input, range 0-100: 0=lowest quality, 100=highest quality */}
            <input
              type="range"
              id="quality"
              min="0"
              max="100"
              value={quality}
              onChange={(e) => setQuality(parseInt(e.target.value))}
            />
          </div>

          {/* 按钮区域 / Button section */}
          <div className="button-section">
            {/* 提交按钮,优化中时禁用 / Submit button, disabled while optimizing */}
            <button 
              type="submit"
              disabled={isOptimizing}
            >
              {/* 三元运算符：根据状态显示不同文本 / Ternary operator: show different text based on state */}
              {isOptimizing ? 'Optimizing...' : 'Optimize Image'}
            </button>
          </div>
        </form>

        {/* 错误信息显示 / Error message display */}
        {/* 条件渲染：只有当errorMessage存在时才显示 / Conditional rendering: only show when errorMessage exists */}
        {errorMessage && (
          <p style={{ color: '#b00020', marginTop: '1rem', fontWeight: 600 }}>
            {errorMessage}  {/* 显示错误信息 / Display error message */}
          </p>
        )}

        {/* 图片对比区域 / Images comparison section */}
        <div className="images-comparison">
          {/* 原图显示区域 / Original image display area */}
          {/* 条件渲染：只有选择了图片才显示 / Conditional rendering: only show when image is selected */}
          {selectedImageUrl && (
            <div className="image-container">
              <h2>Original Image</h2>  {/* 标题 / Title */}
              {/* 显示原图,使用本地URL,响应式样式 / Display original image with local URL, responsive style */}
              <img 
                src={selectedImageUrl}
                alt="Original version"
                style={{ maxWidth: '100%', height: 'auto' }}
              />
              <p>Size: {formatFileSize(selectedImageSize)}</p>  {/* 显示文件大小 / Display file size */}
            </div>
          )}

          {/* 优化图显示区域 / Optimized image display area */}
          {/* 条件渲染：只有优化完成后才显示 / Conditional rendering: only show after optimization */}
          {optimizedImageUrl && (
            <div className="image-container">
              <h2>Optimized Image</h2>  {/* 标题 / Title */}
              {/* 显示优化后的图片,响应式样式 / Display optimized image with responsive style */}
              <img 
                src={optimizedImageUrl}
                alt="Optimized version"
                style={{ maxWidth: '100%', height: 'auto' }}
              />
              <p>Size: {formatFileSize(optimizedImageSize)}</p>  {/* 优化后文件大小 / Optimized file size */}
              
              {/* 压缩率显示 / Compression ratio display */}
              {/* 只有当原图和优化图大小都存在时才显示 / Only show when both sizes exist */}
              {selectedImageSize && optimizedImageSize && (
                <p>
                  Size Reduction: {/* 文件大小减少百分比 / File size reduction percentage */}
                  {(((selectedImageSize - optimizedImageSize) / selectedImageSize) * 100).toFixed(1)}%
                </p>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
  // 结束return语句,返回完整的JSX渲染树 / End return statement, returns complete JSX render tree
}
// 结束App函数组件定义 / End App function component definition

// 导出App组件作为默认导出 / Export App component as default export
// 这样其他文件可以通过 import App from './App' 来使用这个组件
// This allows other files to use this component via import App from './App'
export default App
