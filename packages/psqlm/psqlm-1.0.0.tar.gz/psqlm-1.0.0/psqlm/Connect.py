#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   Connect.py
@Time    :   2023-03-17 17:57
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
from pymysql import connect
from loguru import logger


class Connect:
	def __init__(self, host, user, password, database="mysql", port=3306, timeout=5, charset='utf8', debug=True):
		"""
		初始化数据库连接参数
		:param host: 设置登录主机
		:param user: 设置登录用户
		:param password: 设置登录密码
		:param port: 设置连接端口，默认： 3306
		:param timeout: 设置超时连接,默认: 5
		:param database: 设置数据库名称,默认：mysql
		:param charset: 设置编码,默认: utf8
		:param debug: 是否显示调试信息
		"""
		self.debug = debug
		self.charset = charset
		self.database = database
		self.timeout = timeout
		self.port = port
		self.password = password
		self.user = user
		self.host = host
		self.data = None
		self.connect = connect(host=host, port=port, user=user, passwd=password, connect_timeout=timeout,
		                       charset=charset)

	def ReConnect(self):
		"""
		重新连接
		:return:
		"""
		self.connect = connect(host=self.host,
		                       port=self.port,
		                       user=self.user,
		                       passwd=self.password,
		                       connect_timeout=self.timeout,
		                       charset=self.charset)

	def status(self):
		"""
		判断数据库连接状态
		:return:
		"""
		try:
			print("状态检测 - 设置连接超时: [ %s ]" % self.timeout)
			self.connect.select_db(self.database)
			return True
		except Exception as err:
			logger.error('数据库连接失败: status')
			print(err)
			logger.error(str(err))
			return False

	def Close(self):
		"""
		关闭连接
		:return:
		"""
		self.connect.close()

	def Commit(self, sql):
		"""
		提交数据，不限制数据库和表，使用update语法
		:param sql: 需要提交数据的SQL语句
		:return:
		"""
		try:
			self.connect.select_db(self.database)
		except Exception as err:
			logger.error("commit函数连接失败")
			logger.error(str(err))
			return False
		commit = self.connect.cursor()
		try:
			commit.execute(sql)
			self.connect.commit()
			commit.close()
			if self.debug:
				print("提交成功: ", sql)
			return True
		except Exception as err:
			info = str("提交失败: " + sql)
			logger.error(info)
			logger.error(str(err))
			return False

	def Select(self, sql):
		"""
		执行查询语句
		:param sql: 数据表查询语句
		:return: 执行结果(bool)，执行数据请通过实例变量data获取
		"""
		self.data = None
		try:
			self.connect.select_db(self.database)
		except Exception as e:
			logger.error('数据库连接失败: cmd')
			logger.error(str(e))
			return False
		# print("cmd")
		cmd = self.connect.cursor()
		try:
			cmd.execute(sql)
			self.data = cmd.fetchall()
			cmd.close()
			if not self.data:
				return False
			else:
				return True
		except Exception as e:
			logger.error('SQl_cmd: %s' % e)
			logger.error(str(e))
			cmd.close()
			return False
