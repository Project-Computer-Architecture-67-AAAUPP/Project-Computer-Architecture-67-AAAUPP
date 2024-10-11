        lw  0   1   five    #load reg1 with 5 (uses symbolic address)
        lw  1   2   3       #load reg2 with -1 (uses numeric address)
# OR    lw  0   2   neg1    #load reg2 with -1 (uses symbolic address)
start   add 1   2   1       #decrement reg1
        beq 0   1   2       #go to end of program when reg1==0
        beq 0   0   start   #go back to the beginning of the loop
        noop
done    halt                #end of program
five    .fill   5
neg1    .fill   -1
stAddr  .fill   start       #will contain the address of start