import sys


class CodeTranslation(object):
    """The stack's command list and translator."""

    COMMAND_LIST = {'sub': '@SP\n'
                           'AM=M-1\n'
                           'D=M\n'
                           'A=A-1\n'
                           'M=M-D\n',

                    'add': '@SP\n'
                           'AM=M-1\n'
                           'D=M\n'
                           'A=A-1\n'
                           'M=M+D\n',

                    'neg': '@SP\n'
                           'A=M-1\n'
                           'M=-M\n',

                    'not': '@SP\n'
                           'A=M-1\n'
                           'M=!M\n',

                    'and': '@SP\n'
                           'AM=M-1\n'
                           'D=M\n'
                           'A=A-1\n'
                           'M=D&M\n',

                    'or': '@SP\n'
                          'AM=M-1\n'
                          'D=M\n'
                          'A=A-1\n'
                          'M=D|M\n',

                    'gt': '@SP\n'
                          'AM=M-1\n'
                          'D=M\n'
                          'A=A-1\n'
                          'D=M-D\n'
                          '@FALSE_SEQ\n'
                          'D;JLE\n'
                          '@SP\n'
                          'A=M-1\n'
                          'M=-1\n'
                          '@CONTINUE_SEQ\n'
                          '0;JMP\n'
                          '(FALSE_SEQ)\n'
                          '@SP\n'
                          'A=M-1\n'
                          'M=0\n'
                          '(CONTINUE_SEQ)\n',

                    'lt': '@SP\n'
                          'AM=M-1\n'
                          'D=M\n'
                          'A=A-1\n'
                          'D=M-D\n'
                          '@FALSE_SEQ\n'
                          'D;JGE\n'
                          '@SP\n'
                          'A=M-1\n'
                          'M=-1\n'
                          '@CONTINUE_SEQ\n'
                          '0;JMP\n'
                          '(FALSE_SEQ)\n'
                          '@SP\n'
                          'A=M-1\n'
                          'M=0\n'
                          '(CONTINUE_SEQ)\n',

                    'eq': '@SP\n'
                          'AM=M-1\n'
                          'D=M\n'
                          'A=A-1\n'
                          'D=M-D\n'
                          '@TRUE_SEQ\n'
                          'D;JEQ\n'
                          '@SP\n'
                          'A=M-1\n'
                          'M=0\n'
                          '@CONTINUE_SEQ\n'
                          '0;JMP\n'
                          '(TRUE_SEQ)\n'
                          '@SP\n'
                          'A=M-1\n'
                          'M=-1\n'
                          '(CONTINUE_SEQ)\n',

                    'push constant':
                        '@X\n'
                        'D=A\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n',

                    'push argument':
                        '@ARG\n'
                        'D=M\n'
                        '@X\n'
                        'A=D+A\n'
                        'D=M\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n',

                    'push local':
                        '@LCL\n'
                        'D=M\n'
                        '@X\n'
                        'A=D+A\n'
                        'D=M\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n',

                    'push static':
                        '@X\n'
                        'D=M\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n',

                    'push this':
                        '@THIS\n'
                        'D=M\n'
                        '@X\n'
                        'A=D+A\n'
                        'D=M\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n',

                    'push that':
                        '@THAT\n'
                        'D=M\n'
                        '@X\n'
                        'A=D+A\n'
                        'D=M\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n',

                    'push pointer':
                        '@X\n'
                        'D=A\n'
                        '@3\n'
                        'A=D+A\n'
                        'D=M\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n',

                    'push temp':
                        '@X\n'
                        'D=A\n'
                        '@5\n'
                        'A=D+A\n'
                        'D=M\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n',

                    'pop argument':
                        '@ARG\n'
                        'D=M\n'
                        '@X\n'
                        'D=D+A\n'
                        '@R13\n'
                        'M=D\n'
                        '@SP\n'
                        'AM=M-1\n'
                        'D=M\n'
                        '@R13\n'
                        'A=M\n'
                        'M=D\n',

                    'pop local':
                        '@LCL\n'
                        'D=M\n'
                        '@X\n'
                        'D=D+A\n'
                        '@R13\n'
                        'M=D\n'
                        '@SP\n'
                        'AM=M-1\n'
                        'D=M\n'
                        '@R13\n'
                        'A=M\n'
                        'M=D\n',

                    'pop static':
                        '@X\n'
                        'D=M\n'
                        '@R13\n'
                        'M=D\n'
                        '@SP\n'
                        'AM=M-1\n'
                        'D=M\n'
                        '@R13\n'
                        'A=M\n'
                        'M=D\n',

                    'pop this':  # Possibly wrong
                        '@THIS\n'
                        'D=M\n'
                        '@X\n'
                        'D=D+A\n'
                        '@R13\n'
                        'M=D\n'
                        '@SP\n'
                        'AM=M-1\n'
                        'D=M\n'
                        '@R13\n'
                        'A=M\n'
                        'M=D\n',

                    'pop that':
                        '@THAT\n'
                        'D=M\n'
                        '@X\n'
                        'D=D+A\n'
                        '@R13\n'
                        'M=D\n'
                        '@SP\n'
                        'AM=M-1\n'
                        'D=M\n'
                        '@R13\n'
                        'A=M\n'
                        'M=D\n',

                    'pop pointer':
                        '@X\n'
                        'D=A\n'
                        '@3\n'
                        'D=D+A\n'
                        '@R13\n'
                        'M=D\n'
                        '@SP\n'
                        'AM=M-1\n'
                        'D=M\n'
                        '@R13\n'
                        'A=M\n'
                        'M=D\n',

                    'pop temp':
                        '@X\n'
                        'D=A\n'
                        '@5\n'
                        'D=D+A\n'
                        '@R13\n'
                        'M=D\n'
                        '@SP\n'
                        'AM=M-1\n'
                        'D=M\n'
                        '@R13\n'
                        'A=M\n'
                        'M=D\n',

                    }

    def __init__(self, pure_file):
        self._file = pure_file
        out_file = self._file.get_filename().rsplit('.', maxsplit=1)[0] + '.asm'
        self.out_handle = open(out_file, 'w')

    def write_code(self):
        # self.out_handle.truncate()
        sequence = 0
        for line in self._file.get_lines():
            splited_line = line.rsplit(' ', maxsplit=1)
            if len(splited_line) == 1:
                if splited_line[0] in ['add', 'sub', 'neg', 'not', 'and', 'or']:
                    asm_code = self.COMMAND_LIST[splited_line[0]]
                    self.out_handle.write(asm_code)
                else:
                    asm_code = self.COMMAND_LIST[splited_line[0]]
                    asm_code = asm_code.replace('_SEQ', '_'+str(sequence))
                    self.out_handle.write(asm_code)
                    sequence += 1
            elif len(splited_line) == 2:
                asm_code = self.COMMAND_LIST[splited_line[0]]
                if 'static' in splited_line[0]:
                    asm_code = asm_code.replace('X',
                                                line.split(' ', maxsplit=1)[1]
                                                .replace('static', self._file.get_filename()).replace(' ', '.'))
                else:
                    asm_code = asm_code.replace('X', splited_line[1])
                self.out_handle.write(asm_code)

        self.out_handle.write('(END)\n'
                              '@END\n'
                              '0;JMP')
        print('File Writing Completed')

    def close_file(self):
        self.out_handle.close()
        print('Output file finished')


class Remover(object):
    """parsing the file and remove comments, spaces."""

    def __init__(self, unsolved_file):
        self.file_name = unsolved_file
        self.f_handle = open(self.file_name, 'r')
        self._lines = []

    def remove_comments(self):
        for line in self.f_handle.readlines():
            if line.isspace() or line.startswith('//'):
                pass
            else:
                cleared_line = line.rstrip('\n').split('//', 1)[0]
                self._lines.append(cleared_line)

    def get_filename(self):
        return self.file_name

    def get_lines(self):
        for line in self._lines:
            yield line

    def close_file(self):
        self.f_handle.close()
        print('Source file closed')


def run(file_name):
    remover = Remover(file_name)
    remover.remove_comments()
    code_translation = CodeTranslation(remover)
    code_translation.write_code()
    remover.close_file()
    code_translation.close_file()


file_path = sys.argv[1]
run(file_path)
