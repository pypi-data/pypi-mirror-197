from distutils.core import setup

setup(
    name="math_t",      #对外我们的模块名
    version="1.0",           #版本号
    description="这是一个发布模块，测试",#描述
    author="linan",          #作者
    author_email="365763491@qq.com",     #作者邮箱
    py_modules=["math_t.demo1","math_t.demo2"]    #要发布的模块
)