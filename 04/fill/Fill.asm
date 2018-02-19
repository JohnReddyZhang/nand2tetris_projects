// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
@KBD
D=A
@screenend
M=D

@SCREEN
D=A
@mouse
M=D

(LOOP)
@KBD
D = M
@GOWHITE
D; JEQ
@GOBLACK
0; JMP


(GOBLACK)
@mouse
D=M
@screenend
D=M-D
@LOOP
D; JEQ

@mouse
A=M
M=-1
@mouse
M=M+1
@LOOP
0; JMP

(GOWHITE)
@mouse
D=M
@SCREEN
D=D-A
@LOOP
D; JEQ

@mouse
M=M-1
A=M
M=0
@LOOP
0; JMP
