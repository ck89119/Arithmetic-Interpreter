INTEGER, PLUS, MINUS, MUL, DIV, LPAR, RPAR, EOF = 'INTERGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAR', 'RPAR', 'EOF'

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, MUL, DIV, EOF
        self.type = type
        self.value = value
   
    def __str__(self):
        return 'Token({type}, {value})'.format(
            type = self.type,
            value = self.value
            )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    """docstring for Lexer"""
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos]
    
    def error(self):
        raise Exception('Invalid character')

    def next_char(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_space(self):
        while self.current_char is not None and self.current_char == ' ':
            self.next_char()
    
    def get_integer(self):
        result = 0
        while self.current_char is not None and self.current_char.isdigit():
            result = result * 10 + (int)(self.current_char)
            self.next_char()
        return result

    def get_next_token(self):
        """ Tokenizer
        
        """
        while self.current_char is not None:
            if self.current_char == ' ':
                self.skip_space()
            elif self.current_char == '+':
                self.next_char()
                return Token(PLUS, '+')
            elif self.current_char == '-':
                self.next_char()
                return Token(MINUS, '-')
            elif self.current_char == '*':
                self.next_char()
                return Token(MUL, '*')
            elif self.current_char == '/':
                self.next_char()
                return Token(DIV, '/')
            elif self.current_char == '(':
                self.next_char()
                return Token(LPAR, '(')
            elif self.current_char == ')':
                self.next_char()
                return Token(RPAR, ')')
            elif self.current_char.isdigit():
                return Token(INTEGER, self.get_integer())
            else:
                self.error()

        return Token(EOF, None)


class Interpreter(object):
    """docstring for Interpreter"""
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid character')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
   
    def item(self):
        result = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.factor()
        return result

    def factor(self):
        token = self.current_token
        #print(token)
        if token.type == INTEGER:
            result = token.value
            self.eat(INTEGER)
        elif token.type == LPAR:
            self.eat(LPAR)
            result = self.expr()
            self.eat(RPAR)
        else:
            self.error()

        return result

    def expr(self):
        """ Arithmetic expression parser
            
        expr: item ((PLUS | MINUS) item)*
        item: factor ((MUL | DIV) factor)*
        factor: INTEGER
        """       
        #print("expr start")
        result = self.item()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.item()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.item()

        #print("expr end")
        return result
        

def main():
    while True:
        try:
            text = raw_input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
