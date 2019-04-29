
# %% iniziamo sta sequenza
# fibo(n) = fibo(n-1) + fibo(n-2)
def fibo(n):
    if n == 0:
        return 1

    elif n == 1:
        return 1
    elif n >= 2:
        return fibo(n-1)+fibo(n-2)
for x in range(int(input('quanti numeri della sequenza vuoi avere?'))):
    print(fibo(x))

ciao
