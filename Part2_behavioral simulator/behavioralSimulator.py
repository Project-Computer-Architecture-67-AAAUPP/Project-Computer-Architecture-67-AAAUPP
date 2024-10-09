def convertNum(num):
    """
    แปลงเลข 16 บิตให้เป็นเลข 32 บิตโดยใช้การขยาย sign (sign extension)
    ฟังก์ชันนี้จะใช้เพื่อแปลงค่าที่เป็น 16-bit 2's complement 
    ไปเป็นค่า 32-bit integer เพื่อรักษาความหมายของเลขลบ

    Parameters:
    num (int): เลข 16 บิตที่จะแปลง (อาจจะเป็นบวกหรือลบใน 2's complement)

    Returns:
    int: เลข 32 บิตที่ถูกแปลงแล้ว

    ตัวอย่าง:
    - convertNum(1000) -> 1000 (บวก, คงค่าเดิม)
    - convertNum(0xFFFF) -> -1 (ลบ, แปลงเป็นค่า 32 บิต)
    """
    if num & (1 << 15):  # ถ้า bit ที่ 15 ของ num มีค่าเป็น 1 (หมายถึงเลขลบใน 16-bit)
        num -= (1 << 16)  # ลบ 65536 เพื่อขยาย sign เป็นเลขลบ 32-bit
    return num


def printState(pc, reg, memory, memory_size):
    """
    แสดงสถานะปัจจุบันของโปรแกรม (program counter, ค่าใน registers, และ memory)
    
    Parameters:
    pc (int): ค่า program counter ปัจจุบัน (ตำแหน่งคำสั่งในหน่วยความจำ)
    reg (list): ลิสต์ที่เก็บค่าของ 8 registers (32-bit แต่ละตัว)
    memory (list): หน่วยความจำที่เก็บ machine code และข้อมูล
    memory_size (int): ขนาดของหน่วยความจำ (บอกจำนวนที่ต้องการพิมพ์)

    Returns:
    None: ฟังก์ชันนี้จะพิมพ์สถานะของเครื่องออกมาที่หน้าจอ
    """
    print("\n" + "@@@")
    print("state:")
    print(f"\tpc {pc}")
    print("\tmemory:")
    for i in range(memory_size):
        print(f"\t\tmem[ {i} ] {memory[i]}")
    print("\tregisters:")
    for i in range(8):
        print(f"\t\treg[ {i} ] {reg[i]}")
    print("end state")


def simulate(memory, memory_size):
    """
    จำลองการทำงานของเครื่อง SMC โดยใช้ machine code ที่อยู่ในหน่วยความจำ
    """
    reg = [0] * 8  # ตั้งค่า registers 8 ตัวให้เป็น 0
    pc = 0  # ค่า program counter เริ่มที่ 0
    running = True
    instruction_count = 0

    while running:
        # ดึงคำสั่งจาก memory
        instruction = memory[pc]
        printState(pc, reg, memory, memory_size)

        # ถอดรหัสคำสั่ง
        opcode = (instruction >> 22) & 0x7  # ดึง bits 24-22 เพื่อหา opcode
        regA = (instruction >> 19) & 0x7
        regB = (instruction >> 16) & 0x7
        destReg = instruction & 0x7
        offsetField = convertNum(instruction & 0xFFFF)  # offsetField 16-bit

        # ประมวลผลคำสั่ง
        if opcode == 0:  # add
            reg[destReg] = reg[regA] + reg[regB]
        elif opcode == 1:  # nand
            reg[destReg] = ~(reg[regA] & reg[regB])
        elif opcode == 2:  # lw (load)
            reg[regB] = memory[reg[regA] + offsetField]
        elif opcode == 3:  # sw (store)
            memory[reg[regA] + offsetField] = reg[regB]
        elif opcode == 4:  # beq (branch if equal)
            if reg[regA] == reg[regB]:
                pc += offsetField
        elif opcode == 5:  # jalr (jump and link register)
            reg[regB] = pc + 1
            pc = reg[regA] - 1  # -1 เพราะ pc จะถูกเพิ่มขึ้นหลังจากนี้
        elif opcode == 6:  # halt
            running = False
        elif opcode == 7:  # noop (no operation)
            pass

        # พิมพ์ค่าที่เกี่ยวข้องในแต่ละคำสั่ง
        print(f"pc={pc}, opcode={opcode}, regA={regA}, regB={regB}, destReg={destReg}, offsetField={offsetField}")
        
        pc += 1  # เลื่อนไปยังคำสั่งถัดไป
        instruction_count += 1

    # แสดงผลสถานะสุดท้ายหลังจาก halt
    # พิมพ์สถานะสุดท้ายเมื่อเครื่องหยุดทำงาน
    print("machine halted")
    print(f"total of {instruction_count} instructions executed")
    print("final state of machine:")
    printState(pc, reg, memory, memory_size)


def load_memory_from_file(file_path):
    """
    อ่าน machine code จากไฟล์และโหลดเข้าไปใน memory list
    
    Parameters:
    file_path (str): ที่อยู่ของไฟล์ machine code (เช่น output.mc)
    
    Returns:
    list: ลิสต์ของ machine code ที่จะถูกเก็บไว้ใน memory
    """
    memory = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # ตรวจสอบว่าบรรทัดไม่ใช่ค่าว่าง
                memory.append(int(line))
    return memory
  

def print_memory(memory):
    """
    แสดงค่าทั้งหมดใน memory
    """
    for i in range(len(memory)):
        print(f"memory[{i}]={memory[i]}")

# โหลด machine code จากไฟล์ output.mc
memory = load_memory_from_file('../Part1_compile/TestOutput.mc')
# เรียกใช้ simulator กับ machine code ที่โหลดมา
print_memory(memory)
simulate(memory, len(memory))



