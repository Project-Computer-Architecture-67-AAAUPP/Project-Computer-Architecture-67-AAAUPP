 Noted
Part 3 : Compiler for Function Multiple&Combination
        send output to monitor behavior to part2
 #python AssemblyToMachineCode.py input.asm output.mc           //for test run
    #run Test 
        -python AssemblyToMachineCode.py TestInput.asm TestOutput.mc
    #run Multiple
        -python AssemblyToMachineCode.py MultiplicationInput.asm MultiplicationOutput.mc
    #run Combination
        -python AssemblyToMachineCode.py CombinationInput.asm CombinationOutput.mc
 #test.asm = input file                                         // each line is one instruction code 
 #output.mc = output file                                       // after compile assembly this file will collect that result of compile as machinecode in decimal