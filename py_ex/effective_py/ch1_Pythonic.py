#! /usr/bin/env python3

from urllib.parse import parse_qs


# item 3: Know the Differences between bytes, str, and unicode
def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str

    return value    # instance of str


def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value    # instance of bytes


# item 4: Write Helper Functions Instead of Complex Expressions
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        found = int(found[0])
    else:
        found = default

    return found


my_values = parse_qs('red=5&blue=0&green=',
                     keep_blank_values=True)

print('my_values')
print('\nUsing the "repr" method:')
print(repr(my_values))

print('\nUsing the "get" method:')
print('Red:     ', my_values.get('red'))
print('Green:   ', my_values.get('green'))
print('Opacity: ', my_values.get('opacity'))

print('\nIndexing the "get" result:')
red = my_values.get('red', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0
print('Red:     %r' % red)
print('Green:   %r' % green)
print('Opacity: %r' % opacity)

print('\nUsing the helper function:')
red = get_first_int(my_values, 'red')
green = get_first_int(my_values, 'green')
opacity = get_first_int(my_values, 'opacity')
print('Red:     %r' % red)
print('Green:   %r' % green)
print('Opacity: %r' % opacity)


# item 5: know how to slice sequences
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print('First 4:', a[:4])
print('Last 4: ', a[-4:])
print('Middle 2:', a[3: -3])
print('All:', a[:])
print('neg index "-4":', a[-4:])
print('big neg index "-10":', a[-10:])

assert a[:5] == a[0:5]
assert a[5:] == a[5:len(a)]


# item 6: avoid using start, end, and stride in a single slice
a = [1, 2, 3, 4, 5, 6, 7, 8]
odds = a[::2]
evens = a[1::2]
reverse = a[::-1]
print('odds: %r' % odds)
print('evens: %r' % evens)
print('reverse: %r' % reverse)
