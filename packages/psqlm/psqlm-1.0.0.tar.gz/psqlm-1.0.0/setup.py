# -*- encoding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
	long_description = fh.read()
setuptools.setup(
	name="psqlm",
	version="1.0.0",
	author="坐公交也用券",
	author_email="liumou.site@qq.com",
	description="使用Python编写的基于pymysql二次封装模块",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitee.com/liumou_site/psqlm",
	packages=["psqlm"],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",

	],
	# Py版本要求
	python_requires='>=3.0',
	# 依赖
	install_requires=[]
)
