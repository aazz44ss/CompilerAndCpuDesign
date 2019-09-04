# VM translator

VM translator compile VM code to assambly code

	usage:
		python VMtranslator.py test/FibonacciElement/

	out:
		Test/FibonacciElement/FibonacciElement.asm
	
## VM Architecture Introduction

	RAM:
		0: SP		// stack pointer
		1: LCL		// local memory pointer
		2: ARG		// argument pointer
		3: THIS		// function pointer
		4: THAT
		5~255:		// static variable
		256~2047:	// stack
		2048~16383: // heap memory
		16384~24576:// screen and keyboard

	There are 4 commands:
	1. Arithmetic/Logical commands
		1. add  // x= *(SP-2), y=*(SP-1), *(SP-2)=x+y, SP=SP-1
		2. sub	// x= *(SP-2), y=*(SP-1), *(SP-2)=x-y, SP=SP-1
		3. neg  // *(SP-1)=-(*(SP-1))
		4. eq   // x= *(SP-2), y=*(SP-1), *(SP-2)=(x==y)?-1:0, SP=SP-1
		5. gt   // x= *(SP-2), y=*(SP-1), *(SP-2)=(x>y)?-1:0, SP=SP-1
		6. lt   // x= *(SP-2), y=*(SP-1), *(SP-2)=(x<y)?-1:0, SP=SP-1
		7. and  // x= *(SP-2), y=*(SP-1), *(SP-2)=x&y, SP=SP-1
		8. or   // x= *(SP-2), y=*(SP-1), *(SP-2)=x|y, SP=SP-1
		9. not  // *(SP-1)=!(*(SP-1))

	2. Memory access
		1. pop segment i     // pop "i" from *(SP-1) to "segment", SP=SP-1
		2. push segment i    // push "i" from "segment" to *(SP), SP=SP+1

	3. Branching commands
		1. label label       // label LOOP
		2. goto label		 // goto LOOP
		3. if-goto label     // if(*(SP-1)==-1) goto label

	4. Function commands
		1. function functionName nVars
			1. label (function_label)
			2. initial local memory to 0, nVars times
		2. call functionName nArgs
			1. push return address
			2. push current LCL,ARG,THIS,THAT address
			3. modify function ARG to SP (ARG = SP-5-nArgs), push function arguments
			4. modify function LCL to SP
			5. goto funciton
			6. label (function_return_label)
		3. return
			1. push return value to function *ARG
			2. restore THAT,THIS,ARG,CLC
			3. goto function_return_label

### VM Booting
	We need to boot our VM by first setting SP to 256,
	then call Sys.init function in Sys.vm code.

	VM program is a folder that has Sys.vm file, and optional other .vm files.
	In Sys.vm file, there must has Sys.init function to boot our VM.
