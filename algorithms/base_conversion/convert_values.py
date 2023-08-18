import math

bases = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


# Convert a number from one base to the other.

def to_decimal(val: str, base: str):
    _str = str(val)
    base_ = bases.index(base)
    if base_ == -1:
        raise exception(f'base not found in list of bases:\n{bases}')
    b10_val = 0
    rs = _str[::-1]
    mult = 1
    for i, c in enumerate(rs):
        b10_val += mult * bases.index(c)
        mult *= base_
    return b10_val


def from_decimal(val: int, base: str):
    numbase = bases.index(base)
    if numbase == -1:
        raise exception(f'base not found in list of bases:\n{bases}')
    reps = []
    mult = 1
    while mult < 10**50:
        reps.append(mult)
        if mult * numbase > val:
            break
        mult *= numbase
    reps = reps[::-1]
    out = []
    remainder = val
    for m in reps:
        (idx, remainder) = divmod(remainder, m)
        out.append(bases[idx])
    out = ''.join(out)    
    return out, numbase

if __name__ == "__main__":
    bin_val = '101110110101011101'
    b10 = to_decimal(bin_val, '2')
    b, numbase = from_decimal(b10, 'Z')
    print(f'Base {numbase} Value of binary {bin_val} is {b}')

    _str = input('Number in any base >>')
    print(_str)
    input_base = input('base of previous number >>')
    output_base = input(f'Choose from {bases}\nDesired output base >>')

    in_base = bases.index(input_base)
    out_base = bases.index(output_base)
    print('\n', in_base, out_base)
    out, bn = from_decimal(to_decimal(_str, input_base), output_base)
    print(f'Base {bn} value of input, {_str} in base {in_base}, is {out}')


