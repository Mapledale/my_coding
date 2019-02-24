#!/usr/bin/env python3
# _*_ code: utf-8 _*_
""" Demo for iterator """


class Primes_iter(object):
    """ An iterator to get all prime numbers not greater than n """

    def __init__(self, n):
        self.top = n
        self.prm = 1

    def __iter__(self):
        return self

    def __next__(self):
        self.prm += 1
        if self.prm >= self.top:
            raise StopIteration
        elif self.is_prime(self.prm):
            return self.prm
        else:
            return self.__next__()

    def is_prime(self, n):
        """ to determine whether or not a positive integer is prime """
        i = 2
        while i <= int(n ** 0.5):
            if n % i == 0:
                return False
            i += 1
        return True


def primes_gene(max):
    """ generator to get all prime numbers not greater than n """
    num = 1
    while num < max:
        num += 1
        if is_prime(num):
            yield num


def is_prime(n):
    """ to determine whether or not a positive integer is prime """
    i = 2
    while i <= int(n ** 0.5):
        if n % i == 0:
            return False
        i += 1
    return True

# my_prm = primes_gene(17)
my_prm = (i for i in range(2, 18) if is_prime(i))
print(my_prm)
print(my_prm.__next__())
for i in my_prm:
    print(i)
