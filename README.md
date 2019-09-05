# About This Design

	利用Nand設計了一個CPU
	並為這個CPU設計了虛擬機和簡單的高階語言
	並且為高階語言設計了編譯器


## 專案結構

	在 VM-Assmbly-Machine 中
	利用邏輯電路中最基本的元素"Nand Gate"組合出CPU及Memory

	在 VM-Assmbly 中
	將 Assmbly Code 編譯成所設計硬體可執行的 Binary Code

	在 VM_translator 中
	將 VM Code 編譯成 Assmbly Code

	在 Compiler 中
	將設計一個物件導向的高階語言，並編寫編譯器將代碼編譯成 VM Code


	--- Compiler
		|--- Square
			|--- Main.hl
			|--- Square.hl
			|--- SquareGame.hl
		|--- compile_engine.py
		|--- constant.py
		|--- hl_analyzer.py
		|--- hl_tokenizer.py
		|--- README.md
	--- VM
		|--- Assmbly
			|--- Machine
				|--- Component
					|--- Basic_Element
						|--- Mux.hdl
						|--- Mux4Way16.hdl
						|--- Mux8Way16.hdl
						|--- Mux16.hdl
						|--- Not.hdl
						|--- Not16.hdl
						|--- Or.hdl
						|--- Or8Way.hdl
						|--- Or16.hdl
						|--- Xor.hdl
						|--- README.md
					|--- Add16.hdl
					|--- ALU.hdl
					|--- FullAdder.hdl
					|--- HalfAdder.hdl
					|--- Inc16.hdl
					|--- README.md
				|--- Ram
					|--- RAM4K.hdl
					|--- RAM16K.hdl
					|--- RAM512.hdl
				|--- Computer.hdl
				|--- CPU.hdl
				|--- Memory.hdl
				|--- README.md
			|--- mult
				|--- mult.asm
			|--- README.md
		|--- assmbler.py
		|--- README.md
	--- VM_translator
		|--- test
			|--- BasicLoop
				|--- BasicLoop.vm
			|--- FibonacciElement
				|--- Main.vm
				|--- Sys.vm
			|--- FibonacciSeries
				|--- FibonacciSeries.vm
		|--- code_writer.py
		|--- constant.py
		|--- parser.py
		|--- VMtranslator.py
		|--- README.md
