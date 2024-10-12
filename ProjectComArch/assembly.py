import sys

# Constants
MAXLINELENGTH = 1000  # ขนาดสูงสุดของบรรทัดในไฟล์ assembly
MAXLINES = 100000      # ความยาวสูงสุดของโปรแกรม assembly
# รายการของ opcode ที่ใช้ได้
VALID_OPCODES = ['add', 'nand', 'lw', 'sw', 'beq', 'jalr', 'halt', 'noop', '.fill']

# คลาสสำหรับการจัดการ Symbolic Address (Linked List)
class SymbolicAddressNode:
    def __init__(self, label='', address=0):
        self.label = label  # ชื่อ label
        self.address = address  # ที่อยู่ของ label
        self.next = None  # การเชื่อมโยงไปยัง node ถัดไป

# คลาสสำหรับจัดเก็บข้อมูลของคำสั่งแต่ละบรรทัด
class InstructionNode:
    def __init__(self, address=0, opcode='', arg0='', arg1='', arg2=''):
        self.address = address  # ที่อยู่ของคำสั่งในหน่วยความจำ
        self.opcode = opcode  # opcode ของคำสั่ง
        self.arg0 = arg0  # อาร์กิวเมนต์ตัวแรก
        self.arg1 = arg1  # อาร์กิวเมนต์ตัวที่สอง
        self.arg2 = arg2  # อาร์กิวเมนต์ตัวที่สาม

# ฟังก์ชันช่วยในการเปิดไฟล์
def prepare_file(filename, mode):
    try:
        return open(filename, mode, encoding='utf-8')  # พยายามเปิดไฟล์ด้วยโหมดที่ระบุ
    except IOError:
        print(f"ERROR: Can't open file: {filename}!")  # แสดงข้อความเมื่อเปิดไฟล์ไม่สำเร็จ
        sys.exit(1)  # ออกจากโปรแกรมด้วยรหัสสถานะ 1

# ฟังก์ชันตรวจสอบว่า label นั้นถูกต้องหรือไม่
def is_valid_label(label):
    if not label[0].isalpha():  # ตรวจสอบว่าอักขระแรกเป็นตัวอักษรหรือไม่
        return False
    return all(c.isalnum() for c in label)  # ตรวจสอบว่าอักขระทั้งหมดเป็นตัวอักษรหรือตัวเลข

# ฟังก์ชันเพิ่ม Symbolic Address ลงใน linked list
def add_symbol(root, label, address):
    if not is_valid_label(label):  # ตรวจสอบว่า label นั้นถูกต้องหรือไม่
        print(f"ERROR: {label} is not a valid label. (see address {address})")
        sys.exit(1)

    node = root
    while node.next is not None:
        node = node.next
        if node.label == label:  # ตรวจสอบว่า label ซ้ำหรือไม่
            print(f"ERROR: Duplicate label, {label}, found. (see address {address})")
            sys.exit(1)

    new_node = SymbolicAddressNode(label, address)  # สร้าง node ใหม่
    node.next = new_node  # เพิ่ม node ใหม่ใน linked list

# ฟังก์ชันค้นหาที่อยู่ของ Symbolic Label
def get_symbol_address(root, label):
    if not is_valid_label(label):  # ตรวจสอบว่า label นั้นถูกต้องหรือไม่
        print(f"ERROR: {label} is not a valid label.")
        sys.exit(1)

    node = root
    while node.next is not None:
        node = node.next
        if node.label == label:  # พบ label ที่ต้องการแล้ว
            return node.address

    print(f"ERROR: Undeclared label {label}.")  # ไม่พบ label ในลิสต์
    sys.exit(1)

# ฟังก์ชันอ่านคำสั่งจาก assembly file และเก็บใน instruction list
def read_assembly(infile, root, instructions):
    i = 0  # ตัวนับ index
    for line in infile:
        line = line.split('#')[0].strip()  # ลบคอมเม้นต์และตัดช่องว่าง
        if len(line) == 0:
            continue  # ข้ามบรรทัดที่ว่าง

        instructions[i] = InstructionNode(address=i)  # สร้าง node ของคำสั่งใหม่

        # แบ่งบรรทัดเป็นส่วนๆ
        parts = line.split()

        # ตรวจสอบว่าอักขระแรกเป็น label หรือไม่ (ถ้าไม่ใช่ opcode)
        if parts[0] not in VALID_OPCODES and is_valid_label(parts[0]):
            add_symbol(root, parts[0], i)  # เพิ่ม label ลงใน linked list
            parts = parts[1:]  # ลบ label ออกจากบรรทัด

        # ประมวลผลคำสั่งที่เหลือ
        if len(parts) > 0:
            instructions[i].opcode = parts[0]  # เก็บ opcode
        if len(parts) > 1:
            instructions[i].arg0 = parts[1]  # เก็บ argument ตัวแรก
        if len(parts) > 2:
            instructions[i].arg1 = parts[2]  # เก็บ argument ตัวที่สอง
        if len(parts) > 3:
            instructions[i].arg2 = parts[3]  # เก็บ argument ตัวที่สาม

        i += 1
        if i > MAXLINES:  # ตรวจสอบว่าเกินความยาวโปรแกรมที่กำหนดหรือไม่
            print(f"ERROR: Maximum program length exceeded. Maximum: {MAXLINES}")
            sys.exit(1)

    return i

# ฟังก์ชันเขียนการแทนค่าคำสั่งเป็น binary ลงในไฟล์ output
def write_binary(outfile, root, instructions, counter):
    for i in range(counter):
        outfile.write(f"{parse(root, instructions[i])}\n")

# ฟังก์ชันแปลงคำสั่งจาก assembly เป็น binary
def parse(root, inode):
    print(f"Parsed instruction at address: {inode.opcode} {inode.arg0} {inode.arg1} {inode.arg2}")
    if inode.opcode == 'add':
        return r_type(0 << 22, inode.arg0, inode.arg1, inode.arg2)
    elif inode.opcode == 'nand':
        return r_type(1 << 22, inode.arg0, inode.arg1, inode.arg2)
    elif inode.opcode == 'lw' or inode.opcode == 'sw':
        # ตรวจสอบว่า argument เป็น label หรือจำนวนที่มีค่าเป็นลบ
        if inode.arg2.lstrip('-').isdigit():
            offset = int(inode.arg2)  # เป็นตัวเลข (รวมค่าลบด้วย)
        else:
            offset = get_symbol_address(root, inode.arg2)  # เป็น label
        return i_type((2 if inode.opcode == 'lw' else 3) << 22, inode.arg0, inode.arg1, offset)
    elif inode.opcode == 'beq':
        if is_valid_label(inode.arg2):
            label_address = get_symbol_address(root, inode.arg2)
            offset = label_address - (inode.address + 1)  # Offset จะเป็นระยะห่างจากคำสั่งถัดไป
        else:
            offset = int(inode.arg2)
        return i_type(4 << 22, inode.arg0, inode.arg1, offset)
    elif inode.opcode == 'jalr':
        return j_type(5 << 22, inode.arg0, inode.arg1)  # rs ใน arg0, rd ใน arg1
    elif inode.opcode == 'halt':
        return o_type(6 << 22)
    elif inode.opcode == 'noop':
        return o_type(7 << 22)
    elif inode.opcode == '.fill':
        if is_valid_label(inode.arg0):
            return get_symbol_address(root, inode.arg0)
        else:
            return int(inode.arg0)
    else:
        print(f"WARNING: Unrecognized opcode {inode.opcode} at address {inode.address}, skipping...")
        return 0

# ฟังก์ชันแปลงคำสั่ง r-type เป็น binary
def r_type(op, reg1, reg2, dest):
    regA = int(reg1)
    regB = int(reg2)
    destReg = int(dest)
    return (op | (regA << 19) | (regB << 16) | destReg)

# ฟังก์ชันแปลงคำสั่ง i-type เป็น binary
def i_type(op, reg1, reg2, offset):
    regA = int(reg1)
    regB = int(reg2)

    # ตรวจสอบว่า offset อยู่ในช่วงที่กำหนดหรือไม่
    if offset < -32768 or offset > 32767:
        print(f"ERROR: Offset {offset} out of range for I-type instruction")
        sys.exit(1)

    # แปลง offset ที่เป็นลบให้เป็น two's complement แบบ 16-bit
    if offset < 0:
        offset = (1 << 16) + offset  # แปลงเป็น two's complement แบบ 16-bit

    return (op | (regA << 19) | (regB << 16) | offset)

# ฟังก์ชันแปลงคำสั่ง j-type เป็น binary
def j_type(op, reg1, reg2):
    regA = int(reg1)
    regB = int(reg2)
    return (op | (regA << 19) | (regB << 16))

# ฟังก์ชันแปลงคำสั่ง o-type เป็น binary
def o_type(op):
    return op

# ฟังก์ชันหลัก
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"ERROR: Usage: {sys.argv[0]} <assembly-code-file> <machine-code-file>")
        sys.exit(1)

    infile = prepare_file(sys.argv[1], 'r')  # เปิดไฟล์ assembly
    outfile = prepare_file(sys.argv[2], 'w+')  # เปิดไฟล์สำหรับเขียน output

    symbol_list = SymbolicAddressNode()  # สร้าง linked list สำหรับเก็บ label
    instructions = [None] * MAXLINES  # สร้าง array สำหรับเก็บคำสั่ง

    instruction_counter = read_assembly(infile, symbol_list, instructions)  # อ่านคำสั่งจากไฟล์
    write_binary(outfile, symbol_list, instructions, instruction_counter)  # เขียนคำสั่งเป็น binary ลงไฟล์

    infile.close()
    outfile.close()