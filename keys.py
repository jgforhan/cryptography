import secrets
import random
import helpers

class MakeKey:

    def __init__(self, size_bits=2048, trials=50):
        self.key = None
        self.size = size_bits
        self.trials = trials

    def get_key(self):
        return self.key
    
    def get_size(self):
        return self.size

    def set_size(self, new_size):
        self.size = new_size

    def get_num_trials(self):
        return self.trials

    def set_num_trials(self, new_num_trials):
        self.trials = new_num_trials
    
    ## The lower limit is 2
    ## The upper limit is current key - 1
    def __create_witness__(self):
        # 2 <= return value < upper_bound
        return random.randrange(2, self.key-1)
    
    # Create a list of witnesses length count to stand trial for
    # Compositeness in the Miller-Robin test
    def __create_witnesses__(self):
        witness_list = [self.__create_witness__() for i in range(self.trials)]
        return witness_list
    
    # decompose (accused - 1) into (2**k)q
    # where q is odd
    # pow2_exp is the exponent k
    def __miller_robin_decomp__(self, number):
        pow2_exp = 0
        odd_factor = -1
        while number % 2 == 0:
            number //= 2
            pow2_exp += 1
        odd_factor = number
        return (odd_factor, pow2_exp)
    
    # Attempt to determine if accused is composite using witness
    # True corresponds to the test determining the accused to be composite
    # False corresponds to the test failing to detect if accused is composite
    def __miller_robin_trial__(self, witness):
        # composite if even
        if self.key % 2 == 0:
            return True
        # returns two parameters: 'odd' and 'pow2'
        params = self.__miller_robin_decomp__(self.key - 1)
        examinee = helpers.fast_powering(witness, params[0], self.key)
        if examinee == 1:
            return False
        for i in range(params[1]):
            if (examinee + 1) % self.key == 0:
                return False
            examinee = (examinee**2) % self.key
        return True
    
    ## Run num_trials Miller-Robin trials on accused
    ## Pick random values 1 < witness < accused
    ## If any trial returns True, then the test has passed
    ## and thus returns the witness
    ## If all trials fail then the test returns -1
    ## and P(accused is compsite) < (0.25)**num_trials
    def __miller_robin_test__(self, witness_list):
        for witness in witness_list:
            if self.__miller_robin_trial__(witness):
                return witness
        return -1

    # Generate a cryptographically strong random odd int of length 'num_bits' bits
    def __attempt_generate_key__(self):
        ## MSB and LSB must be 1
        potential_key = 2**(self.size-1) + 1
        potential_key += secrets.randbits(self.size-2) << 1
        self.key = potential_key

    def generate_key(self):
        while True:
            self.__attempt_generate_key__()
            witness_list = self.__create_witnesses__()
            if self.__miller_robin_test__(witness_list) < 0:
                break
        return self.key
            
            
        