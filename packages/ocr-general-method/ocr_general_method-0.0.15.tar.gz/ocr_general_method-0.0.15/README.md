# ocr封装接口通用方法

* /src/example
  * 测试

* /src/common
  * file_utils：文件工具类
  * exception：错误码工具类
  * http_utils：远程请求工具类

# 打包命令
* 打包：python -m build
* 检查：twine check dist/*
* 上传：twine upload dist/*