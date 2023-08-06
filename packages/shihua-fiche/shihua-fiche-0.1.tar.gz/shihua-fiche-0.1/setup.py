from setuptools import setup,find_packages

### 打开readme文件流，使用utf-8编码
with open("README.mdown","r",encoding="utf-8") as fh:
        long_description = fh.read()

setup(
        ### 包与作者信息
        name = 'shihua-fiche',
        version = '0.1',
        author = 'shihua',
        author_email = "15021408795@163.com",
        python_requires = ">=3.9.12",
        license = "MIT",

        ### 源码与依赖
        packages = find_packages(),
        include_package_data = True,
        description = 'Fiche is a metadata management tool with MongoDB about algorithm info,model info,parameter info,application info,dataset info and more;supporting http interface and python sdk.',
        # install_requires = ['click','fastapi','rich','pymongo'],

        ### 包接入点，命令行索引
        entry_points = {
            'console_scripts': [
                'fichectl = fiche.cli:fiche'
            ]
        },

        ### pypi配置
        long_description = long_description,
        long_description_content_type = "text/markdown",
        url = "https://github.com/redblue0216/Fiche",
        classsifiers = [
                "Programming Language :: Python :: 3.9",
                "License :: OSI Approved :: MIT License",
                "Topic :: Scientific/Engineering :: Artificial Intelligence"
        ]      
)