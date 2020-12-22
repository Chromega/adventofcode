import re
import sys

class Rule:
    def __init__(self):
        pass
        
class BaseRule(Rule):
    def __init__(self):
        self.idx = -1
        self.c = ''
    def GetRegex(self):
        return self.c
    def UpdateRuleReferences(self, rules):
        pass
        
class SequenceCompoundRule(Rule):
    def __init__(self):
        self.idx = -1
        self.ruleIndices = []
        self.subRules = []
    def GetRegex(self):
        s = '('
        for i in range(len(self.subRules)):
            s += self.subRules[i].GetRegex()
        s += ')'
        return s
    def UpdateRuleReferences(self, rules):
        self.subRules = []
        for idx in self.ruleIndices:
            self.subRules.append(rules[idx])
        
class OrCompoundRule(Rule):
    def __init__(self):
        self.idx = -1
        self.subRules = []
        self.currentRecursionDepth = 0
    def GetRegex(self):
        self.currentRecursionDepth += 1
        
        if self.currentRecursionDepth > 10:
            self.currentRecursionDepth -= 1
            return ''
            
        s = '('
        for i in range(len(self.subRules)):
            if i != 0:
                s += '|'
            s += self.subRules[i].GetRegex()
        s += ')'
        self.currentRecursionDepth -= 1
        return s
    def UpdateRuleReferences(self, rules):
        for rule in self.subRules:
            rule.UpdateRuleReferences(rules)
            
        
rules = {}
input = []
MODE_RULES = 0
MODE_INPUTS = 1
mode = MODE_RULES
with open("input2.txt") as FILE:
    for line in FILE:
        line = line.strip()
        if mode == MODE_RULES:
            if len(line)==0:
                mode = MODE_INPUTS
            else:
                #parse the line
                colonIdx = line.find(':')
                ruleIdx = int(line[:colonIdx])
                ruleStr = line[colonIdx+2:]
                
                if ruleStr.find('"') != -1:
                    rule = BaseRule()
                    rule.c = ruleStr[ruleStr.find('"')+1:-1]
                elif ruleStr.find('|') != -1:
                    rule = OrCompoundRule()
                    for subruleStr in ruleStr.split('|'):
                        subruleStr = subruleStr.strip()
                        compoundRule = SequenceCompoundRule()
                        for idx in subruleStr.split(' '):
                            compoundRule.ruleIndices.append(int(idx))
                        rule.subRules.append(compoundRule)
                else:
                    rule = SequenceCompoundRule()
                    for idx in ruleStr.split(' '):
                        rule.ruleIndices.append(int(idx))
                rules[ruleIdx] = rule
        else:
            input.append(line)
for idx in rules:
    rules[idx].UpdateRuleReferences(rules)
    rules[idx].idx = idx
    
print('parsed!')
regex = '^'+rules[0].GetRegex()+"$"
print('got regex!')

#part a
passCount = 0
for msg in input:
    if re.search(regex,msg) is not None:
        passCount += 1
print(passCount)

#part b

#Aha, doesn't work because each subrule needs the SAME number of repeats
"""
class SelfLoopingRule(Rule):
    def __init__(self):
        self.idx = -1
        self.ruleIndices = []
        self.subRules = []
    def GetRegex(self):
        s = '('
        for i in range(len(self.subRules)):
            s += self.subRules[i].GetRegex()
            s += '+'
        s += ')'
        return s
    def UpdateRuleReferences(self, rules):
        for idx in self.ruleIndices:
            self.subRules.append(rules[idx])
    
        

rule8 = SelfLoopingRule()
rule8.ruleIndices = [42,]
rules[8] = rule8

rule11 = SelfLoopingRule()
rule11.ruleIndices = [42,31]
rules[11] = rule11

for idx in rules:
    rules[idx].UpdateRuleReferences(rules)
    rules[idx].idx = idx
print('parsed!')
regex = '^'+rules[0].GetRegex()+"$"
print(regex)

passCount = 0
for msg in input:
    if re.search(regex,msg) is not None:
        passCount += 1
print(passCount) #394 too high??

"""