'''
Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

The brackets must close in the correct order, "()" and "()[]{}" are all valid but "(]" and "([)]" are not.
'''

class Solution:
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        if len(s) <= 1:
            return False
        
        for i in range(len(s)):
            (rst, i) = self.secValid(s, i)
            if not rst:
                break
        
        return rst
    
    def secValid(self, s, i):
        p0 = ['(', '[', '{']
        p1 = [')', ']', '}']
        
        if i == len(s) - 1:
            return (False, i)
        
        c = s[i]
        if c not in p0:
            return (False, i)
        else:
            c_next = s[i + 1]
            if c_next in p0:
                return self.secValid(s, i + 1) 
            elif c_next in p1:
                idx = p0.index(c)
                idx_next = p1.index(c_next)
                if idx == idx_next:
                    return (True, i + 2)
                else:
                    return (False, i)
            else:
                return (False, i)
                
