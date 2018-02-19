import sys
import pathlib
from compilation_engine import CompilerToXML


class Constructor(object):
    def __init__(self, path):
        self.path = pathlib.Path(path)

    def run(self):
        try:
            if self.path.is_file():
                with open(self.path, mode='r') as source:
                    # Out path for tokenizer only
                    out = open(self.path.parent.joinpath(
                        f"{self.path.name.replace(self.path.suffix, '')}.xml"), mode='w')
                    CompilerToXML(source, out)
                    out.close()
            elif self.path.is_dir():
                for singlefile in self.path.glob('*.jack'):
                    with open(singlefile, mode='r') as source:
                        # Out path for tokenizer only
                        out = open(singlefile.parent.joinpath(
                            f"{singlefile.name.replace(singlefile.suffix, '')}.xml"), mode='w')
                        CompilerToXML(source, out)
                        print(f'Finished {source.name}')
                        out.close()
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            print(f'Did not find {self.path}, Please try again.')


# input_path = input('input path:')
input_path = sys.argv[1]
test = Constructor(input_path)
test.run()
