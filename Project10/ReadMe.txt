The submission is a working TOKENIZER, I am still working on Compile Engine.
To test the tokenizer, use "python3 main.py <file_path>" in command line.
I used "pathlib" module in processing the file path, but I am not sure still
whether it works on Windows or not. PLEASE USE A MAC TO TEST.

if <file_path> is a file, in the same parent folder, a "<file_name>T.xml" will generate containing
tokenize-ed file.
else if it is a directory, all *.jack file under the dir will generate "<file_name>T.xml"

tokenizer.py has method described as the textbook, and also a "tag_adder" as a generator to add tags
to each token.
It is recommended to use main, instead of using tokenizer.py alone.

I will submit compilation_engine and a working, fully functioning main.py ASAP.