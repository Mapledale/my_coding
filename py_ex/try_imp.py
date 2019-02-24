#! /usr/bin/env python
# _*_ coding: utf-8 _*_

#from my_imp import my_func

# wrong! ValueError: Attempted relative import in non-package
#from . import my_imp as my_imp
#print('from . import my_imp as my_imp')

# wrong! SyntaxError: invalid syntax - import <imp> can only use absolute path
#import .py_exer.my_imp as my_imp
#print('import .py_exer.my_imp as my_imp')

# good!
#import my_imp as my_imp
#print('import my_imp as my_imp')

# good!
import py_exer.my_imp as my_imp
print('import py_exer.my_imp as my_imp')

# good!
#from py_exer import my_imp as my_imp
#print('from py_exer import my_imp as my_imp')

my_imp.my_func()
