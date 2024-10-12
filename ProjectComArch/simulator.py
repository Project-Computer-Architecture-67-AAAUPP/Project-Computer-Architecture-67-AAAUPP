NUMMEMORY = 65536  # จำนวนคำสูงสุดในหน่วยความจำ
NUMREGS = 8  # จำนวนเรจิสเตอร์
MAXLINELENGTH = 1000  # ขนาดสูงสุดของแต่ละบรรทัดในไฟล์

# คลาสสำหรับสถานะของเครื่องจำลอง
class State:
    def __init__(self):
        self.pc = 0  # ตัวนับโปรแกรม (Program Counter)
        self.mem = [0] * NUMMEMORY  # หน่วยความจำที่กำหนดไว้สูงสุด
        self.reg = [0] * NUMREGS  # เรจิสเตอร์ทั้งหมด 8 ตัว
        self.numMemory = 0  # ตัวแปรเก็บจำนวนคำที่ใช้ในหน่วยความจำ

# ฟังก์ชันสำหรับพิมพ์สถานะของเครื่องจำลองลงไฟล์
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

# ฟังก์ชันแปลงตัวเลข 16-bit ให้เป็น 32-bit (ใช้กับ I-type)
def convertNum(num):
    """แปลงค่า 16-bit เป็น 32-bit"""
    if num & (1 << 15):
        num -= (1 << 16)  # แปลงค่าถ้าหากเป็นเลขลบ
    return num

# ฟังก์ชันถอดรหัสคำสั่งประเภท R-type
def r_getArgs(bitstring):
    """ถอดรหัสคำสั่ง R-type"""
    regA = (bitstring >> 19) & 0x7  # ค่าเรจิสเตอร์ A
    regB = (bitstring >> 16) & 0x7  # ค่าเรจิสเตอร์ B
    destReg = bitstring & 0x7  # ค่าเรจิสเตอร์ปลายทาง
    return regA, regB, destReg

# ฟังก์ชันถอดรหัสคำสั่งประเภท I-type
def i_getArgs(bitstring):
    """ถอดรหัสคำสั่ง I-type"""
    regA = (bitstring >> 19) & 0x7  # ค่าเรจิสเตอร์ A
    regB = (bitstring >> 16) & 0x7  # ค่าเรจิสเตอร์ B
    offsetField = bitstring & 0xFFFF  # ค่า offset
    offsetField = convertNum(offsetField)  # แปลงค่า offset
    return regA, regB, offsetField

# ฟังก์ชันถอดรหัสคำสั่งประเภท J-type
def j_getArgs(bitstring):
    """ถอดรหัสคำสั่ง J-type"""
    regA = (bitstring >> 19) & 0x7  # ค่าเรจิสเตอร์ A
    regB = (bitstring >> 16) & 0x7  # ค่าเรจิสเตอร์ B
    return regA, regB

# ฟังก์ชันถอดรหัสคำสั่งประเภท O-type
def o_getArgs(bitstring):
    """ถอดรหัสคำสั่ง O-type"""
    return None

# ฟังก์ชันหลักของโปรแกรมจำลอง
def main():
    import sys

    # ตรวจสอบว่าใส่ argument ในการเรียกใช้ถูกต้องหรือไม่
    if len(sys.argv) != 2:
        print(f"error: usage: {sys.argv[0]} <machine-code file>")
        return

    # เปิดไฟล์ machine code
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()  # อ่านบรรทัดทั้งหมดจากไฟล์
    except FileNotFoundError:
        print(f"ERROR: Can't open file {filename}")  # แสดงข้อผิดพลาดถ้าไฟล์ไม่พบ
        return

    # ตั้งค่าเริ่มต้น
    state = State()  # สร้างออบเจ็ค State สำหรับเครื่องจำลอง
    output_filename = "Simulator" + filename[2:-3] + ".txt"  # ชื่อไฟล์สำหรับบันทึกผลลัพธ์
    with open(output_filename, 'w') as output_file:  # เปิดไฟล์สำหรับเขียน
        for line in lines:
            if state.numMemory >= NUMMEMORY:
                print(f"ERROR: Max number of words exceeded. Max: {NUMMEMORY}")
                return
            try:
                state.mem[state.numMemory] = int(line.strip())  # เก็บคำสั่งลงในหน่วยความจำ
                output_file.write(f"memory[{state.numMemory}]={state.mem[state.numMemory]}\n")
                state.numMemory += 1
            except ValueError:
                print(f"ERROR: Failed to read address {line.strip()}")  # ข้อผิดพลาดถ้าอ่านคำสั่งไม่สำเร็จ
                return

        total_instructions = 0
        while True:
            total_instructions += 1
            printState(state, output_file)  # แสดงสถานะในไฟล์

            instruction = state.mem[state.pc]  # อ่านคำสั่งจากหน่วยความจำ
            opcode = instruction >> 22  # ดึงค่า opcode

            # พิมพ์ค่า PC และ instruction ก่อนทำงาน
            output_file.write(f"PC = {state.pc}, Instruction = {instruction}, Opcode = {opcode}\n")
            
            if opcode == 0:  # ADD
                regA, regB, destReg = r_getArgs(instruction)
                state.reg[destReg] = state.reg[regA] + state.reg[regB]  # บวกค่าเรจิสเตอร์ A และ B
                output_file.write(f"ADD: reg[{destReg}] = reg[{regA}] + reg[{regB}]\n")

            elif opcode == 1:  # NAND
                regA, regB, destReg = r_getArgs(instruction)
                state.reg[destReg] = ~(state.reg[regA] & state.reg[regB])  # นำค่าของเรจิสเตอร์ A และ B มาทำ NAND
                output_file.write(f"NAND: reg[{destReg}] = ~(reg[{regA}] & reg[{regB}])\n")

            elif opcode == 2:  # LW (Load Word)
                regA, regB, offsetField = i_getArgs(instruction)
                address = state.reg[regA] + offsetField  # คำนวณที่อยู่ในหน่วยความจำ
                if address < 0 or address >= NUMMEMORY:
                    output_file.write(f"ERROR: Invalid memory address: {address} (out of range).\n")
                    return
                state.reg[regB] = state.mem[address]  # โหลดค่าจากหน่วยความจำเข้าเรจิสเตอร์
                output_file.write(f"LW: reg[{regB}] = mem[{address}]\n")

            elif opcode == 3:  # SW (Store Word)
                regA, regB, offsetField = i_getArgs(instruction)
                address = state.reg[regA] + offsetField  # คำนวณที่อยู่ในหน่วยความจำ
                if address < 0 or address >= NUMMEMORY:
                    output_file.write(f"ERROR: Invalid memory address: {address} (out of range).\n")
                    return
                state.mem[address] = state.reg[regB]  # เก็บค่าจากเรจิสเตอร์ลงหน่วยความจำ
                output_file.write(f"SW: mem[{address}] = reg[{regB}]\n")

            elif opcode == 4:  # BEQ (Branch if Equal)
                regA, regB, offsetField = i_getArgs(instruction)
                output_file.write(f"BEQ: Checking if reg[{regA}] == reg[{regB}]\n")
                if state.reg[regA] == state.reg[regB]:  # ตรวจสอบว่าเรจิสเตอร์ A และ B มีค่าเท่ากันหรือไม่
                    new_pc = state.pc + offsetField  # เปลี่ยนค่า PC
                    output_file.write(f"BEQ: Jump to PC{new_pc+1}\n")
                    if new_pc < 0 or new_pc >= state.numMemory:
                        output_file.write(f"ERROR: PC is out of range after BEQ: {new_pc}\n")
                        return
                    state.pc = new_pc
                else:
                    output_file.write("BEQ: No jump, registers are not equal.\n")  # ไม่กระโดด

            elif opcode == 5:  # JALR (Jump and Link Register)
                regA, regB = j_getArgs(instruction)
                output_file.write(f"JALR: Jumping to address {state.reg[regA]} from PC = {state.pc}\n")
                state.reg[regB] = state.pc + 1  # บันทึกค่า PC ปัจจุบันลงใน regB
                state.pc = state.reg[regA] - 1  # กระโดดไปยังที่อยู่ใน regA

            elif opcode == 6:  # HALT (หยุดการทำงาน)
                o_getArgs(instruction)
                output_file.write("machine halted\n")
                output_file.write(f"total of {total_instructions} instructions executed\n")
                output_file.write("final state of machine:\n")
                printState(state, output_file)  # แสดงสถานะในไฟล์
                return

            elif opcode == 7:  # NOOP (ไม่ทำอะไร)
                o_getArgs(instruction)
                output_file.write("NOOP: No operation\n")

            state.pc += 1  # เพิ่มค่า PC

            if state.pc >= state.numMemory or state.pc < 0:
                output_file.write(f"ERROR: PC is out of range [0, {state.numMemory}). PC value: {state.pc}\n")
                return

if __name__ == "__main__":
    main()