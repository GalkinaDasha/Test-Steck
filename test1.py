#На Python
#---------------------------------------------------------------------------------------------------
import traceback


class TestRunner(object):
    def __init__(self, name):
        self.name = name
        self.testNo = 1

    def expectTrue(self, cond):
        try:
            if cond():
                self._pass()
            else:
                self._fail()
        except Exception as e:
            self._fail(e)

    def expectFalse(self, cond):
        self.expectTrue(lambda: not cond())

    def expectException(self, block):
        try:
            block()
            self._fail()
        except:
            self._pass()

    def _fail(self, e=None):
        print(f'FAILED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1
        if e is not None:
            traceback.print_tb(e.__traceback__)

    def _pass(self):
        print(f'PASSED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1


def match(string, pattern):
	# ------------------------------------------------------------------------------------------------
	# Решение задачи 1
	# ------------------------------------------------------------------------------------------------
	# проверка длинны
	if len(string)!=len(pattern):
		return False
	# проверка на верность символов в шаблоне
	for symbl in pattern:
		if symbl != "a" and symbl != "d" and symbl != "*" and symbl != " ":
			raise BaseException("wrong symbol")
	# проверка соответствия строки шаблону
	index = 0
	for symbl in string:
		if symbl == " " and pattern[index] != " ":
			return False
		if symbl != " " and pattern[index] == " ":
			return False
		if symbl.isdigit() and symbl != "*" and pattern[index] == "a" and pattern[index] != "*":
			return False
		if not(symbl.isdigit()) and symbl != "*" and pattern[index] == "d" and pattern[index] != "*":
			return False
		index = index+1
	return True




def testMatch():
    runner = TestRunner('match')

    runner.expectFalse(lambda: match('xy', 'a'))
    runner.expectFalse(lambda: match('x', 'd'))
    runner.expectFalse(lambda: match('0', 'a'))
    runner.expectFalse(lambda: match('*', ' '))
    runner.expectFalse(lambda: match(' ',  'a'))

    runner.expectTrue(lambda:  match('01 xy', 'dd aa'))
    runner.expectTrue(lambda: match('1x', '**'))

    runner.expectException(lambda:  match('x', 'w'))

tasks = {
    'id': 0,
    'name': 'Все задачи',
    'children': [
        {
            'id': 1,
            'name': 'Разработка',
            'children': [
                {'id': 2, 'name': 'Планирование разработок', 'priority': 1},
                {'id': 3, 'name': 'Подготовка релиза', 'priority': 4},
                {'id': 4, 'name': 'Оптимизация', 'priority': 2},
            ],
        },
        {
            'id': 5,
            'name': 'Тестирование',
            'children': [
                {
                    'id': 6,
                    'name': 'Ручное тестирование',
                    'children': [
                        {'id': 7, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 8, 'name': 'Выполнение тестов', 'priority': 6},
                    ],
                },
                {
                    'id': 9,
                    'name': 'Автоматическое тестирование',
                    'children': [
                        {'id': 10, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 11, 'name': 'Написание тестов', 'priority': 3},
                    ],
                },
            ],
        },
        {'id': 12, 'name': 'Аналитика', 'children': []},
    ],
}

# поиск нужной группы
def findGroup(task, groupId):
	if "priority" in task:
		return None
	if task["id"] == groupId:
		return task
	if "children" not in task:
		return None
	else:
		for child in task["children"]:
			x = findGroup(child, groupId)
			if x:
				return x

# поиск задачи с наивысшим приоритетом
def findTask(task, tempTask):
	temp = tempTask
	# если не группа, а задача, проверка на приоритет
	if "priority" in task:
		if tempTask is None:
			return task
		if task["priority"] > tempTask["priority"]:
			return task
	# если группа, то проверяем все под группы или задачи в группе
	if "children" not in task:
		return tempTask
	else:
		for child in task["children"]:
			x = findTask(child, temp)
			if x:
				temp = x
	return temp


def findTaskHavingMaxPriorityInGroup(tasks, groupId):
	# ------------------------------------------------------------------------------------------------
	# Решение задачи 2
	# ------------------------------------------------------------------------------------------------
	group = findGroup(tasks, groupId)
	if group is None:
		raise BaseException("wrong id")
	return findTask(group, None)


def taskEquals(a, b):
    return (
        not 'children' in a and
        not 'children' in b and
        a['id'] == b['id'] and
        a['name'] == b['name'] and
        a['priority'] == b['priority']
    )


def testFindTaskHavingMaxPriorityInGroup():
    runner = TestRunner('findTaskHavingMaxPriorityInGroup')

    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 13))
    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 2))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 12) is None)

    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 0), {
        'id': 8,
        'name': 'Выполнение тестов',
        'priority': 6,
    }))
    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 1), {
        'id': 3,
        'name': 'Подготовка релиза',
        'priority': 4,
    }))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 9)['priority'] == 3)


testMatch()
testFindTaskHavingMaxPriorityInGroup()