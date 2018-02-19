import re

_SYMBOL_LIST = '{}()\[\].,;+\-*/&|<>=~'

_SYMBOL_LIST_PATTERN = r'[{}()\[\].,;+\-*/&|<>=~]'
_STRING_CONST_PATTERN = r'\"[^\"]*\"'
_IDENTIFIER_AND_KEYWORDS = r'\w+'
_KEYWORD_LIST = ['class', 'constructor', 'function',
                 'method', 'field', 'static', 'var',
                 'int', 'char', 'boolean', 'void',
                 'true', 'false', 'null', 'this', 'let', 'do',
                 'if', 'else', 'while', 'return']


class Tokenizer(object):
    def __init__(self, jack_file_object):
        self.source = jack_file_object
        self.purified_tokens = []
        self.current_token = None
        self.current_token_type = None
        self._has_more_tokens = True
        self.generate_token = self.tokenizer()

    def content_reader(self):
        for original_line in self.source:
            if not original_line.isspace():
                yield original_line.rstrip()

    def comment_remover(self):
        is_comment = re.compile(r'//|/\*.*|/\*\*.*|.*\*/')
        has_double_slash = re.compile('//')
        for non_clear_line in self.content_reader():
            if is_comment.match(non_clear_line):
                pass
            elif non_clear_line.startswith(' * '):
                pass
            else:
                yield has_double_slash.split(non_clear_line)[0]

    # Yields tokens one by one
    def tokenizer(self):
        pattern = '|'.join([_SYMBOL_LIST_PATTERN, _STRING_CONST_PATTERN, _IDENTIFIER_AND_KEYWORDS])
        for cleared_line in self.comment_remover():
            for raw_token in re.compile(pattern).findall(cleared_line):
                self.purified_tokens.append(raw_token)
                yield raw_token

    def has_more_tokens(self):
        return self._has_more_tokens

    def advance(self):
        try:
            self.current_token = next(self.generate_token)
            self.current_token_type = self.token_type_detector()
            print(f'Current token set to {self.current_token}')
        except StopIteration:
            print('No more tokens in queue')
            self._has_more_tokens = False
            self.current_token = None
            self.current_token_type = None

    def token_type_teller(self):
        return self.current_token_type

    def token_type_detector(self):
        try:
            if self.current_token in _KEYWORD_LIST:
                return 'KEYWORD'
            elif self.current_token in _SYMBOL_LIST:
                return 'SYMBOL'
            elif self.current_token.startswith('"'):
                return 'STRING_CONST'
            elif self.current_token.isdecimal():
                return 'INT_CONST'
            elif re.match(r'[\w_]+', self.current_token) and not self.current_token[0].isdigit():
                return 'IDENTIFIER'
            else:
                raise ValueError
        except ValueError:
            print(f'Illegal token detected: current token:{self.current_token}')
            self.current_token_type = None
            return self.current_token_type

    def keyword(self):
        return self.current_token

    def symbol(self):
        return '&lt;' if self.current_token == '<' else ('&gt;' if self.current_token == '>'
                                                         else ('&quot;' if self.current_token == '"'
                                                               else ('&amp;' if self.current_token == '&'
                                                                     else self.current_token)))

    def identifier(self):
        return self.current_token

    def int_value(self):
        return self.current_token

    def string_value(self):
        return self.current_token.strip('"')

    # def tag_adder(self):
    #     try:
    #         while self.has_more_tokens():
    #             self.advance()
    #             if self.current_token_type == 'STRING_CONST':
    #                 yield '<stringConstant> {} </stringConstant>'.format(self.string_value().strip('"'))
    #             elif self.current_token_type == 'KEYWORD':
    #                 yield f'<keyword> {self.keyword()} </keyword>\n'
    #             elif self.current_token_type == 'SYMBOL':
    #                 yield '<symbol> {} </symbol>'.format(self.symbol())
    #             elif self.current_token_type == 'INT_CONST':
    #                 yield f'<integerConstant> {self.int_value()} </integerConstant>'
    #
    #             elif self.current_token_type == 'IDENTIFIER':
    #                 yield f'<identifier> {self.identifier()} </identifier>\n'
    #             else:
    #                 raise ValueError
    #     except ValueError:
    #         print(f'No Match on {self.current_token}')

    # This function is replaced with a better version
    # def _tag_adder(self):
    #     try:
    #         for token in self.generate_token:
    #             if token.startswith('"'): # is a string constant
    #                 yield '<stringConstant> {} </stringConstant>'.format(token.strip('"'))
    #             elif token in _KEYWORD_LIST:
    #                 yield f'<keyword> {token} </keyword>'
    #             elif token in _SYMBOL_LIST:
    #                 yield '<symbol> {} </symbol>'.format('&lt;' if token == '<'
    #                                                      else ('&gt;' if token == '>'
    #                                                      else ('&quot;' if token == '"'
    #                                                      else ('&amp;' if token == '&' else token))))
    #             elif token.isdecimal():
    #                 yield f'<integerConstant> {token} </integerConstant>'
    #
    #             elif re.match(r'[\w_]+', token) and not token[0].isdigit():
    #                 yield f'<identifier> {token} </identifier>'
    #             else:
    #                 raise ValueError
    #     except ValueError:
    #         print(f'No Match on {token}')

    def close(self):
        self.source.close()
