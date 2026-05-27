Welcome to the Derivative Calculator!

OVERVIEW:
Using this calculator, you would be able to differentiate (almost) all types of functions you find in the wild. The calculator also supports the use of Product rule, Quotient rule and Chain rule automatically.

HOW IT WORKS:
this is the v1.0 of the calculator and it currently has a web UI which is connected to a python backend. In python, the differentiation is done using string slicing and recursion. First, the expression is taken through the get_terms() function which calls other functions to return an ordered dictionary of each term in the expression as the key, and the value as the type of the term (identified by the get_type() function). Then, that dictionary is passed onto the main differentiate() function where differentiation takes place through recursion (calling itself within the function). Recursion is what makes things like chain rule and nested function derivatives possible.

SUPPORTED FUNCTIONS:
1. Power Functions (x^2, 2x^3, etc.)
2. Exponential Functions (2^x, e^x, etc.)
3. Variable Exponential functions (x^x, (sin(x))^(3x), etc.)
4. Trigonometric Functions (sin(x), cos(x^2), etc.)
5. Inverse Trigonometric Functions (arcsin(x), arccos(x), etc,)
6. Logarithmic Functions (ln(x), log10(x))
AND A COMBINATION OF ALL!

SYNTAX RULES:
1. Pow, Exp & VarExp: use '^' as operator ( (2x+1)^2, e^(3x+2), (2x+1)^(3x) )
2. Trig, InvTrig & Log: variable should be in brackets (sin(x), arccos(x), ln(x))
3. For logbasex, write it as "logbase(x)" (log10(x), log2(x))
4. Prod rule: use '*' identifier between consecutive terms ((e^x)*(sin(x)))
5. Quot rule: use '/' identifier between consecutive terms ((e^x)/(sin(x)))
NOTE: '*' AND '/' ARE SPECIAL IDENTIFIERS AND SHOULD ONLY BE USED IN CASES SPECIFIED ABOVE
6. Prod, Quot, VarExp: Consecutive terms to be enclosed in parenthesis.
example:- (sin(x))*(x^2), (2x)^(x^2), (x^2)/((2x+1))
7. Do not use fractions, only use decimals.

LOCAL SETUP:
1. Clone the repository
2. Create a virtual environment and activate it
3. Run `pip install -r requirements.txt`
4. Run `python main.py`
5. Open `http://127.0.0.1:5000` in your browser

LIVE DEMO:
https://derivative-calculator-g91r.onrender.com/

(made by: r10m-10)