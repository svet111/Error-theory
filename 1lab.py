import math
from matplotlib import pyplot as plt

MANTISSA=4
MACH_ERR=10**-15
a, b=(-0.9, -0.1)

# Получение i-го члена ряда Маклорена для ф-ции arctg(x**2)
def calc_el(x, i):
    return ((-1)**(i-1))*(x**(4*i-2))/(2*i-1)

# Получение N-ой частичной суммы ряда Маклорена для ф-ции arctg(x**2)
def S(x, N):
    S=0.0
    for i in range(1, N+1):
        S+=calc_el(x, i)
    return S

# Получение N-ой частичной суммы ряда Маклорена для ф-ции arctg(x**2) с учётом округления
def S_round(x, N):
    S=0.0
    for i in range(1, N+1):
        S+=round_mant(calc_el(x, i), MANTISSA)
        S=round_mant(S, MANTISSA)
    return S

# Точное значение ф-ции arctg(x**2)
def F(x):
    return math.atan(x**2)

# Получение точек для оси OY из заданных точек оси OX и ф-ции
def y_points(x_data, func):
    return [func(i) for i in x_data]

# Получение абсолютной погрешности расчёта arctg(x**2) в точке x с помощью N-ой частичной суммы
def abs_err(x, N):
    return abs(S(x, N)-F(x))

# Получение отн-ной погрешности расчёта arctg(x**2) в точке x с помощью N-ой частичной суммы
def rel_err(x, N):
    return abs_err(x, N)/abs(S(x, N))

# Расчёт номера члена ряда, начиная с которого отн-ная погрешность расчёта очередного члена
# меньше машинного эпсилон
def calc_number(x):
    N=1
    S=calc_el(x, N)
    el=calc_el(x, N)
    err=abs(el/S)
    while err>=MACH_ERR:
        N+=1
        el=calc_el(x, N)
        S+=el
        err=abs(el/S)
    return N
    
# Получение порядка числа
def exp(f):
    return int(math.floor(math.log10(abs(f))))+1 if f != 0 else 0

# Получение мантиссы числа
def mant(f):
    return f/10**exp(f)

# Округление мантиссы числа
def round_mant(x, t):
    manti=round(mant(x), t)
    return manti*10**exp(x)
   
# Кол-во точек на оси OX
x_points_count=100
# Список самих точек, полученных равномерным распределением x_points_count по отрезку [a, b]
x_points=[a + (b-a)*(i/x_points_count) for i in range(x_points_count+1)]

fig, pl=plt.subplots(2, 2, layout='tight')

# Графики первых пяти частичных сумм и график ф-ции
pl[0][0].plot(x_points, y_points(x_points, lambda x: S(x, 1)), color="red", label="S(x, 1)")
pl[0][0].plot(x_points, y_points(x_points, lambda x: S(x, 2)), color="yellow", label="S(x, 2)")
pl[0][0].plot(x_points, y_points(x_points, lambda x: S(x, 3)), color="magenta", label="S(x, 3)")
pl[0][0].plot(x_points, y_points(x_points, lambda x: S(x, 4)), color="blue", label="S(x, 4)")
pl[0][0].plot(x_points, y_points(x_points, lambda x: S(x, 5)), color="brown", label="S(x, 5)")
pl[0][0].plot(x_points, y_points(x_points, F), color="green", label="F(x)")

# Расчёт номера частичной суммы, при котором величина отн-ной погрешности в средней точке
# станет меньше машинного эпсилон
number=calc_number((b+a)/2)
print(number)

# Графики погрешностей
pl[0][1].plot(x_points, y_points(x_points, lambda x: abs_err(x, number)),
            color="green", label= f'$\Delta S(x, {number})$')
pl[0][1].plot(x_points, y_points(x_points, lambda x: rel_err(x, number)),
            color="blue", label= f'$\delta S(x, {number})$')
pl[0][1].set(ylim=(0.0, 1e-14))

# Графики первых 5-ти частичных сумм и график ф-ции с учётом округления
pl[1][0].plot(x_points, y_points(x_points, lambda x: S_round(x, 1)),
            color="red", label="S(x, 1)")
pl[1][0].plot(x_points, y_points(x_points, lambda x: S_round(x, 2)),
            color="yellow", label="S(x, 2)")
pl[1][0].plot(x_points, y_points(x_points, lambda x: S_round(x, 3)),
            color="magenta", label="S(x, 3)")
pl[1][0].plot(x_points, y_points(x_points, lambda x: S_round(x, 4)),
            color="blue", label="S(x, 4)")
pl[1][0].plot(x_points, y_points(x_points, lambda x: S_round(x, 5)),
            color="brown", label="S(x, 5)")
pl[1][0].plot(x_points, y_points(x_points, lambda x: round_mant(F(x), MANTISSA)),
            color="green", label="F(x)")

# Графики разности между округлёнными и неокруглёнными значениями первых 5-ти частичных сумм и
# окргулёнными и неокруглёнными значениями ф-ции
pl[1][1].plot(x_points, y_points(x_points, lambda x: abs(S_round(x, 1) - S(x, 1))),
            color="red", label="S(x, 1)")
pl[1][1].plot(x_points, y_points(x_points, lambda x: abs(S_round(x, 2) - S(x, 2))),
            color="yellow", label="S(x, 2)")
pl[1][1].plot(x_points, y_points(x_points, lambda x: abs(S_round(x, 3) - S(x, 3))),
            color="magenta", label="S(x, 3)")
pl[1][1].plot(x_points, y_points(x_points, lambda x: abs(S_round(x, 4) - S(x, 4))),
            color="blue", label="S(x, 4)")
pl[1][1].plot(x_points, y_points(x_points, lambda x: abs(S_round(x, 5) - S(x, 5))),
            color="brown", label="S(x, 5)")
pl[1][1].plot(x_points, y_points(x_points, lambda x: abs(round_mant(F(x), MANTISSA) - F(x))),
            color="green", label="F(x)")

pl[0][0].legend()
pl[0][1].legend()
pl[1][0].legend()
pl[1][1].legend()
plt.show()
