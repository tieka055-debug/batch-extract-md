from setuptools import find_packages, setup

setup(
    name="batch-extract-md",
    version="0.2.0",
    description="批量提取文案md：将 Get笔记知识库内容导出为 Markdown",
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={
        "console_scripts": [
            "batch-extract-md=biji_archive.cli:main",
            "biji-archive=biji_archive.cli:main",
        ]
    },
)
