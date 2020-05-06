import numpy as np
from numba import njit, objmode, types
from numba.typed import List
from numba.pycc import CC

cc = CC('algoxtools32')
cc.verbose = True

@cc.export('annex_row', 'void( i2[:,:,:], i2, i2[:] )')
@njit( 'void( i2[:,:,:], i2, i2[:] )')
def annex_row( array, cur_row, col_list ):
    L, R, U, D, LINKED, VALUE =  range(6)  
    INDEX = 0
    prv_col = -1
    ncol_list = List() #[]
    ncol_list.append(INDEX)
    #[ ncol_list.append( col ) for col in col_list ]
    for col in range(len(col_list)) :
        ncol_list.append( col_list[col] )
    first_col = ncol_list[0]
    last_col = 0
    for cur_col in ncol_list:
        # Set Last, Total indices
        if array[ INDEX, cur_col, VALUE  ] == -1:
            array[ INDEX, cur_col, U ] = cur_row
        else:
            # Set Up, Down
            last_row = array[ INDEX, cur_col, U ]
            array[ cur_row, cur_col, U ]  = last_row 
            array[ last_row, cur_col, D ] = cur_row
            first_row = array[ INDEX, cur_col, D ]
            array[ cur_row, cur_col, D ] = first_row
            array[ first_row, cur_col, U ] = cur_row
        if cur_col != INDEX:
            array[ INDEX, cur_col, VALUE  ] += 1
        if cur_row != INDEX:
            array[ cur_row, INDEX, VALUE  ] += 1
        # Set Right, left 
        if prv_col != -1:
            array[ cur_row, prv_col, R ] = cur_col
            array[ cur_row, cur_col, L ] = prv_col
        array[ INDEX, cur_col, U ] = cur_row
        prv_col = cur_col
        last_col = cur_col
        if cur_row != INDEX and cur_col != INDEX:
            array[ cur_row, cur_col, VALUE ] = 1
        if cur_row == INDEX:
            #array[ INDEX, INDEX, VALUE ] += 1
            array[ INDEX, cur_col, LINKED ] = 1
        array[ cur_row, INDEX, LINKED ] = 1
        array[ cur_row, cur_col, LINKED ] = 1
    # Make row toroidal
    array[ cur_row, first_col, L] = last_col
    array[ cur_row, last_col, R] = first_col
    # unlink row index
    col_index = array[ cur_row, INDEX ]
    array[ cur_row, col_index[R], L ] = col_index[L]
    array[ cur_row, col_index[L], R ] = col_index[R]

@cc.export('init','i2[:,:,:](i2, i2)')
@njit('i2[:,:,:](i2, i2)')
def init( rows, cols ):
    L, R, U, D, LINKED, VALUE =  range(6)  
    INDEX = 0
    META = -1
    array=np.zeros( ( rows + 2, cols + 1, 6 ), np.int16 )
    array[ INDEX, :, VALUE ] = -1
    array[ :, INDEX, VALUE ] = -1
    array[ META, INDEX, VALUE ] = 0
    array[ INDEX, INDEX, VALUE ] = 0
    col_ind = np.arange( 1, cols+1, 1, np.int16)
    annex_row( array, INDEX, col_ind )
    #array[ INDEX, INDEX, VALUE ] = cols
    return array

# Cover
@cc.export('cover','void( i2[:,:,:],i2,i2,i2 )')
@njit( 'void( i2[:,:,:],i2,i2,i2 )',nogil=True)
def cover( array, row, col, level ):
    L, R, U, D, LINKED, VALUE =  range(6)  
    INDEX = 0
    META, COVERCOUNT, SOLUTIONCOUNT = -1, -1, 0
    ROW, COL = 0 ,1

    array[ META, level + 1, VALUE ] = row
    array[ META, COVERCOUNT, VALUE ] += array[ row, INDEX, VALUE ]

    j = col
    while True:
    #for j in r_sweep( array, row, col ):
        if array[ INDEX, j, LINKED ]:
            #unlink_col( array, j )

            col_index = array[ INDEX, j ]
            # Unlink Left - Right
            array[ INDEX, col_index[L], R ] = col_index[R]
            array[ INDEX, col_index[R], L ] = col_index[L]
            col_index[LINKED] = 0
            # Update main header
            index_index = array[ INDEX, INDEX ]
            if index_index[L] == j == index_index[R]:
                index_index[LINKED] = 0
            if index_index[L] == j:
                index_index[L] = col_index[L]
            if index_index[R] == j:
                index_index[R] = col_index[R]

        j = array[ row, j, R ]
        if j == col:
            break
            
    j = col
    while True:
    #for j in r_sweep( array, row, col ):
 
        i = row
        while True:

        #for i in d_sweep( array, row, j ):
            if array[ i, INDEX, LINKED ]: #Works when left out
                #unlink_row(array, i )
                
                row_index = array[ i, INDEX ]
                # Unlink Up - Down
                array[ row_index[D], INDEX, U ] = row_index[U]
                array[ row_index[U], INDEX, D ] = row_index[D]
                row_index[LINKED] = 0
                # Update main header
                index_index = array[ INDEX, INDEX ]
                if index_index[U] == i == index_index[D]:
                    index_index[LINKED] = 0
                if index_index[U] == i:
                    index_index[U] = row_index[U]
                if index_index[D] == i:
                    index_index[D] = row_index[D]

            k = array[ i, j, R ]
            # Skip first collumn and unlink 'loose' nodes, ie. nodes not in both unlinked rows and cols lattice
            while k != j:
                if ( array[ INDEX, k, LINKED ] or array[ i, INDEX, LINKED ] ) and array[ i, k, LINKED ]:
                    #unlink_node( array, i, k )
                    
                    node = array[ i, k ]
                    array[ node[D], k, U ] = node[U]
                    array[ node[U], k, D ] = node[D]
                    # Update collumn index
                    col_index = array[ INDEX, k ]
                    if i == col_index[U]:
                        col_index[U] = node[U]
                    if i == col_index[D]:
                        col_index[D] = node[D]
                    col_index[VALUE] -= 1
                    node[LINKED] = 0
                    
                k = array[ i, k, R ]

            i = array[ i, j, D ]
            if i == row:
                break

        j = array[ row, j, R ]
        if j == col:
            break

# Uncover
@cc.export('uncover','void( i2[:,:,:] )')
@njit( 'void( i2[:,:,:] )',nogil=True)
def uncover(array):
    L, R, U, D, LINKED, VALUE =  range(6)  
    INDEX = 0
    META, COVERCOUNT, SOLUTIONCOUNT = -1, -1, 0
    ROW, COL = 0 ,1
    level = array[ INDEX, INDEX, VALUE ]
    row = array[ META, level, ROW ]
    col = array[ META, level, COL ]

    j = col
    while True:
    #for j in r_sweep( array, row, col ):
        if not array[ INDEX, j, LINKED ]:
            #relink_col(array, j )

            col_index = array[ INDEX, j ]
            array[ INDEX, col_index[R], L] = array[ INDEX, col_index[L], R] = j
            col_index[LINKED] = 1
            # Update main header
            index_index = array[ INDEX, INDEX ]
            if j > index_index[L]:
                index_index[L] = j
            if j < index_index[R]:
                index_index[R] = j
            index_index[LINKED] = 1
            
        i = row
        while True:
        
        #for i in d_sweep( array, row, j ):
            if not array[ i, INDEX , LINKED ]:
                #relink_row( array, i )
                
                row_index = array[ i, INDEX ]
                array[ row_index[U], INDEX, D ] = array[ row_index[D], INDEX, U ] = i
                row_index[LINKED] = 1
                # Update main header
                index_index = array[ INDEX, INDEX ]
                if i < index_index[D]:
                    index_index[D] = i
                if i > index_index[U]:
                    index_index[U] = i
                index_index[LINKED] = 1
                
            # for k in r_sweep( array, i ,j 
            k = array[ i, j, R ]
            # Skip first collumn and relink 'loose' nodes, ie. nodes not in both unlinked rows and cols lattice
            while k != j:
                if not array[ i, k, LINKED ]:
                    #relink_node( array, i, k )

                    node = array[ i, k ]
                    array[ node[D], k, U ] = array[ node[U], k, D ] = i
                    col_index = array[ INDEX, k ]
                    if i > col_index[U]:
                        col_index[U] = i
                    if i < col_index[D]:
                        col_index[D] = i
                    col_index[VALUE] += 1
                    node[LINKED] = 1
     
                k = array[ i, k, R ]

            i = array[ i, j, D ]
            if i == row:
                break

        j = array[ row, j, R ]
        if j == col:
            break
            
    array[ META, COVERCOUNT, VALUE ] -= array[ row, INDEX, VALUE ]

@cc.export('min_col','i2( i2[:,:,:] )')
@njit( 'i2( i2[:,:,:] )',nogil=True)
def min_col( array ):
    L, R, U, D, LINKED, VALUE =  range(6)  
    INDEX = 0
    min_val = np.iinfo(np.int16).max
    col = 0
    cl = array[ INDEX, INDEX, R ]
    
    j = cl
    while True:

    #for j in r_sweep( array, INDEX, cl ):
        if array[ INDEX, j, VALUE ] < min_val:
            min_val = array[ INDEX, j, VALUE ]
            col = j

        j = array[ INDEX, j, R ]
        if j == cl:
            break

    return col

def dump(array):
    L, R, U, D, LINKED, VALUE =  range(6)  
    INDEX = 0
    rows = array.shape[0]
    cols = array.shape[1]
    print('rows',rows,'cols',cols)
    print()
    for cl in range(cols):
        print('\tcol',cl,end='')
    print()
    print()
    for rw,row in enumerate(array):
        print('\t',end='')
        for node in row:
            print(node[LINKED],node[U],'\t',end='')
        print()
        print('row',rw,'\t',end='')
        for node in row:
            print(node[L],node[VALUE],node[R],'\t',end='')
        print()
        print('\t',end='')
        for node in row:
            print(' ',node[D],'\t',end='')
        print()
        print()

@cc.export('isempty','b1(i2[:,:,:])')
@njit( 'b1(i2[:,:,:])', nogil=True)
def isempty(array):
    L, R, U, D, LINKED, VALUE =  range(6)  
    INDEX = 0
    META, COVERCOUNT, SOLUTIONCOUNT = -1, -1, 0
    ROW, COL = 0 ,1
    if not array[ INDEX, INDEX, LINKED ] and array[ META, COVERCOUNT, VALUE ] == array.shape[1] - 1:
            array[ META, SOLUTIONCOUNT, VALUE ] += 1
            return True
    return False

@cc.export('mcr_cover','b1(i2[:,:,:])')
@njit( 'b1(i2[:,:,:])', nogil=True)
def mcr_cover(array):
    L, R, U, D, LINKED, VALUE =  range(6)  
    INDEX = 0
    META, ROW, COL, FIRSTROW = -1, 0, 1, 2
    level = array[ INDEX, INDEX, VALUE ]
    first_row = array[ META, level, FIRSTROW ]
    if first_row == 0:
        col = min_col(array)
        if array[ INDEX, col, VALUE ] > 0:
            row = array[ INDEX, col, D ]
            array[ META, level, FIRSTROW ] = row
            array[ META, level, ROW ] = row
            array[ META, level, COL ] = col
            cover( array, row, col, level )
            return True
        else:
            return False
    else:
        level = array[ INDEX, INDEX, VALUE ]
        first_row = array[ META, level, FIRSTROW ]
        row = array[ META, level, ROW ]
        col = array[ META, level, COL ]
        row = array[ row, col, D ]
        if row != first_row:
            array[ META, level, ROW ] = row
            cover( array, row, col, level )
            return True
        else:
            array[ META, level, FIRSTROW ] = 0
            return False

@njit( 'void( i2[:] )', nogil=True)     
def fsolution(solution):      
    #print(solution)
    pass
    
@cc.export('search', 'void( i2[:,:,:] )')
@njit( 'void( i2[:,:,:] )', nogil=True )
def search(array):
    INDEX, VALUE, META = 0, -1, -1
    array[ INDEX, INDEX, VALUE ] += 1
    if isempty(array):
        level = array[ INDEX, INDEX, VALUE ]
        fsolution( array[ META, 1 : level, VALUE ] )
    else:
        while mcr_cover(array):
            search(array)
            uncover(array)
    array[ INDEX, INDEX, VALUE ] -= 1
    
if __name__ == '__main__':
    cc.compile()
    """
    #import os
    #os.environ['NUMBA_DISABLE_JIT'] = "1"
    """
    VALUE = 5
    META, SOLUTIONCOUNT = -1, 0

    array = init( 6, 7 )
    annex_row( array, 1, np.array([ 1, 4, 7 ], np.int16 ) )
    annex_row( array, 2, np.array([ 1, 4 ],np.int16 ) )
    annex_row( array, 3, np.array([ 4, 5, 7 ],np.int16 ) )
    annex_row( array, 4, np.array([ 3, 5, 6 ],np.int16 ) )
    annex_row( array, 5, np.array([ 2, 3, 6, 7 ],np.int16 ) )
    annex_row( array, 6, np.array([ 2, 7 ],np.int16 ) )

    search( array )
    print(array[ META, SOLUTIONCOUNT, VALUE ])
