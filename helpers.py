# Do a binary expansion of the 'exponent' of the power
def _bin_expand(exponent):
    # From least to most significant
    bits = list()
    if exponent == 0:
        return [0]
    while (exponent > 0):
        if exponent % 2 == 0:
            bits.append(0)
        else:
            bits.append(1)
            exponent -= 1
        exponent //= 2
    return bits

# Calculate the value of 'base'**'exponent' mod 'modulus' efficiently
def fast_powering(base, exponent, modulus):
    result = 1
    exp_expanded = _bin_expand(exponent)
    power_table = [base]
    for i in range(1, len(exp_expanded)):
        power_table.append(power_table[i-1]**2 % modulus)
    for i in range(len(exp_expanded)):
        if (exp_expanded[i] != 0):
            result *= power_table[i]
        result = result % modulus
    return result

def gcd(num1, num2):
    quotient = -1
    remainder = -1
    while(remainder != 0):
        remainder = num1 % num2
        quotient = (num1 - remainder)//num2
        num1 = num2
        num2 = remainder
    # when the current remainder is 0, the prior remainder is gcd
    return num1

## Solves equation s*modulus + t*num = 1
## Returns inverse t, if it exists and 'None' otherwise
## Inverse will be returned as a positive int
def modular_inverse(num, modulus):
    t_old, t_new = 0, 1
    r_old, r_new = modulus, num

    while r_new != 0:
        quotient = r_old // r_new
        t_old, t_new = t_new, t_old - quotient * t_new
        r_old, r_new = r_new, r_old - quotient * r_new

    if r_new > 0:
        return None

    if t_old < 0:
        return t_old + modulus
    else:
        return t_old