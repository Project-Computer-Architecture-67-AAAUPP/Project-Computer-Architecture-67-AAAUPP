NUMMEMORY = 65536  # จำนวนคำสูงสุดในหน่วยความจำ
NUMREGS = 8  # จำนวนเรจิสเตอร์
MAXLINELENGTH = 1000  # ขนาดสูงสุดของแต่ละบรรทัดในไฟล์

class State:
    def __init__(self):
        self.pc = 0
        self.mem = [0] * NUMMEMORY
        self.reg = [0] * NUMREGS
        self.numMemory = 0

def printState(state):
    """แสดงสถานะของเครื่องจำลอง"""
    print("\n@@@\nstate:")
    print(f"\tpc {state.pc}")
    print("\tmemory:")
    for i in range(state.numMemory):
        print(f"\t\tmem[ {i} ] {state.mem[i]}")
    print("\tregisters:")
    for i in range(NUMREGS):
        print(f"\t\treg[ {i} ] {state.reg[i]}")
    print("end state")

def convertNum(num):
    """แปลงค่า 16-bit เป็น 32-bit"""
    if num & (1 << 15):
        num -= (1 << 16)
    return num

def r_getArgs(bitstring):
    """ถอดรหัสคำสั่ง R-type"""
    regA = (bitstring >> 19) & 0x7
    regB = (bitstring >> 16) & 0x7
    destReg = bitstring & 0x7
    return regA, regB, destReg

def i_getArgs(bitstring):
    """ถอดรหัสคำสั่ง I-type"""
    regA = (bitstring >> 19) & 0x7
    regB = (bitstring >> 16) & 0x7
    offsetField = bitstring & 0xFFFF
    offsetField = convertNum(offsetField)
    return regA, regB, offsetField


def main():
    import sys
    debug = False

    if len(sys.argv) == 3 and sys.argv[2] == "-d":
        print("***********DEBUG MODE ENABLED***********")
        debug = True
    elif len(sys.argv) != 2:
        print(f"error: usage: {sys.argv[0]} <machine-code file>")
        return

    # เปิดไฟล์ machine code
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: Can't open file {filename}")
        return

    # ตั้งค่าเริ่มต้น
    state = State()
    for line in lines:
        if state.numMemory >= NUMMEMORY:
            print(f"ERROR: Max number of words exceeded. Max: {NUMMEMORY}")
            return
        try:
            state.mem[state.numMemory] = int(line.strip())
            print(f"memory[{state.numMemory}]={state.mem[state.numMemory]}")
            state.numMemory += 1
        except ValueError:
            print(f"ERROR: Failed to read address {line.strip()}")
            return

    total_instructions = 0
    while True:
        if debug:
            print(f"run: {total_instructions + 1}")
        total_instructions += 1
        printState(state)

        instruction = state.mem[state.pc]
        opcode = instruction >> 22

        if opcode == 0:  # ADD
            regA, regB, destReg = r_getArgs(instruction)
            state.reg[destReg] = state.reg[regA] + state.reg[regB]

        elif opcode == 1:  # NAND
            regA, regB, destReg = r_getArgs(instruction)
            state.reg[destReg] = ~(state.reg[regA] & state.reg[regB])

        elif opcode == 2:  # LW
            regA, regB, offsetField = i_getArgs(instruction)
            address = state.reg[regA] + offsetField
            if address < 0 or address >= state.numMemory:
                print(f"ERROR: Invalid memory address: {address} (out of range).")
                return
            state.reg[regB] = state.mem[address]

        elif opcode == 3:  # SW
            regA, regB, offsetField = i_getArgs(instruction)
            address = state.reg[regA] + offsetField
            if address < 0 or address >= state.numMemory:
                print(f"ERROR: Invalid memory address: {address} (out of range).")
                return
            state.mem[address] = state.reg[regB]

        elif opcode == 4:  # BEQ
            regA, regB, offsetField = i_getArgs(instruction)
            if state.reg[regA] == state.reg[regB]:
                state.pc += offsetField
                
        elif opcode == 5:  # JALR
            regA, regB, destReg = r_getArgs(instruction)
            if state.reg[regB] != 0:
                state.reg[destReg] = state.reg[regA]

        elif opcode == 6:  # HALT
            print("machine halted")
            print(f"total of {total_instructions} instructions executed")
            print("final state of machine:")
            printState(state)
            return

        elif opcode == 7:  # NOOP
            pass

        state.pc += 1

        if state.pc >= state.numMemory or state.pc < 0:
            print(f"ERROR: PC is out of range [0, {state.numMemory}). PC value: {state.pc}")
            return

if __name__ == "__main__":
    main()