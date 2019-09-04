# COMPONENT

利用Basic element組合出ALU

## ALU介紹

IN
  DATA_INPUT
	x[16], y[16],  // 16-bit inputs
  PARAMETER_INPUT
	zx, // zero the x input?
	nx, // negate the x input?
	zy, // zero the y input?
	ny, // negate the y input?
	f,  // compute out = x + y (if 1) or x & y (if 0)
	no; // negate the out output?

OUT
  DATA_OUTPUT
	out[16], // 16-bit output
  PARAMETER_OUTPUT
	zr, // 1 if (out == 0), 0 otherwise
	ng; // 1 if (out < 0),  0 otherwise
	
ALU可以輸入2組16bit資料，並有6個參數輸入來控制資料狀態
透過這6個參數我們可以得到out_put組合有
x+y, x-y, y-x, 0, 1, -1, x, y, -x, -y, !x, !y,
x+1, y+1, x-1, y-1, x&y, x|y

<ALU圖片>