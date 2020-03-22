from sqlalchemy.orm import sessionmaker
from faker import Faker
from studyer import Base,engine,User,Course,Lab,Tag

session = sessionmaker(engine)()
fake = Faker('zh-cn')

def create_users():
	for i in range(10):
		user = User(name=fake.name(),email=fake.email())
		session.add(user)

def create_courses():
	#session有个query方法用来查询数据，参数为映射类的类名
	#all方法表示查询全部，这里也可以省略不写
	#user就是上一个函数create_users中的user对象
	for user in session.query(User).all():
		for i in range(2):
			course = Course(name=''.join(fake.words(4)),user_id = user.id)
			session.add(course)

def create_labs():
	for course in session.query(Course):
		lab = Lab(name=''.join(fake.words(5)),id=course.id)
		session.add(lab)

def create_tags():
	for name in ['python','linux','java','mysql','kisp']:
		tag = Tag(name=name)
		session.add(tag)


def main():
	create_users()
	create_courses()
	create_labs()
	create_tags()

	session.commit()

if __name__ == '__main__':
	main()
