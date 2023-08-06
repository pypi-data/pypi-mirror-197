from setuptools import setup,find_namespace_packages,find_packages

setup(
name='nonebot_plugin_simulator_xiuxian',
version='0.5.18',
description='修仙',
#long_description=open('README.md','r').read(),
author='luoyefufeng',
author_email='2859385794@qq.com',
license='MIT license',
include_package_data=True,
packages=find_namespace_packages(include=["nonebot_plugin_simulator_xiuxian"]),
platforms='all',
install_requires=["nonebot2","nonebot-adapter-onebot",'wget==3.2'],
url='https://github.com/luoyefufeng/nonebot_plugin_xiuxian_1',
)


