from ctypes import Structure, Union, c_float, c_uint32, c_uint8
import math
import time

from matplotlib import pyplot as plt


class struct (Structure):
     _fields_ = [("f", c_uint32,23),
                ("e", c_uint32, 8),
                ("s",c_uint32,1)
                ]

class IEE754(Union):
     _fields_ = [("x",c_float),
                 ("bits",struct)]

def novo_numero_IEEE(num):
    y = IEE754()
    y.x = num
    return y

# def get_IEE754(y):
#     z = IEE754()
#     z.x = y
#     fz = z.bits.f
#     e = z.bits.e
#     s = z.bits.s
#     f23 = 0.00000011920928955078125 # 2^-23
#     fr = fz*f23 # ver como float
#     return fz,e,s,fr

def IEEE_POW_2(exp):
    x = novo_numero_IEEE(2)

    a = c_uint8(x.bits.e)
    b = c_uint8(exp - 1)

    if(exp > 0):
        while b.value != 0:
            carry = c_uint8(a.value & b.value) # Carry value is calculated 
            a = c_uint8(a.value ^ b.value) # Sum value is calculated and stored in a
            b = c_uint8(carry.value << 1) # The carry value is shifted towards left by a bit
    # elif(exp < 0):
    #     while b.value != 0:
    #         borrow = c_uint8((~a.value) & b.value) #get the borrow bit
    #         a = c_uint8(a.value ^ b.value) # get the difference using XOR
    #         b = c_uint8(borrow.value << 1)

    x.bits.e = a.value
    return x # returns the final sum

def gerar_nice_numbers(inicio, fim):
    nice_numbers = []

    for i in range(inicio, fim+1):
         # Encontra os nice numbers no formato
         # +- (2 ** +-i) +- 1

         nice_number_1 = (2**i)+1
         nice_number_2 = (2**i)-1

         nice_number_3 = (2**-i)+1
         nice_number_4 = (2**-i)-1

         nice_number_5 = -(2**-i)+1
         nice_number_6 = -(2**-i)-1

         nice_number_7 = -(2**i)+1
         nice_number_8 = -(2**i)-1

         nice_numbers.append(nice_number_1)
         nice_numbers.append(nice_number_2)
         nice_numbers.append(nice_number_3)
         nice_numbers.append(nice_number_4)
         nice_numbers.append(nice_number_5)
         nice_numbers.append(nice_number_6)
         nice_numbers.append(nice_number_7)
         nice_numbers.append(nice_number_8)

    nice_numbers.sort()
    nice_numbers = list(dict.fromkeys(nice_numbers)) # Remove números duplicados
    return nice_numbers

def gerar_tabela_ln_da_lista(lista_numeros):
    lista_numeros = [i for i in lista_numeros if i > 0] # Modifica a lista para apenas número positivos

    dict_ln = {}

    for i in lista_numeros:
        dict_ln[i] = math.log(i, math.e)

    return dict_ln

def reduzir_argumento(x, lista):
    for i in lista:
        if i > x:
            imediatamente_superior = i
            break

    x_red = x / imediatamente_superior

    return x_red, imediatamente_superior

def encontrar_i_do_nice_number(nice_number):
    i = 0

    while True:
        nice_numbers = []

        nice_number_1 = (2**i)+1
        nice_number_2 = (2**i)-1

        nice_number_3 = (2**-i)+1
        nice_number_4 = (2**-i)-1

        nice_number_5 = -(2**-i)+1
        nice_number_6 = -(2**-i)-1

        nice_number_7 = -(2**i)+1
        nice_number_8 = -(2**i)-1

        nice_numbers.append(nice_number_1)
        nice_numbers.append(nice_number_2)
        nice_numbers.append(nice_number_3)
        nice_numbers.append(nice_number_4)
        nice_numbers.append(nice_number_5)
        nice_numbers.append(nice_number_6)
        nice_numbers.append(nice_number_7)
        nice_numbers.append(nice_number_8)

        if(nice_number in nice_numbers):
            break
        else:
            i = i + 1

    return i

def recuperacao_residuo(xn):
    return abs(1 - xn)


def ln(x):
    nice_numbers = gerar_nice_numbers(-8, 8)
    lista_ln = gerar_tabela_ln_da_lista(nice_numbers)
    argumento_reduzido, numero_imediatamente_superior = reduzir_argumento(x, nice_numbers)

    xj = argumento_reduzido
    yj = lista_ln[numero_imediatamente_superior]
    iter = len(lista_ln.keys())

    while iter > 0:
        maior_k = 0

        for i in lista_ln.keys():
            # Se k for 1, não há mudança no resultado
            if(i != 1 and i * xj < 1):
                maior_k = i

        # Condição de parada
        # Percorreu toda a lista de logaritmo e não encontrou
        # valor tal que i * xj < 1
        if(maior_k == 0):
            break

        xj = maior_k * xj
        yj = yj - lista_ln[maior_k]
        iter = iter -1

    resultado_ln = yj - recuperacao_residuo(xj)

    return resultado_ln
    # print("ln(", x, ") = ", resultado_ln)

def main():
    x = IEEE_POW_2(5)
    print(x.x)

    # fz, e, s, fr = get_IEE754(3.125)
    # print(fz,e,s,fr)

    # x para cálculo de ln(x)
    # erro,x_list,tempo,resultado_calculadora,resultado_nice_numbers = [],[],[],[],[]
    # for x in range(1,100):

    #     ln_calculadora = math.log(x)

    #     start = time.time()
    #     ln_nice_numbers = ln(x)
    #     end = time.time()

    #     erro.append(abs(ln_nice_numbers - ln_calculadora))

    #     tempo.append(end -start)
    #     x_list.append(x)
    #     resultado_calculadora.append(ln_calculadora)
    #     resultado_nice_numbers.append(ln_nice_numbers)

    # #Erro
    # plt.plot(x_list,erro,label = 'ln(X)-Calculadora X Nice-Numbers')
    # plt.ylabel('Erro')
    # plt.xlabel('Argumento')
    # plt.legend()
    # plt.show()
    # #tempo
    # plt.plot(x_list,tempo,label = 'Tempo-Nice-Numbers')
    # plt.ylabel('Tempo')
    # plt.xlabel('Argumento')
    # plt.legend()
    # plt.show()
    # #Resultado
    # plt.plot(x_list,resultado_calculadora,label = 'ln(X)-Calculadora',color ='blue')
    # plt.plot(x_list,resultado_nice_numbers,label = 'ln(X)- Nice-Numbers',color =  'red')
    # plt.yscale('log')
    # plt.ylabel('ln(x)')
    # plt.xlabel('Argumento')
    # plt.legend()
    # plt.show()


main()

