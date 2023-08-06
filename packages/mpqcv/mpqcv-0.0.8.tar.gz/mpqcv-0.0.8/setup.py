from setuptools import find_packages, setup
setup(
    name='mpqcv',
    version='0.0.8',
    description='CV for MPQ',
    author='MPQ',#作者
    author_email='miaopeiqi@163.com',
    url='https://github.com/miaopeiqi',
    #packages=find_packages(),
    #data_files=['mpqcv/*.pyd']
    packages=['mpqcv'],  #这里是所有代码所在的文件夹名称
        package_data={
        '':['*.pyd'],
        },
    install_requires=[''],
)
