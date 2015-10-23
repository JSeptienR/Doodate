from collections import OrderedDict
import datetime

from peewee import *

db = SqliteDatabase('doodate.db')

class Task(Model):
	content = TextField()
	due_date = DateTimeField(default=datetime.datetime.now)
	timestamp = DateTimeField(default=datetime.datetime.now)
	
	class Meta:
		database = db

def initialize():
	db.connect()
	db.create_tables([Task], safe=True)


def add_task():
	"""Add a Task"""
	print("Enter task:")
	data = input('>> ')
	print("Due date? (mm/dd/yyyy or t for today)")
	date = input('>> ').strip()
	if data and date and input('Save task? [Yn]: ').lower() != 'n':
		if date != 't':
			due = datetime.datetime.strptime(date, '%m/%d/%Y')
			Task.create(content = data, due_date = due)
		else:
			Task.create(content = data)


def delete_task():
	"""Delete a Task"""
	tasks = view_tasks()
	
	index = int(input('Which task to delete? ').strip())
	if index > 0 and index < len(tasks):
		task = tasks[index - 1]
		if input('Delete "{}. {}"? [yN]:'.format(index, task.content)).strip().lower() == 'y':
			task.delete_instance()
	else:
		print('No task with that index.')

def empty_tasks(task):
	"""Empty Tasks List"""
	tasks = Task.select().order_by(Task.due_date)
	for task in tasks:
		task.delete_instance()


def view_tasks():
	"""View Tasks"""
	print('-' * 10)
	print('  TASKS')
	print('-' * 10)
	tasks = Task.select().order_by(Task.due_date)
	
	for index, task in enumerate(tasks):
		due_date = task.due_date.strftime('%A %B %d, %Y')
		print("{}. {}. --> Due {}".format(index + 1, task.content, due_date))
		
	return tasks
			
def menu_loop():
	"""Show Menu"""
	choice = None
	
	while choice != 'q':
		print('-' * 10)
		print('  MENU')
		print('-' * 10)
		for key, value in menu.items():
			print('{}) {}'.format(key, value.__doc__))
		choice = input('Select: ').lower().strip()
		if choice in menu:
			menu[choice]()
		

menu = OrderedDict([
	('a', add_task),
	('v', view_tasks),
	('d', delete_task)
])

if __name__ == '__main__':
	initialize()
	menu_loop()

