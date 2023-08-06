from distutils.core import setup
import setuptools

packages = ['xincshi']  # 唯一的包名，自己取名, import 导入的名字
setup(name='xincshi-hello2',  # name 是第三方库名， pip install 的名字
      version='1.0',
      author='xincshi',
      packages=packages,
      package_dir={'requests': 'requests'}, )
