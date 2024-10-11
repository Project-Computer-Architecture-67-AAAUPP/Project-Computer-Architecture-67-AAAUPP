NUMMEMORY = 65536  # จำนวนคำสูงสุดในหน่วยความจำ
NUMREGS = 8  # จำนวนเรจิสเตอร์
MAXLINELENGTH = 1000  # ขนาดสูงสุดของแต่ละบรรทัดในไฟล์

class State:
    def __init__(self):
        self.pc = 0
        self.mem = [0] * NUMMEMORY
        self.reg = [0] * NUMREGS
        self.numMemory = 0

def printState(state, output_file):
    """แสดงสถานะของเครื่องจำลอง"""
    output_file.write("\n@@@\nstate:\n")
    output_file.write(f"\tpc {state.pc}\n")
    output_file.write("\tmemory:\n")
    for i in range(state.numMemory):
        output_file.write(f"\t\tmem[ {i} ] {state.mem[i]}\n")
    output_file.write("\tregisters:\n")
    for i in range(NUMREGS):
        output_file.write(f"\t\treg[ {i} ] {state.reg[i]}\n")
    output_file.write("end state\n")

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

def j_getArgs(bitstring):
    """ถอดรหัสคำสั่ง J-type"""
    regA = (bitstring >> 19) & 0x7  # Extract regA from bits 24-22
    regB = (bitstring >> 16) & 0x7  # Extract regB from bits 21-19
    return regA, regB

def o_getArgs(bitstring):
    """ถอดรหัสคำสั่ง O-type"""
    return None

def main():
    import sys

    if len(sys.argv) != 2:
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
    output_filename = "Simulator" + filename[2:-3] + ".txt"   # เปลี่ยนชื่อไฟล์ที่บันทึก
    with open(output_filename, 'w') as output_file:  # เปิดไฟล์สำหรับเขียน
        for line in lines:
            if state.numMemory >= NUMMEMORY:
                print(f"ERROR: Max number of words exceeded. Max: {NUMMEMORY}")
                return
            try:
                state.mem[state.numMemory] = int(line.strip())
                output_file.write(f"memory[{state.numMemory}]={state.mem[state.numMemory]}\n")
                state.numMemory += 1
            except ValueError:
                print(f"ERROR: Failed to read address {line.strip()}")
                return

        total_instructions = 0
        while True:
            total_instructions += 1
            printState(state, output_file)  # แสดงสถานะในไฟล์

            instruction = state.mem[state.pc]
            opcode = instruction >> 22

            # พิมพ์ค่า PC และ instruction ก่อนทำงาน
            output_file.write(f"PC = {state.pc}, Instruction = {instruction}, Opcode = {opcode}\n")
            
            if opcode == 0:  # ADD
                regA, regB, destReg = r_getArgs(instruction)
                state.reg[destReg] = state.reg[regA] + state.reg[regB]
                output_file.write(f"ADD: reg[{destReg}] = reg[{regA}] + reg[{regB}]\n")

            elif opcode == 1:  # NAND
                regA, regB, destReg = r_getArgs(instruction)
                state.reg[destReg] = ~(state.reg[regA] & state.reg[regB])
                output_file.write(f"NAND: reg[{destReg}] = ~(reg[{regA}] & reg[{regB}])\n")

            elif opcode == 2:  # LW
                regA, regB, offsetField = i_getArgs(instruction)
                address = state.reg[regA] + offsetField
                if address < 0 or address >= state.numMemory:
                    output_file.write(f"ERROR: Invalid memory address: {address} (out of range).\n")
                    return
                state.reg[regB] = state.mem[address]
                output_file.write(f"LW: reg[{regB}] = mem[{address}]\n")

            elif opcode == 3:  # SW
                regA, regB, offsetField = i_getArgs(instruction)
                address = state.reg[regA] + offsetField
                if address < 0 or address >= state.numMemory:
                    output_file.write(f"ERROR: Invalid memory address: {address} (out of range).\n")
                    return
                state.mem[address] = state.reg[regB]
                output_file.write(f"SW: mem[{address}] = reg[{regB}]\n")

            elif opcode == 4:  # BEQ
                regA, regB, offsetField = i_getArgs(instruction)
                output_file.write(f"BEQ: Checking if reg[{regA}] == reg[{regB}]\n")
                if state.reg[regA] == state.reg[regB]:
                    new_pc = state.pc + offsetField
                    output_file.write(f"BEQ: Jump to new PC = {new_pc}\n")
                    if new_pc < 0 or new_pc >= state.numMemory:
                        output_file.write(f"ERROR: PC is out of range after BEQ: {new_pc}\n")
                        return
                    state.pc = new_pc
                else:
                    output_file.write("BEQ: No jump, registers are not equal.\n")

            elif opcode == 5:  # JALR
                regA, regB = j_getArgs(instruction)
                output_file.write(f"JALR: Jumping to address {state.reg[regA]} from PC = {state.pc}\n")
                if state.reg[regB] != 0:  # Check if regB is not zero
                    state.reg[destReg] = state.pc + 1  # Save return address
                    state.pc = state.reg[regA]  # Jump to the address in regA

            elif opcode == 6:  # HALT
                o_getArgs(instruction)
                output_file.write("machine halted\n")
                output_file.write(f"total of {total_instructions} instructions executed\n")
                output_file.write("final state of machine:\n")
                printState(state, output_file)  # แสดงสถานะในไฟล์
                return

            elif opcode == 7:  # NOOP
                o_getArgs(instruction)
                output_file.write("NOOP: No operation\n")

            state.pc += 1

            if state.pc >= state.numMemory or state.pc < 0:
                output_file.write(f"ERROR: PC is out of range [0, {state.numMemory}). PC value: {state.pc}\n")
                return

if __name__ == "__main__":
    main()
