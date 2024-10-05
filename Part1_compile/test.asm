        lw      0       1       five        # Load reg1 with 5 (uses symbolic address)
        lw      1       2       neg1        # Load reg2 with -1 (uses symbolic address)
start   add     1       2       1           # Decrement reg1
        beq     0       1       2           # Go to 'done' when reg1 == 0
        beq     0       0       start       # Go back to the beginning of the loop
        noop                                # No operation
done    halt                                # End of program
five    .fill   5                           # Store the value 5
neg1    .fill   -1                          # Store the value -1
stAddr  .fill   start                       # Will contain the address of 'start'
