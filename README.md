# algoxtools
<h2>A fast implementation of Donald Knuth's Algorithm X in Python by using Numpy and Numba.
<h3>
Open source implementations of [Algorithm X]](https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf)  in Python are plentiful. The justification of creating this module is that existing packages are all based on the beautiful object oriented example introduced by dr. Knuth. Python classes have a poor relation with compilers such as Numba however, resulting in discouraging speed gains.<br/> 
In algoxtools the web of Dancing Links nodes are embedded in a numpy array. Since the array is heterogenous, it is able to come more close to machine level when compiled, thus gaining performance.<br/>
The array space has three dimensions nl. row, column and substitutes for class attributes. Attributes used are Left, Right, Up, Down, Linked and Value. Headers for rows and columns as well as meta data such as recursion level, current row, column and solution at hand are all embedded in the array, making it easy to pass like a more conventional object.<br/>
The array organisation used is sparse and uses 16 bit ints. If needed it can be easily adapted. Dynamic allocation of nodes could further optimize use of memory and squeeze out some last bit of performance gain, but remains to be implemented.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Seemee/algoxtools/299b8f1cd71c766032fb969ab2a77308fc2f59c8?filepath=examples%2Falgoxtools%20api%20usage%20example%20in%20ipynb.ipynb) [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/119zcx-mmnLA333ifXJFVjbB9aRKbiU6S?usp=sharing)
