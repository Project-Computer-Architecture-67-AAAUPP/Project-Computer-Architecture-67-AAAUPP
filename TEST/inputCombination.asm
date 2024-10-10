        lw      0       1       n           # Load n into reg1
        lw      0       2       r           # Load r into reg2
        lw      0       4       neg1         # Load -1 into reg4
        lw      0       5       one          # Load 1 into reg5
        lw      0       6       stackPtr     # Load stack pointer into reg6

        # Check base cases
        beq     2       0       base        # If r == 0, jump to base case (C(n, 0) = 1)
        beq     1       2       base        # If n == r, jump to base case (C(n, n) = 1)

        # Store n and r on stack
        add     6       4       6           # Decrement stack pointer
        sw      6       1       stackN      # Store n on stack
        add     6       5       6           # Increment stack pointer
        sw      6       2       stackR      # Store r on stack
        add     6       4       6           # Decrement stack pointer

        # Prepare for recursive calls
        add     1       4       7           # n - 1 -> reg7
        add     2       4       8           # r - 1 -> reg8

        jalr    5       7                   # Recursive call: combination(n-1, r)
        add     6       5       6           # Increment stack pointer
        lw      3       6       stackN      # Load result of C(n-1, r)

        add     6       4       6           # Decrement stack pointer
        lw      2       6       stackR      # Load r back
        add     6       4       6           # Decrement stack pointer
        lw      1       6       stackN      # Load n back

        # Prepare n-1 for second call
        add     1       4       7           # Prepare n - 1 for second call
        jalr    5       8                   # Recursive call: combination(n-1, r-1)
        
        add     6       5       6           # Increment stack pointer
        lw      4       6       stackN      # Load result of C(n-1, r-1)

        # Combine the results from the two recursive calls
        add     3       4       3           # reg3 = C(n-1, r) + C(n-1, r-1)
        halt                                # End of program
        
base    li      0       3       one         # If it's a base case, return 1
        halt                                # End of program


# Data section
n       .fill   7                   # Value of n
r       .fill   3                   # Value of r
result  .fill   0                   # Initialize result to 0
one     .fill   1                   # Define 1
neg1    .fill   -1                  # Define -1
stackPtr .fill  0                   # Pointer to the stack
stackN  .fill   0                   # Stack for storing n
stackR  .fill   0                   # Stack for storing r
        .fill   0                   # Fill stack space to avoid overwriting
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
