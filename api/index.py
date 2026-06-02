from flask import Flask, request, jsonify, render_template

def get_parenthesis(term):
    LP = []
    P_Outer = []
    Track = False
    last_obj = ''
    count = 0
    for i in range(0,len(term)):
        if term[i] == '(':
            Track = True
            if last_obj == '(':
                count+= 1
            elif last_obj==')' or last_obj == '':
                P_Outer.append(i)
            last_obj = '('
        if Track:
            LP.append(i)
        if term[i] == ')':
            if count == 0:
                P_Outer.append(i)
                Track = False
            else:
                count -= 1
            last_obj = ')'
    LP.append(P_Outer)
    return LP

def get_type(term, term_dict):
    LP = get_parenthesis(term)
    i1, i2, i3 = 0,0,0
    s1, s2, s3 = False, False, False
    for i in range(len(term)):
        if term[i] == '^' and i not in LP:
            i1 = i
            s1 = True
        elif term[i] == '*' and i not in LP:
            i2 = i
            s2 = True
        elif term[i] == '/' and i not in LP:
            i3 = i
            s3 = True
    if s1:
        pow = term[i1+1:]
        var = term[i1-1]
        if var.isdigit() or var == 'e':
            term_dict[term] = 'Exp'
        elif pow.isdigit() or '.' in pow and term.find('.') not in LP:
            term_dict[term] = 'Pow'
        else:
            term_dict[term] = 'VarExp'
    elif any(i in term and term.find(i) not in LP for i in ['arcsin', 'arccos', 'arctan', 'arccot', 'arcsec', 'arccosec']):
        term_dict[term] = 'InverseTrig'
    elif any(i in term and term.find(i) not in LP for i in ['sin', 'cos', 'tan', 'cot', 'sec', 'cosec']):
        term_dict[term] = 'Trig'
    elif any(i in term and term.find(i) not in LP for i in ['ln', 'log']):
        term_dict[term] = 'Log'
    elif s2:
        term_dict[term] = ['Prod', i2]
    elif s3:
        term_dict[term] = ['Quot', i3]
    else:
        term_dict[term] = 'Linear'

def get_terms(exp:str):
    exp = exp.replace(" ", "").lower()
    Terms, op = {}, {}
    LP, L_OP =  get_parenthesis(exp), []
    cur_index = 0
    one_term = False
    for i in range(0,len(exp)):
        if exp[i] in ['+', '-'] and i not in LP:
            term = exp[cur_index:i]
            cur_index = i+1
            L_OP.append(i)
            get_type(term, Terms)

            if exp[i] == '+':
                op[i] = '+'
            else:
                op[i] = '-'
 
    if len(L_OP) >= 1:
        one_term = False
        l_term = exp[L_OP[-1]+1:]
        get_type(l_term, Terms)
    else:
        one_term = True
        get_type(exp, Terms)
    return Terms, op, one_term

def der_pow(term:str, var):
    i = term.find('^')
    o_pow = float(term[i+1:])
    if o_pow.is_integer():
        o_pow = int(o_pow)
    n_pow = f"^{o_pow-1}"
    if n_pow == '^1' or n_pow == '^1.0':
        n_pow = ''
    if term[:i-1] == '':
        der = f"{o_pow}{var}{n_pow}"
    else:
        const = float(term[:i-1]) * o_pow
        if const.is_integer():
            const = int(const)
        der = f"{const}{var}{n_pow}"
    return der

def der_linear(term:str):
    if term.isdigit():
        der = '0'
    else:
        cons = term[:len(term)-1]
        if cons == '':
            der = '1'
        else:
            der = cons
    return der

def der_exp(term:str, var):
    if term[term.find('^')-1] == 'e':
        der = f"e^{var}"
    elif term[term.find('^')-1].isdigit:
        const = term[term.find('^')-1]
        der = f"{term}ln({const})"
    return der

def der_trig(term, var):
    if 'sin' in term:
        c = term[:term.find('s')]
        der = f"{c}cos({var})"
    elif 'cosec' in term:
        c = term[:term.find('c')]
        der = f"-{c}cosec({var})cot({var})"
    elif 'cos' in term:
        c = term[:term.find('c')]
        der = f"-{c}sin({var})"
    elif 'tan' in term:
        c = term[:term.find('t')]
        der = f"{c}(sec({var}))^2"
    elif 'cot' in term:
        c = term[:term.find('c')]
        der = f"-{c}(cosec({var}))^2"
    elif 'sec' in term:
        c = term[:term.find('s')]
        der = f"{c}sec({var})tan({var})"
    return der

def der_itrig(term, var):
    c = term[:term.find('a')]
    if 'arcsin' in term:
        if c=='':
            der = f"1/(1-{var}^2)^1/2"
        else:
            der = f"{c}/(1-{var}^2)^1/2"
    elif 'arccosec' in term:
        if c=='':
            der = f"-1/(|{var}|({var}^2-1))"
        else:
            der = f"-{c}/(|{var}|({var}^2-1))"
    elif 'arccos' in term:
        if c=='':
            der = f"-1/(1-{var}^2)^1/2"
        else:
            der = f"-{c}/(1-{var}^2)^1/2"
    elif 'arctan' in term:
        if c=='':
            der = f"1/(1+{var}^2)"
        else:
            der = f"{c}/(1+{var}^2)"
    elif 'arccot' in term:
        if c=='':
            der = f"-1/(1+{var}^2)"
        else:
            der = f"-{c}/(1+{var}^2)"
    elif 'arcsec' in term:
        if c=='':
            der = f"1/(|{var}|({var}^2-1))"
        else:
            der = f"{c}/(|{var}|({var}^2-1))"
    return der

def der_log(term, var):
    if 'ln' in term:
        der = f"1/{var}"
    else:
        base = term[term.find('g')+1 : term.find('(')].strip()
        if base == 'e':
            der = f"1/{var}"
        else:
            der = f"1/({var}ln({base}))"
    return der

def der_varexp(u, v):
    d = f"({v})*(ln({u}))"
    der = differentiate(d)
    return der

def differentiate(exp):
    t_dict, op_dict, f = get_terms(exp)
    t, op = list(t_dict), list(op_dict)
    t_der = []
    d_tmp= []
    y = ''

    for i in t:
        if wrt in i:
            LP = get_parenthesis(i)[-1]
            if t_dict[i][0] == 'Prod':
                u = i[1:t_dict[i][1]-1]
                v = i[t_dict[i][1]+2:-1]
                d = f"({differentiate(u)})*({v}) + ({differentiate(v)})*({u})"
                t_der.append(d)
            elif t_dict[i][0] == 'Quot':
                u = i[1:t_dict[i][1]-1]
                v = i[t_dict[i][1]+2:-1]
                d = f"(({differentiate(u)})*({v}) - ({differentiate(v)})*({u}))/(({v})^2)"
                t_der.append(d)
            elif t_dict[i] == 'VarExp':
                u = i[LP[0]+1:LP[1]]
                v = i[LP[2]+1:LP[3]]
                d = f"({i})*({der_varexp(u,v)})"
                t_der.append(d)
            elif LP==[] or i[LP[0]+1:LP[1]] == wrt:
                type = t_dict[i]
                if type == 'Pow':
                    d = der_pow(i, wrt)
                elif type == 'Linear':
                    d = der_linear(i)
                elif type == 'Exp':
                    d = der_exp(i, wrt)
                elif type == 'Trig':
                    d = der_trig(i, wrt)
                elif type == 'InverseTrig':
                    d = der_itrig(i, wrt)
                elif type == "Log":
                    d = der_log(i, wrt)
                t_der.append(d)   
            elif i[LP[0]+1:LP[1]] != wrt:
                type = t_dict[i]
                y = i[LP[0]+1:LP[1]]
                if t_dict[i] in ['InverseTrig', 'Trig', 'Log']:
                    outer = i.replace(y, 'y')
                else:
                    outer = i.replace(i[LP[0]:LP[1]+1], 'y' )
                
                if type == 'Pow':
                    outer_der = der_pow(outer, y)
                elif type == 'Linear':
                    outer_der = der_linear(outer)
                elif type == 'Exp':
                    outer_der = der_exp(outer, f"({y})")
                elif type == 'Trig':
                    outer_der = der_trig(outer, y)
                elif type == 'InverseTrig':
                    outer_der = der_itrig(outer, f"({y})")
                elif type == "Log":
                    outer_der = der_log(outer, f"({y})")
                d = f"{outer_der} * {differentiate(y)}"
                t_der.append(d)
        else:
            t_der.append('0')   
    if f == False:
        for i in range(len(t_der)):
            op_f = True
            if t_der[i] == '0' and i == len(t_der)-1:
                d_tmp.pop()
                continue
            elif t_der[i] == '0':
                continue
            if i == len(t_der)-1:
                op_f = False
            if t_der[i][0] == '-':
                l = d_tmp.pop()
                if l == '+':
                    d_tmp.append(t_der[i])
                else:
                    d_tmp.append('+')
                    d_tmp.append(t_der[i][1:])
            else:
                d_tmp.append(t_der[i])
            if op_f:
                d_tmp.append(op_dict[op[i]])
        der = ''.join(d_tmp)
    else:
        der = t_der[0]

    return der

def calc_val():
    pass

wrt = 'x'

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/differentiate', methods=['POST'])
def calculate():
    data = request.get_json()
    exp = data['expression']
    result = differentiate(exp)
    return jsonify({'result': result})