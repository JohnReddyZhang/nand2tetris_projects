import sys
import os.path

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

                    # Following table are for Project 8:
                    'label':
                        '(X)\n',

                    'goto':
                        '@X\n'
                        '0;JMP\n',

                    'if-goto':
                        '@SP\n'
                        'AM=M-1\n'
                        'D=M\n'
                        '@X\n'
                        'D;JNE\n',

                    # Function operations:
                    'function':
                        '(_FUNCTION)\n'
                        '@N_LCL\n'
                        'D=A\n'
                        '@_FUNCTION_k\n'
                        'M=D\n'
                        '(_FUNCTION_LOOP)\n'
                        '@_FUNCTION_k\n'
                        'D=M\n'
                        '@_FUNCTION_END\n'
                        'D;JLE\n'
                        '@0\n'
                        'D=A\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n'
                        '@_FUNCTION_k\n'
                        'M=M-1\n'
                        '@_FUNCTION_LOOP\n'
                        '0;JMP\n'
                        '(_FUNCTION_END)\n',


                    'call':
                        '@RETURN_FUNCTION_X\n'  # Return Address 
                        'D=A\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n'
                        
                        '@LCL\n'  # Save local at tempLCL
                        'D=M\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n'
                        
                        '@ARG\n'  # Save ARG at tempARG 
                        'D=M\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n'
                        
                        '@THIS\n'  # This
                        'D=M\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n'
                        
                        '@THAT\n'  # That
                        'D=M\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n'
                        
                        '@SP\n'  # Reset ARG
                        'D=M\n'
                        '@N_ARG\n'  # number of args
                        'D=D-A\n'
                        '@5\n'
                        'D=D-A\n'
                        '@ARG\n'
                        'M=D\n'
                        
                        '@SP\n'  # Reset LCL to SP value
                        'D=M\n'
                        '@LCL\n'
                        'M=D\n'
                        
                        '@_FUNCTION\n'
                        '0;JMP\n'
                        '(RETURN_FUNCTION_X)\n',  #

                    'return':
                        '@LCL\n'  # Frame = lcl
                        'D=M\n'
                        '@FRAME\n'
                        'M=D\n'
                        
                        '@FRAME\n'  # Ret = (frame - 5) //frame m is the m of lcl
                        'D=M\n'
                        '@5\n'  
                        'D=D-A\n'
                        'A=D\n'  # A at frame - 5
                        'D=M\n'
                        '@RET\n'
                        'M=D\n'
                        
                        '@SP\n'  # ARG = pop() (output value at arg)
                        'A=M-1\n'
                        'D=M\n'
                        '@ARG\n'
                        'A=M\n'
                        'M=D\n'
                    
                        '@ARG\n'  # SP = ARG + 1
                        'D=M\n'
                        '@SP\n'
                        'M=D+1\n'
                    
                        '@FRAME\n'  # That = frame -1
                        'AM=M-1\n'
                        'D=M\n'
                        '@THAT\n'
                        'M=D\n'
                    
                        '@FRAME\n'  # New Frame, = frame - 1, resume this
                        'AM=M-1\n'
                        'D=M\n'
                        '@THIS\n'
                        'M=D\n'

                        '@FRAME\n'  # resume arg
                        'AM=M-1\n'
                        'D=M\n'
                        '@ARG\n'
                        'M=D\n'

                        '@FRAME\n'  # resume lcl
                        'AM=M-1\n'
                        'D=M\n'
                        '@LCL\n'
                        'M=D\n'
                    
                        '@RET\n'
                        'A=M\n'
                        '0;JMP\n'

                    }

    def __init__(self, pure_file=None, path=None, asm_filename=None):
        self.PATH = path
        self._asm_filename = asm_filename
        self._file = pure_file
        self._sequence = 0  # Counter for everything
        self.out_handle = None

    def set_file_source(self, pure_file):
        self._file = pure_file

    def set_asm_filename(self, asm_filename):
        self._asm_filename = asm_filename

    def open_file(self):
        out_file = self.PATH + '/' + self._asm_filename
        self.out_handle = open(out_file, 'w')

    def write_init(self):
        # print('.asm file path: '+self.PATH+'/'+self._asm_filename)
        out_file = self.PATH + '/' + self._asm_filename
        self.out_handle = open(out_file, 'w')
        init_code = '@256\nD=A\n@SP\nM=D\n'
        self.out_handle.write(init_code)
        # call_sys_init = self.COMMAND_LIST['call'].replace('_X', '').replace('_FUNCTION', 'sys.init').replace('N_ARG', '0')
        # self.out_handle.write(call_sys_init)

    def write_code(self):
        for line in self._file.get_lines():
            if 'function' in line or 'call' in line or 'return' in line:
                split_line = line.split(' ')
                asm_code = self.COMMAND_LIST[split_line[0]]
                if split_line[0] == 'function':
                    asm_code = asm_code.replace('_FUNCTION', split_line[1])
                    asm_code = asm_code.replace('N_LCL', str(split_line[2]))
                elif split_line[0] == 'call':
                    asm_code = asm_code.replace('_X', '_'+str(self._sequence))
                    asm_code = asm_code.replace('_FUNCTION', split_line[1])
                    asm_code = asm_code.replace('N_ARG', split_line[2])
                    self._sequence += 1
                self.out_handle.write(asm_code)

            else:
                split_line = line.rsplit(' ', maxsplit=1)
                if len(split_line) == 1:
                    if split_line[0] in ['add', 'sub', 'neg', 'not', 'and', 'or']:
                        asm_code = self.COMMAND_LIST[split_line[0]]
                        self.out_handle.write(asm_code)
                    else:
                        asm_code = self.COMMAND_LIST[split_line[0]]
                        asm_code = asm_code.replace('_SEQ', '_'+str(self._sequence))
                        self.out_handle.write(asm_code)
                        self._sequence += 1
                elif len(split_line) == 2:
                    asm_code = self.COMMAND_LIST[split_line[0]]
                    if 'static' in split_line[0]:
                        asm_code = asm_code.replace('X',
                                                    line.split(' ', maxsplit=1)[1]
                                                    .replace('static', self._file.get_filename()).replace(' ', '.'))
                    else:
                        asm_code = asm_code.replace('X', split_line[1])
                    self.out_handle.write(asm_code)

    def end_file(self):
        self.out_handle.write('(END)\n'
                              '@END\n'
                              '0;JMP')
        print('File Writing Completed')
        self.out_handle.close()
        print('Output file finished')


class Remover(object):
    """parsing the file and remove comments, spaces."""
    def __init__(self, unsolved_file_name, path):
        self.PATH = path
        self.file_name = unsolved_file_name
        self.f_handle = open(self.PATH + '/' + self.file_name, 'r')
        self._lines = []

    def remove_comments(self):
        for line in self.f_handle.readlines():
            if line.isspace() or line.startswith('//'):
                pass  # Write nothing
            else:
                cleared_line = line.rstrip('\n').split('//', 1)[0].strip()
                self._lines.append(cleared_line)

    def get_filename(self):
        return self.file_name

    def get_lines(self):
        for line in self._lines:
            yield line

    def close_file(self):
        self.f_handle.close()
        print('Source file closed')


class Main(object):

    def __init__(self):
        self.PATH = None

    def run(self, path):
        self.PATH = path
        abs_path = os.path.abspath(self.PATH)
        # print('file is at:' + abs_path)
        if os.path.isdir(self.PATH):
            split_name = abs_path.rsplit('/', 1)[1]
            code_translation = CodeTranslation(path=self.PATH)
            print(f'File Path is {self.PATH}')
            code_translation.set_asm_filename(f'{split_name}.asm')
            code_translation.write_init()
            vm_files = [files for files in os.listdir(self.PATH) if files.endswith('.vm')]
            if 'Sys.vm' in vm_files:
                sys_index = vm_files.index('Sys.vm')
                vm_files[sys_index], vm_files[0] = vm_files[0], vm_files[sys_index]  # method inspired by https://stackoverflow.com/questions/2493920/how-to-switch-position-of-two-items-in-a-python-list
                # vm_files = [vm_files[0]]+sorted(vm_files[1:])
            for file_name in vm_files:
                print(f'Parsing {file_name}')
                remover = Remover(file_name, self.PATH)
                remover.remove_comments()
                code_translation.set_file_source(remover)
                code_translation.write_code()
            code_translation.end_file()
        else:
            self.PATH = path
            abs_path = os.path.abspath(self.PATH)
            # print('file is at'+abs_path)
            split_path, split_name = abs_path.rsplit('/', 1)
            # print(split_name.rsplit('.', maxsplit=1)[0])
            remover = Remover(split_name, split_path)
            remover.remove_comments()
            code_translation = CodeTranslation(remover, split_path, split_name.rsplit('.', maxsplit=1)[0]+'.asm')
            code_translation.write_init()
            code_translation.write_code()
            remover.close_file()
            code_translation.end_file()


file_path = sys.argv[1]
main = Main()
main.run(file_path)
