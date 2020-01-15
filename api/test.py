import time

tasks = [
    {
        'id': 1,
        'title': u'Basdries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

def test(parameter):
    time.sleep(1)
    return tasks[parameter]