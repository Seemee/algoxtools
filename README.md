## algoxtools 
### A high efficiency implementation of Donald Knuth's Algorithm X in Python using Numpy and Numba.
#### Open source implementations of [Algorithm X](https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf) in Python are plentiful. The justification of creating this module is that although existing packages are compact and elegantly coded in object oriented Python, a drawback is that the Python classes used tend to have a poor relation with compilers such as Numba, resulting in discouraging speed gains when compiled.<br/> 
In algoxtools the web of Knuth's Dancing Links nodes is embedded in a numpy array. Since numpy arrays are heterogenous by design and boast high performance libraries, algoxtools aims to come more close to machine level, resulting in performance gain.<br/> 
The array space used by algoxtools is 3d, arranged in rows, columns, the third dimension being used for substitutes of class attributes such as pointers and index values. Attributes used are Left, Right, Up, Down, Linked and Value. Headers for rows and columns as well as meta data such as recursion level, current row, column and solution at hand are all embedded in the array as well, making it easy to pass like a conventional object.<br/>
Algoxtools facilitates unlinking and relinking of rows and columns at once by eleborate indexing which avoids handling each individual node chain.
The api is organized in a way that the main search loop can be kept at Python interpreter level so that search results can be easily further processed at this even.
The array organisation is sparse and uses 16 bit ints. If needed, int size can be easily adapted.<br/>Dynamic allocation of nodes could further optimize use of memory and squeeze out a bit of performance gain, but remains to be implemented.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Seemee/algoxtools/299b8f1cd71c766032fb969ab2a77308fc2f59c8?filepath=examples%2Falgoxtools%20api%20usage%20example%20in%20ipynb.ipynb) [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/119zcx-mmnLA333ifXJFVjbB9aRKbiU6S?usp=sharing)
## Installation
```
pip install algoxtools
```
## Api example 
Data taken from [Wikipedia](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X) 
```
import algoxtools as axt
import numpy as np

array = axt.init( 6, 7 )
dt = np.int16
# Rows and cols start from 1!
axt.annex_row( array, 1, np.array([ 1, 4, 7 ], dt ) )
axt.annex_row( array, 2, np.array([ 1, 4 ], dt ) )
axt.annex_row( array, 3, np.array([ 4, 5, 7 ], dt ) )
axt.annex_row( array, 4, np.array([ 3, 5, 6 ], dt ) )
axt.annex_row( array, 5, np.array([ 2, 3, 6, 7 ], dt ) )
axt.annex_row( array, 6, np.array([ 2, 7 ], dt ) )

print( 'Solution:' )
axt.search(array)
```
```
Solution:
[2 4 6]
```
## Usage with main loop at interpreter level:
```
INDEX, META, SOLUTIONCOUNT, VALUE, SOLUTION = 0, -1, 0, -1, 1
ii = array[ INDEX, INDEX ]
def search( array ):
    ii[VALUE] += 1 # Level up
    if axt.isempty(array):
        # Got a solution, do something with it.. like print only the first 5 sols
        if array[ META, SOLUTIONCOUNT, VALUE ] <= 5:
            print( array[ META, SOLUTIONCOUNT, VALUE ],
                  array[ META, SOLUTION : ii[VALUE], VALUE ] )
    else:
        while axt.mcr_cover(array):
            search(array) # Recurse
            axt.uncover(array)
    ii[VALUE] -= 1 # Level down

print('Solution:')
search(array)
print('Total no. of solutions:', end=' ')
print( array[ META, SOLUTIONCOUNT, VALUE ] )
```
```
Solution:
[2 4 6]
Total no. of solutions: 1
```

Above examples are enclosed in jupyter notebook format in the [examples folder](https://github.com/Seemee/algoxtools/tree/master/examples)
