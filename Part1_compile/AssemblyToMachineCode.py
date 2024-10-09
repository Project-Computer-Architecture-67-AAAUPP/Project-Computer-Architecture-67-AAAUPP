import sys

# แปลง opcode เป็นเลขฐานสอง (สำหรับแต่ละ instruction)
OPCODES = {
    'add': '000',
    'nand': '001',
    'lw': '010',
    'sw': '011',
    'beq': '100',
    'jalr': '101',
    'halt': '110',
    'noop': '111'
}

# Function สำหรับรัน pass แรก เพื่อเก็บ label และ address ของ label นั้น
def first_pass(input_file):
    labels = {}  # เก็บ label และ address ที่ตรงกับ label นั้นๆ
    address = 0  # เริ่มที่ address 0
    # เปิดไฟล์ assembly language เพื่ออ่าน
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            parts = line.split()
            # ข้ามบรรทัดที่ว่างเปล่าหรือเป็นคอมเมนต์
            if len(parts) > 0 and not parts[0].startswith('#'):
                # ตรวจสอบว่า parts[0] คือ label หรือไม่ (ไม่ใช่ opcode และไม่ใช่ .fill)
                if parts[0] not in OPCODES and parts[0] != '.fill':
                    # ตรวจสอบว่า label ซ้ำหรือไม่
                    if parts[0] in labels:
                        print(f"Error: Duplicate label '{parts[0]}' at address {address}")
                        sys.exit(1)  # หากเจอ label ซ้ำ ให้หยุดการทำงาน
                    # เก็บ label และ address ที่เจอ
                    labels[parts[0]] = address
                # ทุกบรรทัดของ assembly code จะเพิ่ม address ขึ้น 1 เสมอ
                address += 1
    return labels  # คืนค่า dictionary ของ labels ที่เจอทั้งหมด

# Function สำหรับแปลง assembly instruction เป็น machine code
def assemble_instruction(line, labels, current_address):
    parts = line.split()  # แยกบรรทัด assembly เป็นแต่ละส่วน
    if len(parts) == 0 or parts[0].startswith('#'):
        return None  # ข้ามบรรทัดว่างเปล่าหรือคอมเมนต์

    # ถ้าบรรทัดมี label ให้ข้าม label ไปเริ่มอ่าน instruction
    if parts[0] not in OPCODES and parts[0] != '.fill':
        parts = parts[1:]

    instruction = parts[0]  # ดึงคำสั่ง opcode
    if instruction in OPCODES:
        opcode = OPCODES[instruction]  # แปลง opcode เป็นเลขฐานสอง
        if instruction in ['add', 'nand']:  # R-type instruction
            reg_a = int(parts[1])  # register A
            reg_b = int(parts[2])  # register B
            dest_reg = int(parts[3])  # destination register
            # สร้าง machine code โดยบิตที่ 31-25 ถูกตั้งเป็น 0 เสมอ
            return f"{'0' * 7}{opcode}{reg_a:03b}{reg_b:03b}{'0' * 13}{dest_reg:03b}"
        elif instruction in ['lw', 'sw', 'beq']:  # I-type instruction
            reg_a = int(parts[1])  # register A
            reg_b = int(parts[2])  # register B
            offset_field = parts[3]  # offset field

            # ตรวจสอบว่า offset_field เป็น label หรือไม่
            if offset_field in labels:
                # ตรวจสอบว่าเป็นคำสั่ง beq หรือไม่
                if instruction == 'beq':
                    # สำหรับ beq ต้องคำนวณ offset โดยใช้ (current_address + 1)
                    offset = labels[offset_field] - (current_address + 1)
                else:
                    # สำหรับ lw, sw ให้ใช้ current_address ตรงๆ
                    offset = labels[offset_field] - current_address
            else:
                try:
                    # ถ้าไม่ใช่ label, ให้แปลงเป็นตัวเลขตรงๆ
                    offset = int(offset_field)
                except ValueError:
                    # ถ้า offset ไม่เป็นตัวเลขหรือ label ให้แสดง error และหยุดการทำงาน
                    print(f"Error: Invalid offset or label in line: {line}")
                    sys.exit(1)

            # ตรวจสอบว่า offset อยู่ในช่วง 16-bit two's complement (-32768 ถึง 32767)
            if offset < -32768 or offset > 32767:
                print(f"Error: Offset {offset} out of range at line: {line}")
                sys.exit(1)

            # แปลง offset เป็น 16-bit two's complement
            offset = offset & 0xFFFF  # เก็บเฉพาะ 16 บิต
            # สร้าง machine code โดยบิตที่ 31-25 ถูกตั้งเป็น 0 เสมอ
            return f"{'0' * 7}{opcode}{reg_a:03b}{reg_b:03b}{offset:016b}"

        elif instruction == 'jalr':  # J-type instruction
            reg_a = int(parts[1])  # register A
            reg_b = int(parts[2])  # register B
            # สร้าง machine code โดยบิตที่ 31-25 ถูกตั้งเป็น 0 เสมอ
            return f"{'0' * 7}{opcode}{reg_a:03b}{reg_b:03b}{'0' * 16}"
        elif instruction in ['halt', 'noop']:  # O-type instruction
            # สร้าง machine code โดยบิตที่ 31-25 ถูกตั้งเป็น 0 เสมอ
            return f"{'0' * 7}{opcode}" + "0" * 22
    elif instruction == '.fill':  # จัดการคำสั่ง .fill
        value = parts[1]  # value ที่จะใช้ใน .fill
        if value in labels:
            # ถ้า value เป็น label คืนค่า address ของ label นั้น
            return str(labels[value])
        else:
            try:
                # ถ้า value เป็นตัวเลข คืนค่าตัวเลขนั้นตรงๆ
                return str(int(value))
            except ValueError:
                # ถ้า value ไม่ใช่ตัวเลขหรือ label ให้แสดง error และหยุดการทำงาน
                print(f"Error: Invalid .fill value in line: {line}")
                sys.exit(1)
    return None  # ถ้าคำสั่งไม่ถูกต้อง

# Function สำหรับอ่านไฟล์ assembly และแปลงเป็น machine code
def assemble(input_file, output_file):
    labels = first_pass(input_file)  # รวบรวม label และ address ก่อน
    # เปิดไฟล์เพื่ออ่าน assembly และเขียน machine code
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        address = 0  # เริ่มที่ address 0
        for line in infile:
            parts = line.split()  # แยกแต่ละบรรทัด assembly
            if len(parts) == 0 or parts[0].startswith('#'):
                continue  # ข้ามบรรทัดว่างหรือคอมเมนต์
            # แปลง assembly instruction เป็น machine code
            machine_code = assemble_instruction(line, labels, address)
            if machine_code is not None:
                if parts[0] == '.fill' or (len(parts) > 1 and parts[1] == '.fill'):
                    # แปลงค่าของ .fill เป็น decimal
                    value = int(machine_code)
                else:
                    # แปลง machine code เป็น integer จากเลขฐานสอง
                    value = int(machine_code, 2)

                # แปลง machine code เป็นเลขฐาน 16 และ 2
                # hex_value = hex(value & 0xFFFFFFFF)  # แปลงเป็นเลขฐาน 16
                # bin_value = bin(value & 0xFFFFFFFF)[2:].zfill(32)  # แปลงเป็นเลขฐาน 2 ให้มี 32 บิต
                # เขียนผลลัพธ์ลงไฟล์พร้อม address และค่าในฐาน 10, 16, 2
                # outfile.write(f"(address {address}): {value} (hex {hex_value}) (binary {bin_value})\n")
                # เขียนเฉพาะค่าในฐาน 10 ลงในไฟล์
                outfile.write(f"{value}\n")
            address += 1  # เพิ่ม address หลังจากอ่านแต่ละบรรทัด

# ตรวจสอบว่าโปรแกรมถูกเรียกใช้งานถูกต้อง
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python AssemblyToMachineCode.py <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]  # ไฟล์ input (assembly)
    output_file = sys.argv[2]  # ไฟล์ output (machine code)
    assemble(input_file, output_file)  # เรียกใช้ฟังก์ชัน assemble เพื่อแปลงไฟล์
    print(f"Assembly to Machine Code completed. Output written to {output_file}")
