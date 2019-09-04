# COMPUTER

	Computer是由
	1. 32k ROM來儲存所執行的程式
	2. CPU
	3. 32K RAM	
		Address 0 to 16383: data memory
		Address 16384 to 24575: screen memory map
		Address 24576: keyboard memory map
	4. 外部配備screen，對應到的address有8k個，每個address有16bit控制16個pixel
	5. 外部配備keyboard，對應到address為24576

![image](https://github.com/aazz44ss/CompilerAndCpuDesign/blob/master/VM/Assmbly/Machine/pic/computer.png)

## CPU

	CPU有3個輸入及4個輸出

	INPUT
		1. instruction
		2. inM
		3. reset

	OUTPUT
		1. outM		// 16bit data output
		2. writeM	// outM是否寫入RAM中
		3. addressM // address of RAM
		4. pc		// program counter，來控制程式要執行第幾行的instruction

![image](https://github.com/aazz44ss/CompilerAndCpuDesign/blob/master/VM/Assmbly/Machine/pic/cpu.png)

## instruction介紹

	共16bit
	o1 o2 o3 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3

	o1:
		0: A instruction, 則後面15bit代表一整數
			用來表達constant, address or instruction

		1: C instruction, 則後面15bit為控制單元
			o2 o3	保留為11
			a 		控制進入ALU的是A register或inM
			c1~c6	ALU控制單元
			d1~d3	控制是否覆寫A register,D register, RAM
			j1~j3	控制是否jmp

![image](https://github.com/aazz44ss/CompilerAndCpuDesign/blob/master/VM/Assmbly/Machine/pic/cpu_op.png)


