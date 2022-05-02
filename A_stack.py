'''
>>> is_empty()
True
>>> push(1)
>>> push(2)
>>> push(3)
>>> is_empty()
False
>>> pop()
3
>>> pop()
2
>>> pop()
1
>>> is_empty()
True
>>> push(5)
>>> clear()
>>> is_empty()
True
>>> top()
''
>>> push(1)
>>> top()
1
>>> is_empty()
False

'''


_stack = []


def push(x):
    _stack.append(x)

def pop():
    return _stack.pop()

def is_empty():
    return not bool(_stack)

def clear():
    _stack.clear()

def top():
    return _stack[-1]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
