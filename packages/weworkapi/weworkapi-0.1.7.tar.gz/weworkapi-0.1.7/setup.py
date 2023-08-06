from setuptools import setup, find_packages

# 学习了这篇文章：https://zhuanlan.zhihu.com/p/276461821
# 总结一下就是先写个 setup.py 文件，然后按照下面步骤操作：
# python3 setup.py sdist
# python3 setup.py register
# python3 setup.py sdist upload
setup(
    name='weworkapi',
    version='0.1.7',
    author='may.xiaoya.zhang',
    author_email='may.xiaoya.zhang@gmail.com',
    # 下面这个包运行出错
    # pip3 install -U wework
    # 这个包解决了问题
    # git clone https://github.com/sbzhu/weworkapi_python
    # 结合两个包，就有了这个包 :-)
    description='weworkapi修改了wework包中的WXBizMsgCrypt.py文件，修改结果另存为WXBizMsgCrypt3.py文件',
    packages=find_packages()
)
