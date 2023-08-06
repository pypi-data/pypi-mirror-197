import numpy as np

def convertir_arreglo(arreglo):
    return np.array(arreglo)

def burbuja_optimus(arreglo):
    n = len(arreglo)
    for i in range(n - 1):
        intercambio = False
        for j in range(n - 1 - i):
            if arreglo[j] > arreglo[j + 1] :
                arreglo[j], arreglo[j + 1] = arreglo[j + 1], arreglo[j]
                intercambio = True
        if intercambio == False:
            break

def shellSort(arreglo):
	intervalo = len(arreglo) // 2
	while intervalo > 0:
		for i in range(intervalo, len(arreglo)):
			j = i - intervalo
			while j >= 0:
				k = j + intervalo
				if (arreglo[j] <= arreglo[k]):
					break
				else:
					arreglo[j], arreglo[k] = arreglo[k], arreglo[j]
					j = j - intervalo
		intervalo = intervalo // 2 

def __partition(arreglo, low, high):
    pivot = arreglo[high]
    i = low - 1
    for j in range(low, high):
        if arreglo[j] <= pivot:
            i = i + 1
            (arreglo[i], arreglo[j]) = (arreglo[j], arreglo[i])
    (arreglo[i + 1], arreglo[high]) = (arreglo[high], arreglo[i + 1])
    return i + 1
 
def quickSort(arreglo, low, high):
    if low < high:
        pi = __partition(arreglo, low, high)
        quickSort(arreglo, low, pi - 1)
        quickSort(arreglo, pi + 1, high)

def __countingSort(arreglo, exp1):
	n = len(arreglo)
	output = [0] * (n)
	count = [0] * (10)

	for i in range(0, n):
		index = arreglo[i] // exp1
		count[index % 10] += 1

	for i in range(1, 10):
		count[i] += count[i - 1]

	i = n - 1
	while i >= 0:
		index = arreglo[i] // exp1
		output[count[index % 10] - 1] = arreglo[i]
		count[index % 10] -= 1
		i -= 1

	i = 0
	for i in range(0, len(arreglo)):
		arreglo[i] = output[i]

def radixSort(arreglo):
    max1 = max(arreglo)
    exp = 1
    while max1 / exp >= 1:
        __countingSort(arreglo, exp)
        exp *= 10