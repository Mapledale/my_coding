#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
Every email consists of a local name and a domain name, separated by the @ sign

For example, in alice@leetcode.com, alice is the local name,
and leetcode.com is the domain name.

Besides lowercase letters, these emails may contain '.'s or '+'s.

If you add periods ('.') between some characters in the local name part of
an email address, mail sent there will be forwarded to the same address
without dots in the local name. For example, "alice.z@leetcode.com" and
"alicez@leetcode.com" forward to the same email address.
(Note that this rule does not apply for domain names.)

If you add a plus ('+') in the local name, everything after the first plus sign
will be ignored. This allows certain emails to be filtered, for example
m.y+name@email.com will be forwarded to my@email.com.
(Again, this rule does not apply for domain names.)

It is possible to use both of these rules at the same time.

Given a list of emails, we send one email to each address in the list.
How many different addresses actually receive mails?

Example 1:
Input: ["test.email+alex@leetcode.com", "test.e.mail+bob.cathy@leetcode.com",
"testemail+david@lee.tcode.com"]
Output: 2
Explanation: "testemail@leetcode.com" and "testemail@lee.tcode.com"
actually receive mails

Note:
1 <= emails[i].length <= 100
1 <= emails.length <= 100
Each emails[i] contains exactly one '@' character.
"""


class Solution:
    def numUniqueEmails_0(self, emails: 'List[str]') -> 'int':
        """ using a list
        """
        emails_unq = []
        for e in emails:
            local, domain = e.split('@')
            local = local.split('+')[0]
            local = local.replace('.', '')
            e_unq = local + '@' + domain
            if e_unq not in emails_unq:
                emails_unq.append(e_unq)
        return len(emails_unq)

    def numUniqueEmails_1(self, emails: 'List[str]') -> 'int':
        """ using a set
        then no need to test if an address is already there:
        a set is always unique!
        """
        emails_unq = set()
        for e in emails:
            local, domain = e.split('@')
            local = local.split('+')[0]
            local = local.replace('.', '')
            e_unq = local + '@' + domain
            emails_unq.add(e_unq)
        return len(emails_unq)

    def numUniqueEmails_2(self, emails: 'List[str]') -> 'int':
        """ using a dictionary
        then no need to test if an address is already there:
        the key of a dictionary is always unique!
        """
        emails_unq = {}
        for e in emails:
            local, domain = e.split('@')
            local = local.split('+')[0]
            local = local.replace('.', '')
            e_unq = local + '@' + domain
            emails_unq[e_unq] = 1
        return len(emails_unq)
