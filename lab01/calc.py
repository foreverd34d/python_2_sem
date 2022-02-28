# Модуль калькулятора двоичных чисел
#
# Кирилл Кононенко ИУ7-25Б

def summarize(a: str, b: str):
    """Сумма двух двоичных чисел"""

    if len(a) > len(b):
        a, b = b, a
    a = '0'*(len(b)-len(a)) + a # Заполнение нулями старших разрядов меньшего числа
    result = ''
    overflow = 0

    for i in range(len(a) - 1, -1, -1):
        s = int(a[i]) + int(b[i]) + add_one
        overflow = s // 2
        s %= 2
        result += str(s)

    if overflow == 1:
        result += '1'

    return result[::-1]

def multiply(a: str, b: str):
    """Произведение двух двоичных чисел"""

    result = ''

    if len(a) > len(b):
        a, b = b, a

    for i in range(len(a)):
        if a[-i-1] == '0':
            continue
        x = b + '0'*i
        result = summarize(result, x)
        
    return result

def substract(a: str, b: str):
    """Разность двух двочиных чисел"""