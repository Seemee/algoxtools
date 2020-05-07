## algoxtools 
### A high performance implementation of Donald Knuth's Algorithm X in Python using Numpy and Numba.
#### Open source implementations of [Algorithm X](https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf) in Python are plentiful. The justification of creating this module is that although existing packages are elegantly coded in object oriented Python, a drawback is that the Python classes used have a poor relation with compilers such as Numba, resulting in discouraging speed gains when compiled.<br/> 
In algoxtools the web of Knuth's Dancing Links nodes is embedded in a numpy array. Since numpy arrays are heterogenous by design and boast high performance libraries they are able to come more close to machine level, thus resulting in performance gain.<br/> 
The array space is 3d and is arranged in rows, columns, the third dimension being used for substitutes of class attributes such as pointers and index values. Attributes used are Left, Right, Up, Down, Linked and Value. Headers for rows and columns as well as meta data such as recursion level, current row, column and solution at hand are all embedded in the array as well, making it easy to pass, similar to a more conventional object.<br/>
Furthermore algoxtools facilitates unlinking and relinking of rows and columns at once by eleborate indexing
which avoids handling each individual node chain.
The array organisation is sparse and uses 16 bit ints. If needed int size can be easily adapted. Dynamic allocation of nodes could further optimize use of memory and squeeze out a bit of performance gain, but remains to be implemented.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Seemee/algoxtools/299b8f1cd71c766032fb969ab2a77308fc2f59c8?filepath=examples%2Falgoxtools%20api%20usage%20example%20in%20ipynb.ipynb) [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/119zcx-mmnLA333ifXJFVjbB9aRKbiU6S?usp=sharing)
