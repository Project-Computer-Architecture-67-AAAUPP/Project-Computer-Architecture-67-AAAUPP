        lw      0       1       num1    # Load first number into reg1
        lw      0       2       num2    # Load second number into reg2
        lw      0       3       zero    # Load 0 into reg3 (for result)
        lw      0       4       one     # Load 1 into reg4 (for decrementing)
loop    beq     0       2       done    # If num2 == 0, exit loop
        add     3       1       3       # Add num1 to result
        add     2       4       2       # Decrement num2
        beq     0       0       loop    # Unconditional branch to loop
done    sw      0       3       result  # Store result in memory
        halt                            # End program
num1    .fill   5                       # First number to multiply
num2    .fill   3                       # Second number to multiply
zero    .fill   0
one     .fill   -1                      # Use -1 for decrementing
result  .fill   0                       # Memory location for result