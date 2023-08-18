
def cool_graphics(s, w, h):
    width = 2*s + w
    height = 2*s + h

    slong = '~' * width
    sbar = '~' * s

    for i in range(s):
        print(slong)
    print(sbar + '+' + '-'*(w-2) + '+' + sbar)
    for i in range(h-2):
        print(sbar + '|' + ' '*(w-2) + '|' + sbar)
    print(sbar + '+' + '-'*(w-2) + '+' + sbar)
    for i in range(s):
        print(slong)


if __name__ == "__main__":
    cool_graphics(2,5,3)
    print()
    cool_graphics(6,4,5)
