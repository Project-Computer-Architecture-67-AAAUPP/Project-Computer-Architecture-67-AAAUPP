      lw      0   5   stack       # Initialize the stack pointer
      lw      0   1   n           # Load n into $1
      lw      0   2   r           # Load r into $2
comb  beq     2   0   base        # If r == 0, go to base
      beq     1   2   base        # If n == r, go to base
      lw      0   6   one         # Load 1 into $6 (used for increment/decrement)
      add     5   5   6           # Increment stack pointer
      sw      5   7   stack       # Save return address
      add     5   5   6           # Increment stack pointer
      sw      5   1   stack       # Save n
      add     5   5   6           # Increment stack pointer
      sw      5   2   stack       # Save r
      lw      0   6   neg1        # Load -1 into $6
      add     1   1   6           # n = n - 1
      jalr    6   7               # Call combination(n-1, r)
      add     3   3   4           # Store result in $4 temporarily
      add     2   2   6           # r = r - 1 (using the same -1 from $6)
      jalr    6   7               # Call combination(n-1, r-1)
      add     3   4   3           # Add both results
      lw      0   6   neg1        # Load -1 into $6 (to decrement the stack pointer)
      add     5   5   6           # Decrement stack pointer
      lw      2   5   stack       # Restore r
      add     5   5   6           # Decrement stack pointer
      lw      1   5   stack       # Restore n
      add     5   5   6           # Decrement stack pointer
      lw      7   5   stack       # Restore return address
      jalr    7   6               # Return from function
base  lw      0   3   one         # Return 1 (load constant 1 into $3)
      jalr    7   6               # Return to caller
      halt                        # End of program
n     .fill 7
r     .fill 3
neg1  .fill -1           # Constant -1
one   .fill 1            # Constant 1
stack .fill 0            # Stack starts here
      .fill 0            # More stack memory
      .fill 0
      .fill 0
      .fill 0
      .fill 0
      .fill 0
      .fill 0
      .fill 0
      .fill 0
      .fill 0
      .fill 0
      .fill 0