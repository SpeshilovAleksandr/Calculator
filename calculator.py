import A_stack


def postfix_calc(s: list):
    '''
    >>> postfix_calc(['2', '1', '-', '4', '*', '6', '+', '5', '/'])
    2
    >>> postfix_calc(['2', '3', '-', '12', '10', '-', '*', '4', '2', '/', '+'])
    0
    >>> postfix_calc(['1', '2', '3', '-', '12', '10', '-', '*', '4', '2', '/', '+'])
    Некорректное выражение
    >>> postfix_calc(['4', '5', '3', '-', '+'])
    6
    >>> postfix_calc(['4', '5', '-', '3', '+'])
    2
    >>> postfix_calc(['10', '5', '/', '2', '4', '*', '3', '1', '/', '-', '+'])
    7
    >>> postfix_calc(['7', '3', '6', '2', '3', '/', '*', '-', '+'])
    6
    '''
    n = len(s)
    for i in range(n // 2):
        s[i], s[n - i - 1] = s[n - i - 1], s[i]

    A_stack.clear()
    while len(s) != 0:
        token = s.pop()
        if token not in '+-*/':
            A_stack.push(token)
        elif token in '+-*/':
            number_2 = float(A_stack.pop())
            number_1 = float(A_stack.pop())
            if token == '+':
                number_3 = number_1 + number_2
            elif token == '-':
                number_3 = number_1 - number_2
            elif token == '*':
                number_3 = number_1 * number_2
            elif token == '/':
                number_3 = number_1 / number_2
            else:
                print('Невозможная ситуация, ожидался оператор + - * /')
            A_stack.push(number_3)
            
        else:
            print('Некорректное выражение')
    result = A_stack.pop()
    if A_stack.is_empty():
        return result
    else:
        print('Некорректное выражение')

def infix_to_postfix(s: str):
    '''
    >>> infix_to_postfix('4 + 5 - 3')
    ['4', '5', '3', '-', '+']
    >>> infix_to_postfix('4 - 5 + 3')
    ['4', '5', '-', '3', '+']
    >>> infix_to_postfix('4-5+ 3')
    ['4', '5', '-', '3', '+']
    >>> infix_to_postfix('5 + 3 * 2 - 4')
    ['5', '3', '2', '*', '4', '-', '+']
    >>> infix_to_postfix('2 * 3 + 2 * 5')
    ['2', '3', '*', '2', '5', '*', '+']
    >>> infix_to_postfix('10 / 5 + 2 * 4 - 3 / 1')
    ['10', '5', '/', '2', '4', '*', '3', '1', '/', '-', '+']
    >>> infix_to_postfix('7 + 3 - 6 * 2 / 3')
    ['7', '3', '6', '2', '3', '/', '*', '-', '+']
    >>> infix_to_postfix('')
    []
    >>> infix_to_postfix('256 + 347 - 123')
    ['256', '347', '123', '-', '+']
    >>> infix_to_postfix('256 + 347 - 123 ы')
    Некорректное выражение
    '''
    
    s = s.replace(' ', '')

    infix_list = []
    token = ''
    for i in range(len(s)):
        if s[i] in '0123456789':
            token += s[i]
        elif s[i] in '+-*/':
            infix_list.append(token)
            token = ''
            infix_list.append(s[i]) # Добавляем знак операции в список
        else:
            return print('Некорректное выражение')
    infix_list.append(token)

    infix_reverse = infix_list[:]
    infix_reverse.reverse()

    A_stack.clear()
    result = []
    while len(infix_reverse) > 0:
        token = infix_reverse.pop()
        if token in '+-*/':
            if token == '/':
                A_stack.push(token)
            elif token == '*':
                while not A_stack.is_empty() and A_stack.top() in '/':
                    result.append(A_stack.pop())
                A_stack.push(token)
            elif token == '-':
                while not A_stack.is_empty() and A_stack.top() in '*/':
                    result.append(A_stack.pop())
                A_stack.push(token)
            elif token == '+':
                while not A_stack.is_empty() and A_stack.top() in '-*/':
                    result.append(A_stack.pop())
                A_stack.push(token)
        else:
            result.append(token)

    while not A_stack.is_empty():
        result.append(A_stack.pop())

    return result

def main():
    print('\t\tКалькулятор'\
          '\n\nУмеет вычислять корректные выражения вида: a / b + c * d - e'\
          '\nПоддерживаются знаки операций: " + - * / "'\
          '\nСкобки не поддерживаются')

    expression = input('\nВведите выражение:\n')
    while expression:
        result = postfix_calc(infix_to_postfix(expression))
        print('=', result)
        expression = input('\nВведите выражение:\n')











if __name__ == '__main__':
    main()
