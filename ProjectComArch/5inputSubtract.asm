        lw      0       1       A           # Load A ลงใน reg1
        lw      0       2       B           # Load B ลงใน reg2
        lw      0       3       zero        # Load 0 ลงใน reg3 (สำหรับเก็บผลลัพธ์)
        lw      0       4       pos1        # Load pos1 ลงใน reg4
        nand    2       2       2           # NOT B (เปลี่ยน B เป็นค่าลบ)
        add     2       4       2           # เพิ่ม 1 เพื่อทำ two's complement (ค่าลบ)
        add     1       2       3           # A - B = A + (-B), เก็บผลลัพธ์ใน reg3
done    halt                                # จบการทำงาน
#------------------------------------------------------------------------------#
A       .fill   5                           # ค่า A
B       .fill   -4                          # ค่า B
zero    .fill   0                           # ค่าเริ่มต้น 0
pos1    .fill   1                           # สำหรับ+1 ในการทำ 2 complement