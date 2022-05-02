#! /usr/bin/env python3

"""Calculator.

Evaluates arithmetic expressions with integers, for example:

                        a / (b + c) * d - e

    ((2-1)*4 + 6) / 5           ->  2
    (625+375)/100 - 2*(2+3)     ->  0

"""

import A_stack


def braces_sequence_is_correct(s: str):
    """Check the correctness of the bracket sequence.
    
    >>> braces_sequence_is_correct('{}(()) {(())()}')
    True
    >>> braces_sequence_is_correct(')')
    False
    >>> braces_sequence_is_correct('({)}')
    False

    """
    A_stack.clear()
    for brace in s:
        if brace in '(){}':
            if brace in '({':
                A_stack.push(brace)
                
            elif brace in ')}' and not A_stack.is_empty():
                tmp = A_stack.pop()
                if tmp == '(' and brace != ')':
                    return False
                if tmp == '{' and brace != '}':
                    return False
                
            elif A_stack.is_empty():
                # Tries to pop from the stack while the stack is empty.
                return False

    return A_stack.is_empty()

def check_correct_expression(s: str):
    """Check the correctness of the entered arithmetic expression.

    - removes spaces
    - check the correctness of the bracket sequence
    - check for invalid characters
    - check for the absence of operation signs at the beginning and
      at the end of the expression, as well as 2 or more consecutive
      operation signs without a number between them

    Returns an expression as a list of tokens or writes an error.
    
    >>> check_correct_expression('(2+2 *2 ')
    Некорректная скобочная последовательность

    >>> check_correct_expression('256 + 347 - 123 ы')
    Некорректное выражение
    Введён недопустимый символ

    >>> check_correct_expression('+ 2 - 3')
    Некорректное выражение
    Знак операции в неожиданном месте

    >>> check_correct_expression('2 - 3*')
    Некорректное выражение
    Знак операции в неожиданном месте

    >>> check_correct_expression('2 - *3')
    Некорректное выражение
    Знак операции в неожиданном месте

    >>> check_correct_expression('(2 + 2) * 2')
    ['(', '2', '+', '2', ')', '*', '2']

    """
    if not braces_sequence_is_correct(s):
        print('Некорректная скобочная последовательность')
        return
    
    s = s.replace(' ', '')
    if s[0] in '+-*/' or s[-1] in '+-*/':
        print('Некорректное выражение'\
              '\nЗнак операции в неожиданном месте')
        return
    
    infix_list = []
    token = ''
    for i in range(len(s)):
        if s[i] in '+-*/' and s[i-1] in '+-*/':
            print('Некорректное выражение'\
                  '\nЗнак операции в неожиданном месте')
            return
        
        if s[i] in '0123456789':
            if token:
                if token[-1] in '0123456789':
                    token += s[i]
                else:
                    infix_list.append(token)
                    token = s[i]
            else:
                token += s[i]
                
        elif s[i] in '+-*/()':
            if token:
                infix_list.append(token)
            token = s[i]
            
        else:
            print('Некорректное выражение'\
                  '\nВведён недопустимый символ')
            return
        
    infix_list.append(token)

    return infix_list

def infix_to_postfix(infix_list: list):
    """Transforms an expression from infix notation to postfix notation
    using Dijkstra`s algorithm.
        
    >>> infix_to_postfix(['5', '*', '(', '15', '+', '25', ')'])
    ['5', '15', '25', '+', '*']
    
    >>> infix_to_postfix(['(', '5', '+', '15', ')', '*', '2'])
    ['5', '15', '+', '2', '*']
    
    >>> infix_to_postfix(['(', '5', '*', '(', '15', '+', '25', ')', '-', '(', '120', '-', '20', ')', ')', '/', '25'])
    ['5', '15', '25', '+', '*', '120', '20', '-', '-', '25', '/']

    >>> infix_to_postfix(['(', '2', '*', '15', '+', '20', ')', '/', '(', '12', '+', '2', '-', '9', ')'])
    ['2', '15', '*', '20', '+', '12', '2', '9', '-', '+', '/']

    >>> infix_to_postfix(['2', '-', '1', '-', '1'])
    ['2', '1', '-', '1', '-']

    >>> infix_to_postfix(['8', '/', '4', '/', '2'])
    ['8', '4', '/', '2', '/']

    """
    infix_reverse = infix_list[:]
    infix_reverse.reverse()

    A_stack.clear()
    result = []

    while len(infix_reverse) > 0:
        token = infix_reverse.pop()
        if token in '+-*/':
            if not A_stack.is_empty() and A_stack.top() == '(':
                A_stack.push(token)
            else:
                if token == '/':
                    while not A_stack.is_empty() and A_stack.top() in '/':
                        result.append(A_stack.pop())
                    A_stack.push(token)
                elif token == '*':
                    while not A_stack.is_empty() and A_stack.top() in '/':
                        result.append(A_stack.pop())
                    A_stack.push(token)
                elif token == '-':
                    while not A_stack.is_empty() and A_stack.top() in '-*/':
                        result.append(A_stack.pop())
                    A_stack.push(token)
                elif token == '+':
                    while not A_stack.is_empty() and A_stack.top() in '-*/':
                        result.append(A_stack.pop())
                    A_stack.push(token)

        elif token == '(':
            A_stack.push(token)
            
        elif token == ')':
            while A_stack.top() != '(':
                result.append(A_stack.pop())
            A_stack.pop()  # '('
            
        else:  # token is number
            result.append(token)

    while not A_stack.is_empty():
        result.append(A_stack.pop())

    return result

def postfix_calc(s: list):
    """Evaluates the value of an expression given in postfix notation.

    If there is an attempt to divide by zero, writes a message about it.

    >>> postfix_calc(['2', '1', '-', '4', '*', '6', '+', '5', '/'])
    2.0

    >>> postfix_calc(['2', '3', '-', '12', '10', '-', '*', '4', '2', '/', '+'])
    0.0

    >>> postfix_calc(['1', '2', '3', '-', '12', '10', '-', '*', '4', '2', '/', '+'])
    Некорректное выражение

    >>> postfix_calc(['4', '5', '3', '-', '+'])
    6.0

    >>> postfix_calc(['4', '5', '-', '3', '+'])
    2.0

    >>> postfix_calc(['10', '5', '/', '2', '4', '*', '3', '1', '/', '-', '+'])
    7.0

    >>> postfix_calc(['7', '3', '6', '2', '3', '/', '*', '-', '+'])
    6.0

    >>> postfix_calc(['2', '1', '-', '1', '-'])
    0.0

    >>> postfix_calc(['1', '0', '/'])
    Нельзя делить на 0

    """
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
                try:
                    number_3 = number_1 / number_2
                except ZeroDivisionError:
                    print('Нельзя делить на 0')
                    return
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

def number_formatting(number: float):
    """Rounds an integer.

    If the number is an integer, round it, discarding .0

    >>> number_formatting(2.0)
    2

    """
    if number == None:
        return 1/0
    if str(number)[-2:] == '.0':
        number = int(number)
    return number

def main():
    """The main part of the programm."""
    
    print('\t\t\t"Калькулятор"'
          '\n\n\nУмеет вычислять арифметические выражения '
          'с целыми числами, например: '
          '\n\n\t\t    a / (b + c) * d - e\n')

    expression = input('\nВведите выражение:\n')
    while expression:
        try:
            expression = check_correct_expression(expression)
            result = infix_to_postfix(expression)
            result = postfix_calc(result)
            result = number_formatting(result)
            print('=', result)
            expression = input('\nВведите выражение:\n')
        except NameError:
            expression = input('\nВведите выражение:\n')
        except TypeError:
            expression = input('\nВведите выражение:\n')
        except ZeroDivisionError:
            expression = input('\nВведите выражение:\n')


if __name__ == '__main__':
    main()
    
##    import doctest
##    doctest.testmod()
