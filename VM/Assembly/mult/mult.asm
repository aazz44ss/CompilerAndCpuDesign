// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// set R0 to 16
	@16
	D=A
	@R0
	M=D
// set R1 to 32
	@32
	D=A
	@R1
	M=D

// Multiplies R0 and R1 and stores the result in R2.
	@R2
	M=0 // R2 = 0
	@i
	M=1 // i = 1
	@R1
	D=M
	@n
	M=D // n = R1

(LOOP)
	@i
	D=M
	@n
	D=D-M
	@END
	D;JGT // if i > n then END
	@R0
	D=M
	@R2
	D=D+M
	M=D  // R2 += R0
	@i
	M=M+1
	@LOOP
	0;JMP
(END)
	@END
	0;JMP
