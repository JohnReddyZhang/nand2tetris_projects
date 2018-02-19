This submission is a fine-tuned (I suppose, at least it works with all test files) syntax analyzer.
To test the analyzer, use "python3 main.py <file_path>" in command line.

I used "pathlib" module in processing the file path, but I am not sure still
whether it works on Windows or not. PLEASE USE A MAC TO TEST.

If <file_path> is a file, in the same parent folder, a "<file_name>.xml" will be generated containing translated text.
Else if it is a directory, all *.jack file under the dir will generate corresponding "<file_name>.xml".

tokenizer.py has method described as methods of 'JackTokenizer' in the textbook. And 'compile_engine.py' 'CompilationEngine'.
It is recommended to use main.py though, instead of using submodules alone.

Note:
Actually you could also make main.py work in interactive mode, by changing:
# input_path = input('input path:')
input_path = sys.argv[1]

to

input_path = input('input path:')
# input_path = sys.argv[1]

and importing main: import main
Interactive mode does not support cmd line arguments, as far as I found out.