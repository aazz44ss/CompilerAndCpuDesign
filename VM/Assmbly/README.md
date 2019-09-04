# 適用於此Machine的組合語言介紹

1. LABEL操作, compiler會紀錄label所在的下一個instruction行數
	ex.
		(LOOP)
		(END)


2. @為A instruction,會寫入A register,有三種操作
	1. constant
		ex.
			@16  // A = 16

	2. variable
		ex.
			@temp  => compiler會查之前是有紀錄過此variable,沒有則會將temp轉成一常數,並記錄
			@temp  => @16384
			
	3. label
			@LOOP  => compiler會先查是否之前有記錄到LOOP,若是沒有,則會當作variable看待
			
3. dest = comp ; jmp
	M 為 RAM[A]
	D 為 D register
	A 為 A register
		ex.
			@16 	// A = 16
			D = A	// D = 16
			@18		// A = 18
			M = D	// RAM[18] = 16
			A = D	// A = 16
			M = D+1 // RAM[16] = 16+1
			