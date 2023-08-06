
from setuptools import setup, find_packages

'''
name : 打包后包的文件名
version : 版本号
author : 作者
author_email : 作者的邮箱
py_modules : 要打包的.py文件
packages: 打包的python文件夹
include_package_data : 项目里会有一些非py文件,比如html和js等,这时候就要靠include_package_data 和 package_data 来指定了。package_data:一般写成{‘your_package_name’: [“files”]}, include_package_data还没完,还需要修改MANIFEST.in文件.MANIFEST.in文件的语法为: include xxx/xxx/xxx/.ini/(所有以.ini结尾的文件,也可以直接指定文件名)
license : 支持的开源协议
description : 对项目简短的一个形容
ext_modules : 是一个包含Extension实例的列表,Extension的定义也有一些参数。
ext_package : 定义extension的相对路径
requires : 定义依赖哪些模块
provides : 定义可以为哪些模块提供依赖
data_files :指定其他的一些文件(如配置文件),规定了哪些文件被安装到哪些目录中。如果目录名是相对路径,则是相对于sys.prefix或sys.exec_prefix的路径。如果没有提供模板,会被添加到MANIFEST文件中。
'''

name = "testzmnthy"
package_version = "1.0.4"
description='test zmn'
author='tianheyi'
author_email='485280869@qq.com'
maintainer='tianheyi'
maintainer_email='485280869@qq.com'
# python版本要求
python_requires=">=3.6"
# 定义自己的包依赖哪些模块
install_requires= ['requests']
# 系统自动从当前目录开始找包
packages=find_packages()
# 如果有的文件不用打包，则只能指定需要打包的文件
#packages=['代码1','代码2','__init__']  #指定目录中需要打包的py文件，注意不要.py后缀
license="apache 3.0"

setup(
    name=name,
    version=package_version,
    description=description,
    author=author,
    author_email=author_email,
    maintainer=maintainer,
    maintainer_email=maintainer_email,
    python_requires=python_requires,
    install_requires=install_requires,
    packages=packages,
    license=license
)

"""
生成dist目录，在此目录下生成相关.tar.gz和.whl文件
python setup.py sdist bdist_wheel
生成到pypi
twine upload dist/*
"""
