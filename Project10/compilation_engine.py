from tokenizer import Tokenizer


class CompilerToXML(object):
    def __init__(self, jack_file_object, output_file_object):
        self._tokenizer = Tokenizer(jack_file_object)
        self.out = output_file_object
        self.compile_class()

    def _advance_expect(self, target=None, target_type=None):
        self._tokenizer.advance()
        if not target and target_type:
            if self._tokenizer.current_token_type in target_type:
                return True
        elif target and not target_type:
            if self._tokenizer.current_token in target:
                return True
        else:
            return False

    def _expect(self, target=None, target_type=None):
        if not target and target_type:
            if self._tokenizer.current_token_type in target_type:
                return True
        elif target and not target_type:

            if self._tokenizer.current_token in target:
                return True
        else:
            return False

    def compile_class(self):
        try:
            print('in class')
            if self._advance_expect(target='class'):
                self.out.write('<class>\n')
                self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n')
            else:
                raise SyntaxError

            # Write className
            if self._advance_expect(target_type='IDENTIFIER'):
                self.out.write(f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
            else:
                raise SyntaxError

            if self._advance_expect(target='{'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
            else:
                raise SyntaxError

            # Need repeat
            self._tokenizer.advance()
            while self._tokenizer.current_token in ['static', 'field']:
                self.compile_class_var_dec()
                self._tokenizer.advance()

            # Need repeat
            while self._tokenizer.current_token in ['constructor', 'function', 'method']:
                self.compile_subroutine_dec()
                self._tokenizer.advance()

            if self._expect(target='}'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self.out.write('</class>\n')
            else:
                raise SyntaxError
            self._tokenizer.advance()

        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in compile class')

    def compile_class_var_dec(self):
        try:
            print('in class var dec')
            if self._expect(target=['static', 'field']):
                self.out.write('<classVarDec>\n')
                self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n')
            else:
                raise SyntaxError

            # Compile type
            self._tokenizer.advance()
            if self._tokenizer.current_token_type in ['KEYWORD', 'IDENTIFIER']:
                if self._expect(target=['int', 'char', 'boolean', self._tokenizer.current_token]):
                    self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n'
                                   if self._tokenizer.current_token_type is 'KEYWORD'
                                   else f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
            else:
                raise SyntaxError
            # End of type compilation

            # Write first varName
            if self._advance_expect(target_type='IDENTIFIER'):
                self.out.write(f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
            else:
                raise SyntaxError

            self._tokenizer.advance()
            while self._tokenizer.current_token is ',':
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self._tokenizer.advance()
                if self._expect(target_type='IDENTIFIER'):
                    self.out.write(f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
                else:
                    raise SyntaxError
                self._tokenizer.advance()

            if self._expect(target=';'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self.out.write('</classVarDec>\n')

        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in class var dec')

    def compile_subroutine_dec(self):
        try:
            print('in subroutine dec')
            if self._expect(target=['constructor', 'function', 'method']):
                self.out.write('<subroutineDec>\n')
                self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n')
            else:
                raise SyntaxError

            # Compile void|type
            self._tokenizer.advance()
            if self._tokenizer.current_token_type in ['KEYWORD', 'IDENTIFIER']:
                if self._expect(target=['int', 'char', 'boolean', 'void', self._tokenizer.current_token]):
                    self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n'
                                   if self._tokenizer.current_token_type is 'KEYWORD'
                                   else f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
            else:
                raise SyntaxError
            # End of type compilation

            # Write subroutine name
            if self._advance_expect(target_type='IDENTIFIER'):
                self.out.write(f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
            else:
                raise SyntaxError

            if self._advance_expect('('):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self.out.write('<parameterList>\n')
            else:
                raise SyntaxError
            self._tokenizer.advance()
            self.compile_parameter_list()

            if self._expect(')'):
                self.out.write('</parameterList>\n')
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
            else:
                raise SyntaxError

            self.compile_subroutine_body()

            self.out.write('</subroutineDec>\n')

        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in compile_subroutine_dec')

    def compile_parameter_list(self):
        try:
            print('in parameter list')
            if not self._expect(')'):
                # param is type: write
                if self._tokenizer.current_token_type in ['KEYWORD', 'IDENTIFIER']:
                    if self._expect(target=['int', 'char', 'boolean', self._tokenizer.current_token]):
                        self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n'
                                       if self._tokenizer.current_token_type is 'KEYWORD'
                                       else f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
                    # End of type compilation
                    # compile varName
                    if self._advance_expect(target_type='IDENTIFIER'):
                        self.out.write(f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
                    else:
                        raise SyntaxError

                    if self._advance_expect(target=','):
                        self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                        self._tokenizer.advance()
                        # print('calling compile param')
                        self.compile_parameter_list()

        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in compile_param_list')

    def compile_subroutine_body(self):
        try:
            print('in subroutine body')
            if self._advance_expect('{'):
                self.out.write('<subroutineBody>\n')
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
            else:
                raise SyntaxError

            self._tokenizer.advance()
            while self._expect(target='var'):
                self.compile_var_dec()
                self._tokenizer.advance()
                # Shooting out next

            self.compile_statements()

            if self._expect('}'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self.out.write('</subroutineBody>\n')
            else:
                raise SyntaxError

        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in subroutine body')

    def compile_var_dec(self):
        try:
            print('in var dec')
            if self._expect(target='var'):
                self.out.write('<varDec>\n')
                self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n')
            else:
                raise SyntaxError

            # Compile void|type
            self._tokenizer.advance()
            if self._tokenizer.current_token_type in ['KEYWORD', 'IDENTIFIER']:
                if self._expect(target=['int', 'char', 'boolean', 'void', self._tokenizer.current_token]):
                    # print(f'{self._tokenizer.current_token} isA {self._tokenizer.current_token_type}')
                    self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n'
                                   if self._tokenizer.current_token_type is 'KEYWORD'
                                   else f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
            else:
                raise SyntaxError
            # End of type compilation

            # Write first varName
            if self._advance_expect(target_type='IDENTIFIER'):
                self.out.write(f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
            else:
                raise SyntaxError
            # following vars
            self._tokenizer.advance()
            while self._tokenizer.current_token is ',':
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self._tokenizer.advance()
                if self._expect(target_type='IDENTIFIER'):
                    self.out.write(f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
                else:
                    raise SyntaxError
                self._tokenizer.advance()

            if self._expect(';'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self.out.write('</varDec>\n')

        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in compile var dec')

    def compile_statements(self):  # Does not self-advance, but advances at the end
        try:
            print('in statements')
            self.out.write('<statements>\n')
            while self._expect(target=['do', 'let', 'while', 'return', 'if']):
                print(f'statements looping {self._tokenizer.current_token}')
                if self._expect('do'):
                    self.compile_do()
                    self._tokenizer.advance()
                elif self._expect('let'):
                    self.compile_let()
                    self._tokenizer.advance()
                elif self._expect('while'):
                    self.compile_while()
                    self._tokenizer.advance()
                elif self._expect('return'):
                    self.compile_return()
                    self._tokenizer.advance()

                elif self._expect('if'):
                    self.compile_if()
            self.out.write('</statements>\n') # Shoot next token to subroutineCall while
        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in statements')

    def compile_do(self):
        try:
            print('in Do')
            self.out.write('<doStatement>\n')
            self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n')
            # Subroutine Call
            if self._advance_expect(target_type='IDENTIFIER'):
                self.out.write(f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
            else:
                raise SyntaxError

            self._tokenizer.advance()
            if self._expect('('):  #subroutineName(expressionList)
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self.out.write('<expressionList>\n')
            elif self._expect(target='.'): #(className|varName).subroutineName(expressionList)
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                if self._advance_expect(target_type='IDENTIFIER'):
                    self.out.write(f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
                else:
                    raise SyntaxError
                if self._advance_expect(target='('):
                    self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                    self.out.write('<expressionList>\n')
                else:
                    raise SyntaxError

            self._tokenizer.advance()
            self.compile_expression_list()

            if self._expect(')'):
                self.out.write('</expressionList>\n')
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
            else:
                raise SyntaxError
            # End subroutine Call

            if self._advance_expect(';'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self.out.write('</doStatement>\n')
            else:
                raise SyntaxError

        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in compile_do')

    def compile_let(self):
        try:
            print('in let')
            self.out.write('<letStatement>\n')
            self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n')
            # varName
            if self._advance_expect(target_type='IDENTIFIER'):
                self.out.write(f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
            else:
                raise SyntaxError
            # with or not '['
            if self._advance_expect('['):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')

                self._tokenizer.advance()
                self.compile_expression()

                if self._expect(']'):
                    self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                    self._tokenizer.advance()
                else:
                    raise SyntaxError

            if self._expect('='):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
            else:
                raise SyntaxError

            self._tokenizer.advance()
            self.compile_expression()

            if self._expect(';'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self.out.write('</letStatement>\n')
            else:
                raise SyntaxError

        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in compile_let')

    def compile_while(self):
        try:
            print('in while')
            self.out.write('<whileStatement>\n')
            self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n')
            if self._advance_expect('('):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
            else:
                raise SyntaxError

            self._tokenizer.advance()
            self.compile_expression()

            if self._expect(')'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
            else:
                raise SyntaxError

            if self._advance_expect('{'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
            else:
                raise SyntaxError

            self._tokenizer.advance()
            self.compile_statements()

            if self._expect('}'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self.out.write('</whileStatement>\n')
            else:
                raise SyntaxError

        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in compile_while')

    def compile_return(self):
        try:
            print('in return')
            self.out.write('<returnStatement>\n')
            self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n')
            if not self._advance_expect(';'):
                self.compile_expression()
            if self._expect(';'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self.out.write('</returnStatement>\n')
            else:
                raise SyntaxError

        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in compile_return')

    def compile_if(self):
        try:
            print('in if')
            self.out.write('<ifStatement>\n')
            self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n')

            if self._advance_expect('('):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
            else:
                raise SyntaxError

            self._tokenizer.advance()
            self.compile_expression()

            if self._expect(')'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
            else:
                raise SyntaxError

            if self._advance_expect('{'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
            else:
                raise SyntaxError

            self._tokenizer.advance()
            self.compile_statements()

            if self._expect('}'):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
            else:
                raise SyntaxError

            if self._advance_expect(target='else'):
                self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n')
                if self._advance_expect('{'):
                    self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                else:
                    raise SyntaxError

                self._tokenizer.advance()
                self.compile_statements()

                if self._expect('}'):
                    self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                    self.out.write('</ifStatement>\n')
                    self._tokenizer.advance()
                else:
                    raise SyntaxError
            else:
                self.out.write('</ifStatement>\n')
        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in compile_if')

    def compile_expression(self):
        # does not advance by itself
        print('in compile expression')
        self.out.write('<expression>\n')
        # self._tokenizer.advance()
        self.compile_term()
        # shoots the next token
        if self._expect(target=list('+-*/&|<>=')):
            self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
            self._tokenizer.advance()
            self.compile_term()
        self.out.write('</expression>\n')

    def compile_term(self):
        try:
            print('in compile term')
            # does not advance by itself
            self.out.write('<term>\n')
            if self._expect(target_type='INT_CONST'):
                self.out.write(f'<integerConstant> {self._tokenizer.int_value()} </integerConstant>\n')
                self._tokenizer.advance()
            elif self._expect(target_type='STRING_CONST'):
                self.out.write(f'<stringConstant> {self._tokenizer.string_value()} </stringConstant>\n')
                self._tokenizer.advance()
                print(f'after string, current token is {self._tokenizer.current_token}')
            elif self._expect(target_type='KEYWORD'):
                self.out.write(f'<keyword> {self._tokenizer.keyword()} </keyword>\n')
                self._tokenizer.advance()
            # (expression)
            elif self._expect(target='('):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self._tokenizer.advance()
                self.compile_expression()
                if self._expect(')'):
                    self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self._tokenizer.advance()
            # unaryOP term
            elif self._expect(target=list('-~')):
                self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                self._tokenizer.advance()
                self.compile_term()
            # varName
            elif self._expect(target_type='IDENTIFIER'):
                print('term is identifier')
                self.out.write(f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
                self._tokenizer.advance()
                # varName [ expression ]
                if self._expect('['):
                    self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                    self._tokenizer.advance()
                    self.compile_expression()
                    if self._expect(']'):
                        self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                    self._tokenizer.advance()
                # subroutineCall
                elif self._expect(list('(.')):
                    if self._expect(target='('):  # subroutineName (expressionList)
                        self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                        self.out.write('<expressionList>\n')
                    elif self._expect(target='.'):  # (className|varName).subroutineName(expressionList)
                        self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                        if self._advance_expect(target_type='IDENTIFIER'):
                            self.out.write(f'<identifier> {self._tokenizer.identifier()} </identifier>\n')
                        else:
                            raise SyntaxError
                        if self._advance_expect(target='('):
                            self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                            self.out.write('<expressionList>\n')
                        else:
                            raise SyntaxError

                    self._tokenizer.advance()
                    self.compile_expression_list()

                    if self._expect(')'):
                        self.out.write('</expressionList>\n')
                        self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                        self._tokenizer.advance()
                    else:
                        raise SyntaxError
                    # End subroutine Call
            else:
                raise SyntaxError
            self.out.write('</term>\n')

        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in term')
        # shoots next token

    def compile_expression_list(self):
        # does not advance by it self
        try:
            if not self._expect(')'):
                print('in expression list')
                self.compile_expression()

                if self._expect(target=','):
                    self.out.write(f'<symbol> {self._tokenizer.symbol()} </symbol>\n')
                    self._tokenizer.advance()
                    self.compile_expression_list()

        except SyntaxError:
            print(f'Syntax error at {self._tokenizer.current_token} in compile_param_list')
        # shoots next token




