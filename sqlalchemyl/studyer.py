from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,Table
from sqlalchemy.orm import relationship,backref
from sqlalchemy.ext.declarative import declarative_base
#创建引擎
engine = create_engine('mysql://root@localhost/study?charset=utf8')
#创建声明基类时传入引擎
Base = declarative_base(engine)

Rela = Table('rela',Base.metadata,Column('tag_id',Integer,ForeignKey('tag.id'),primary_key=True),
				Column('course_id',Integer,ForeignKey('course.id'),primary_key=True))


class User(Base): #继承声明基类
	__tablename__ = 'user' #设置数据表名字，不可忽略
	id = Column(Integer,primary_key=True) #设置该字段为主键
	#unique设置唯一约束，nullable设置非空约束
	name = Column(String(64),unique=True,nullable=False)
	email = Column(String(64),unique=True)

	#此特殊方法定义实例的打印样式
	def __repr__(self):
		return '<User: {}>'.format(self.name)

class Course(Base):
	__tablename__ = 'course'
	id = Column(Integer,primary_key=True)
	name = Column(String(64))
	#ForeignKey设置外键关联，第一个参数为字符串，user为数据表名，id为字段名
	#第二个参数ondelete设置删除User实例后对关联的Course实例的处理规则
	#‘CASCADE’表示级联删除，删除用户实例后，对应的课程实例也会被连带删除
	user_id = Column(Integer,ForeignKey('user.id',ondelete='CASCADE'))
	#relationship设置查询接口，以便后期进行数据库查询操作
	#第一个参数为位置参数，参数值为外键关联的映射类名，数据类型为字符串
	#第二个参数backref设置反向查询接口
	#backref的第一个参数‘course’为查询属性，User实例使用该属性可以获得相关课程实例的列表
	#backref的第二个参数cascade如此设置即可实现python语句删除用户数据时级联删除课程数据
	user = relationship('User',backref=backref('course',cascade='all,delete-orphan'))

	def __repr__(self):
		return '<Course: {}>'.format(self.name)

class Lab(Base):
	__tablename__ = 'lab'
	id = Column(Integer,ForeignKey('course.id'),primary_key=True)
	name = Column(String(128))
	course = relationship('Course',backref=backref('lab',uselist=False))
	
	def __repr__(self):
		return '<Lab: {}>'.format(self.name)

class Tag(Base):
	__tablename__ = 'tag'
	id = Column(Integer,primary_key=True)
	name = Column(String(64),unique=True)
	course = relationship('Course',secondary=Rela,backref='tag')

	def __repr__(self):
		return '<Tag: {}>'.format(self.name)


if __name__ == '__main__':
	Base.metadata.create_all()
