from enum import Enum
from math import pi
import random as rn
import time

t0 = time.time()

SCALE = 100

# Класс фигуры: является общим предком для классов конкретных фигур
class Figure:

	def __init__(self, color):
		self.color = color


# Класс круга
class Circle(Figure):
	# Конструктор
	def __init__(self, color, x, y, r):
		Figure.__init__(self, color)
		self.x, self.y, self.r = x, y, r
	# Метод вычисления площади
	def get_area(self):
		return pi * self.r ** 2
	# Определяем представление объекта для функции str()
	def __str__(self):
		return "Circle " + " ".join(list(map(str, [self.color.name, self.x, self.y, self.r])))
	# Статический метод создания круга с случайными параметрами
	def create_random():
		return Circle(Color(rn.randrange(6)), SCALE * rn.random(), SCALE * rn.random(), SCALE * rn.random())

# Класс прямоугольникав
class Rectangle(Figure):

	def __init__(self, color, x1, y1, x2, y2):
		Figure.__init__(self, color)
		self.x1, self.y1 = x1, y1
		self.x2, self.y2 = x2, y2

	def get_area(self):
		return (self.x2 - self.x1) * (self.y1 - self.y2)

	def __str__(self):
		return "Rectangle " + " ".join(list(map(str, [self.color.name, self.x1, self.y1, self.x2, self.y2])))

	def create_random():
		x1, y1, = SCALE * rn.random(), SCALE * rn.random()
		x2, y2, = SCALE * rn.random(), SCALE * rn.random()
		return Rectangle(Color(rn.randrange(6)), min(x1, x2), max(y1, y2), max(x1, x2), min(y1, y2))

# Класс треугольника
class Triangle(Figure):

	def __init__(self, color, x1, y1, x2, y2, x3, y3):
		Figure.__init__(self, color)
		self.x1, self.y1 = x1, y1
		self.x2, self.y2 = x2, y2
		self.x3, self.y3 = x3, y3

	def get_area(self):
		return 0.5 * abs((self.x2-self.x1) * (self.y3-self.y1) - (self.x3-self.x1) * (self.y2-self.y1))

	def __str__(self):
		return "Triangle " + " ".join(list(map(str, [self.color.name, self.x1, self.y1, self.x2, self.y2, self.x3, self.y3])))

	def create_random():
		return Triangle(Color(rn.randrange(6)), SCALE * rn.random(), SCALE * rn.random(), SCALE * rn.random(), SCALE * rn.random(), SCALE * rn.random(), SCALE * rn.random())

# Перечисление цветов
class Color(Enum):
	RED = 0
	ORANGE = 1
	YELLOW = 2
	GREEN = 3
	BLUE = 4
	PURPLE = 5

# Функция выполняющая бинарный поиск величины target_area в массиве collection от индекса start до индекса end
def binary_search(collection, target_area, start, end):
	while start <= end:
		mid = (start+end)//2
		mid_area = collection[mid].get_area()
		if mid_area < target_area:
			end = mid - 1
		elif mid_area > target_area:
			start = mid + 1
		else:
			return mid
	return start

# Функция, выполняющая binary insertion sort в массиве collection
def sort_figures(collection):
	for i in range(1, len(collection)):
		figure = collection[i]
		j = binary_search(collection, figure.get_area(), 0, i-1)
		collection = collection[:j] + [figure] + collection[j:i] + collection[i+1:]
	return collection

# Функция, создающая массив из size случайных фигур
def create_random_collection(size=1000):
	collection = []
	for i in range(size):
		figure_type = rn.randrange(3)
		if figure_type == 0:
			collection.append(Circle.create_random())
		elif figure_type == 1:
			collection.append(Rectangle.create_random())
		else:
			collection.append(Triangle.create_random())
	return collection

# Функция, проверяющая отсортирован ли массив по убыванию
def is_sorted(collection):
	for i in range(1, len(collection)):
		if collection[i].get_area() > collection[i-1].get_area():
			return False
	return True

# Функция, сохраняющая массив фигур collection в файл filename
def serialize_collection(collection, filename="output.txt"):
	string_figures = [str(figure) + "\n" for figure in collection]
	with open(filename, "w") as f:
		f.writelines(string_figures)

# Функция, создающая фигуру типа fig_type c цветом color и параметрами args
def create_figure(fig_type, color, args):
	if fig_type == "Circle":
		x, y, r = map(float, args)
		return Circle(color, x, y, r)
	elif fig_type == "Rectangle":
		x1, y1, x2, y2 = map(float, args)
		return Rectangle(color, x1, y1, x2, y2)
	else:
		x1, y1, x2, y2, x3, y3 = map(float, args)
		return Triangle(color, x1, y1, x2, y2, x3, y3)
	return figure

# Функция, считывающая массив из файла filename
def deserialize_collection(filename="input.txt"):
	collection = []
	with open(filename, "r") as f:
		for string in f.readlines():
			args = string.strip().split()
			fig_type, color = args[0], Color[args[1]]
			collection.append(create_figure(fig_type, color, args[2:]))
	return collection

# Создаем массив размером size со случайными фигурами
random_collection = create_random_collection(size=10)
# Выводим в консоль (каждый элемент с новой строки)
print("\n".join([str(i) for i in random_collection]))
# Выводим в консоль площади фигур в созданном массиве
print([i.get_area() for i in random_collection])
# Сортируем
sorted_collection = sort_figures(random_collection)
# Выводим в консоль площади фигур в отсортированном массиве
print([i.get_area() for i in sorted_collection])
print("--- %s seconds ---" % (time.time() - t0))
