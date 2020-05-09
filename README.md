## algoxtools 
### A practical implementation of Donald Knuth's Algorithm X in Python using Numpy and Numba.
#### Open sourced implementations of [Algorithm X](https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf) in Python are plentiful.<br/>Justification of creating algoxtools is that although existing packages are compact and elegantly coded in object oriented Python, a drawback is that for more complex exact cover problems processing the Python interpreted node objects used in the NP-complete algorithm becomes slow. Since use of classes has a poor relation with compilers such as Numba, resulting speed gains are discouraging.<br/> 
In algoxtools the web of Knuth's Dancing Links nodes is embedded in a numpy array. Since numpy arrays are heterogenous by design and boast high performance libraries, algoxtools aims to come more close to machine level, resulting in performance gain.<br/> 
The array space used by algoxtools is in 3d, arranged in rows, columns, the third dimension being used for substitutes of class attributes such as pointers and index values. Headers for rows and columns as well as meta data such as recursion level, current row, column and solution at hand are all embedded in the array as well, making the variables as easy to pass as a conventional object.<br/>
Algoxtools facilitates unlinking and relinking of rows and columns at once by eleborate indexing which avoids handling each individual node chain*.<br/>Moreover the indexing used shakes off the need for recursion, which allows for returns to caller level from just one function.<br/>
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
INDEX, META, SOLUTIONCOUNT, VALUE, SOLUTION = 0, -1, 0, -1, 1
array = axt.init( 6, 7 )
dt = np.int16
# Rows and cols start from 1!
axt.annex_row( array, 1, np.array([ 1, 4, 7 ], dt ) )
axt.annex_row( array, 2, np.array([ 1, 4 ], dt ) )
axt.annex_row( array, 3, np.array([ 4, 5, 7 ], dt ) )
axt.annex_row( array, 4, np.array([ 3, 5, 6 ], dt ) )
axt.annex_row( array, 5, np.array([ 2, 3, 6, 7 ], dt ) )
axt.annex_row( array, 6, np.array([ 2, 7 ], dt ) )
ii = array[ INDEX, INDEX ]
print( 'Solution:' )
while axt.exact_cover( array ):
    print( array[ META, SOLUTION : ii[VALUE], VALUE ] )
```
```
Solution:
[2 4 6]
```
Above examples is enclosed in jupyter notebook format in the [examples folder](https://github.com/Seemee/algoxtools/tree/master/examples)

## Quick api reference guide:
### array = init( rows, columns )
Initializes algoxtools array.<br/>
Internally the number of columns is one higher than the given value and is used for indexing.<br/>
The internal number of rows is two higher than the given value and is used for indexing and storing meta data<br/>
Rows and columns numbers cannot exceed the np.int16 maximum value - 1 (+32,766)
### Example:
```
import algoxtools as axt
array = axt.init( 6, 7 )
```

### annex_row( array, row_number, numpy.array( column 1, column 2, .. column n , numpy.int16) )
Assigns linked nodes to the specified columns in a specific row.<br/> 
row and col values should be higher than 1 and cannot exceed numpy.int16 maximum value - 1<br/>
In order to solve an exact cover, all rows must contain at least one column.<br/>
### Example:
```
axt.annex_row( array, 4, np.array([ 3, 5, 6 ], np.int16 ) )
```

### bool exact_cover( array )
This is the main function to flip through exact cover solutions, it returns a boolean True if reached an exact cover and returns a boolean False if finished.
### Example:
```
while axt.exact_cover( array )
    print(print( array[ META, SOLUTION : array[ 0,0,-1 ], VALUE ] )
```

## Miscellaneous functions used internally
### bool isempty( array )
Returns boolean True if an exact cover is reached else returns a False
### Example:
```
if axt.isempty( array ):
    ## Exact cover found
    level = array[ 0, 0, -1 ]
    print( array[ -1, 1:level, -1 ]
```

### bool mcr_cover( array )
Minimum column rows cover (Or Most-constrained column rows cover) is a composite of internal min_col() and cover() functions.<br/>
Initialy it selects the first column with the least number of nodes and the first row in that column and covers all nodes which are orthogonally linked to that entry.<br/>
In subsequent calls mcr_cover selects a next row and covers it until all rows are depleted.<br/>
Returns a boolean False if no more rows are available, else returns True<br/>
This function should be balanced by uncover<br/>
### Example:
```
while axt.mcr_cover( array ):
    # Recurse
    search( array )
    axt.uncover( array )
```
### void uncover( array )
Uncover the nodes previously linked to current row and colum entry in the array (selected by mcr_cover) 
### Internal organisation of algoxtools array:
```
0,0 Index,Index------------- Column Indices -----------------------  0,-1

   |     Node 1,1        Node 1,2        Node 1,Columns

   |	 Node 2,1        Node 2,2        Node 2,Columns

  Row 

indices     |               |                |

   |        |               |                |

   |

   |	 Node Rows,1     Node Rows,2     Node Rows,Columns

-1,0 --------------------------- Meta data ----------------------  -1, -1
```
NB The row column indices are basically unlinked nodes keeping track of entry positions and node count
### Specific array values used in api
```
Recursion level:      array[ 0, 0,-1 ]
Solution count:       array[-1, 0, 0 ]
Solution row numbers: array[-1, 1: recursion_level, -1 ]
```
### Node attributes
```
Name    Description               Value
---------------------------------------
L       Left link pointer           0
R       Right link pointer          1
U       Up link pointer             2
D       Down link pointer           3
LINKED  Node or index link status   4
VALUE   Stores miscellaneous values 5 (-1)
```
## &ast; Unlinking en relinking nodes:<br/>
The illustration below which is taken from [Wikipedia](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X) shows how nodes are covered in algoxtools:<br/>
In the example the entry at column 1, row 1 is heuristically chosen to be covered.<br/>
<img src="https://github.com/Seemee/algoxtools/blob/master/images/Cover%20example.PNG" width="300"><br/>
Since the nodes at the red ones in Columns (1,4,7) and rows (A,B,C,E,F)  are not linked to any other outside nodes. Rows and columns are unlinked just by row and column index without unlinking each individual node.<br/>
<img src="https://github.com/Seemee/algoxtools/blob/master/images/Loose%20nodes%20example.png" width="300"><br/> 
What I call 'loose' nodes, which are in this case the remaining ones in the red boxes, (C5,E2,E3,E6 and F2) are situated in an unlinked row but not in an unlinked column, so they are possibly attached to external nodes and therefore need to be unlinked individually<br/>
NB common in most other implementations of Algorithm X only the down link of the upper node and the up link of the down nodes are changed, right and left links do not need to be modified since they are not externally referenced.
