import json
import random


# Strategy: make json object, and traverse it in order to make the string
# the parser reads in.
class ExpMaker:
    def __init__(self):
        self.var = 'a'
        self.fn = 'func'
        self.filename = 'string.txt'
        self.operators = ['+', '-', '*', '/', '^', '%']
        self.precedence = {
            '+' : 3,
            '-' : 3,
            '*' : 4,
            '/' : 4,
            '%' : 4,
            '^' : 5
        }
        self.max_num = len(self.operators) - 1
        self.s_count = 1
        self.exps = set()
        self.type_map = make_type_map()
        self.expected_json = None

    def run(self):
        for num_func_calls in range(5):
            for num_operators in range(16):
                self.exps.add(self.make_expression(num_operators, num_func_calls))

        self.exps = list(self.exps)
        self.exps.sort(key=len)
        for i, exp in enumerate(self.exps):
            with open('Scenario' + str(i) + '.txt', 'w') as output:
                output.write(exp)
                

        

    # randint(a, b)
    def make_expression(self, op_count, num_func_calls):
        
        op = self.operators[random.randint(0, self.max_num)]
        if op_count > 1:
            if num_func_calls > 2:
                calls = num_func_calls // (random.randint(1, (num_func_calls // 2)))
            else:
                calls = 0
            rem_calls = num_func_calls - calls
            
            lhs = self.make_expression((op_count // 2), calls)
            rhs = self.make_expression(op_count - (op_count // 2), rem_calls)

            self.exps.add(lhs)
            self.exps.add(rhs)
            lhs = self.group(lhs,calls)
            rhs = self.group(rhs, rem_calls)

            return lhs + op + rhs

        be_negative = random.randint(0, 10) == 5
        if be_negative:
            #self.exps.add('-' + self.var)
            return neg_var()
        else:
            return make_variable()
        #self.exps.add(self.var)
        #return self.var
    
    def group(self, exp, calls):
        use_parens = random.randint(0, 6) == 4
        if use_parens:
            exp = '(' + exp + ')'
            self.exps.add(exp)
        make_func = random.randint(0, 10) == 5
        if make_func and calls > 0:
            args = list()
            for i in range(random.randint(0, 5)):
                args.append(self.make_expression(i, 0))
            if len(args) > 0:
                exp = self.fn + '(' + exp + ',' + ','.join(args) + ')'
            else:
                exp = self.fn + '(' + exp + ')'
        return exp





def neg_var(self):
    prefix = empty_exp()
    prefix['op'] = "PREFIX"
    prefix['token'] = make_token('-', FILENAME, 1)
    prefix['right_exp'] = make_variable()
    return prefix

def make_variable():
    var = empty_exp()
    var['leaf_value'] = 'a'
    var['token'] = make_token('a', FILENAME, 1)
    return var

def empty_exp():
    return {
        "left_value": None,
        "right_value": None,
        "op": None,
        "leaf_value": None,
        "args": [],
        "token": None,
        "left_exp": None,
        "right_exp": None
    }

def make_token(lit, fname, line):
    return {
        "literal": lit,
        "filename": fname,
        "line_number": line
    }

"""
    return {
        "left_value": None,
        "right_value": None,
        "op": "MINUS",
        "leaf_value": None,
        "args": [],
        "token": {
            "literal": "-",
            "filename": self.filename,
            "line_number": 1
        },
        "left_exp": None,
        "right_exp": {
            "left_value": None,
            "right_value": None,
            "op": None,
            "leaf_value": "a",
            "args": [],
            "token": {
                "literal": "a",
                "filename": self.filename,
                "line_number": 1
            },
            "left_exp": None,
            "right_exp": None
        }
    }
"""













def make_type_map():
    map = dict()
    map['+'] = ['SUM']
    map['-'] = ['SUM', 'PREFIX']
    map['*'] = ['PRODUCT']
    map['/'] = ['PRODUCT']
    map['%'] = ['PRODUCT']
    map['^'] = ['EXPONENT']
    return map






if __name__ == '__main__':
    exp = ExpMaker()
    exp.run()