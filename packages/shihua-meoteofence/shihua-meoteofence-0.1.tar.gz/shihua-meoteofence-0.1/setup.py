from setuptools import setup,find_packages

### 打开readme文件流，使用utf-8编码
with open("README.mdown","r",encoding="utf-8") as fh:
        long_description = fh.read()

setup(
        ### 包与作者信息
        name = 'shihua-meoteofence',
        version = '0.1',
        author = 'shihua',
        author_email = "15021408795@163.com",
        python_requires = ">=3.9.12",
        license = "MIT",

        ### 源码与依赖
        packages = find_packages(),
        include_package_data = True,
        description = 'Meoteofence is a preprocessing program for numerical weather forecasting, which is mainly used to segment the original meteorological data according to the five dimensions of starting time, prediction time, spatial hierarchy, meteorological physical quantities and station coordinate grid. The main technology uses HDF5 to organize the matrix data after analysis, uses hook technology to organize the code, and adds parallel processing at the prediction time level.',
        # install_requires = ['pluggy','tables','pandas','numpy'],

        ### 包接入点，命令行索引
        # entry_points = {
        #     'console_scripts': [
        #         'fichectl = fiche.cli:fiche'
        #     ]
        # }      

        ### pypi配置
        long_description = long_description,
        long_description_content_type = "text/markdown",
        url = "https://github.com/redblue0216/Meoteofence",
        classsifiers = [
                "Programming Language :: Python :: 3.9",
                "License :: OSI Approved :: MIT License",
                "Topic :: Scientific/Engineering :: Mathematics"
        ]

)