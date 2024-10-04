import keys
import helpers

STANDARD_ENCRYPTION_EXPONENT = 65537

class RSA:
    
    def __init__(self, size_bits):
        key_gen = keys.MakeKey(size_bits=size_bits, trials=20)
        self.prime_p = key_gen.generate_key()
        self.prime_q = key_gen.generate_key()
        self.N = self.prime_p * self.prime_q
        self.e = STANDARD_ENCRYPTION_EXPONENT
        
        ## Make sure encryption exponent is coprime to p-1 and q-1
        while helpers.gcd(self.prime_p-1, STANDARD_ENCRYPTION_EXPONENT) != 1:
            self.prime_p = key_gen.generate_key(size=1024, trials=20)
        while helpers.gcd(self.prime_q-1, STANDARD_ENCRYPTION_EXPONENT) != 1:
            self.prime_q = key_gen.generate_key(size=1024, trials=20)

        self.private_key = helpers.modular_inverse(num=self.e, modulus=(self.prime_p-1)*(self.prime_q-1))
        
        self.public_key = (self.N, self.e)

    def get_public_key(self):
        return self.public_key

    def decrypt(self, cyphertext):
        message = helpers.fast_powering(base=cyphertext, exponent=self.private_key, modulus=self.N)
        return message