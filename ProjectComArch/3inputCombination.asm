        lw      0   1   n            # โหลดค่า n (ซึ่งคือ 5) จากหน่วยความจำไปยัง register 1 (reg1 = n)
        lw      0   2   r            # โหลดค่า r (ซึ่งคือ 2) จากหน่วยความจำไปยัง register 2 (reg2 = r)
        lw      0   4   combiAddr    # โหลดค่า combiAddr (ที่อยู่ของฟังก์ชัน combi) ไปยัง register 4 (reg4 = combiAddr)
        jalr    4   7                # กระโดดไปที่ฟังก์ชัน combi โดยเก็บ PC+1 ไว้ใน register 7 (reg7 = PC+1)
        done    halt                 # หยุดการทำงานของโปรแกรม
    #------------------------------------------------------------------------------#
    baseCase
        lw      0   3   one          # โหลดค่า 1 ไปยัง register 3 (reg3 = 1)
        lw      0   6   neg1         # โหลดค่า -1 ไปยัง register 6 (reg6 = -1)
        add     6   5   5            # เพิ่มค่า reg6 (-1) ไปยัง register 5 (stack pointer) (sp = sp - 1)
        add     6   5   5            # ลดค่า stack pointer ลงอีกครั้ง (sp = sp - 2)
        add     6   5   5            # ลดค่า stack pointer ลงอีกครั้ง (sp = sp - 3)
        lw      5   7   stack        # โหลดค่าจาก stack (stack pointer ปัจจุบัน) ไปยัง register 7 (reg7 = ค่าใน stack)
        jalr    7   1                # กระโดดไปยังฟังก์ชันที่อยู่ใน register 7 และเก็บค่า PC+1 ใน register 1        
    #------------------------------------------------------------------------------#
    combi
        lw      0   6   one          # โหลดค่า 1 ไปยัง register 6 (reg6 = 1)
        sw      5   7   stack        # เก็บค่า register 7 ลงใน stack (เก็บ return address)
        add     6   5   5            # เพิ่มค่า stack pointer (sp = sp + 1)
        sw      5   1   stack        # เก็บค่า register 1 (n) ลงใน stack
        add     6   5   5            # เพิ่มค่า stack pointer (sp = sp + 1)
        sw      5   2   stack        # เก็บค่า register 2 (r) ลงใน stack
        add     6   5   5            # เพิ่มค่า stack pointer (sp = sp + 1)

        beq     1   2   baseCase     # ถ้า n == r ให้กระโดดไปที่ baseCase (กรณี n == r)
        beq     0   2   baseCase     # ถ้า r == 0 ให้กระโดดไปที่ baseCase (กรณี r == 0)
        lw      0   6   neg1         # โหลดค่า -1 ไปยัง register 6 (reg6 = -1)
        add     6   1   1            # ลดค่า n (reg1 = reg1 - 1)
        jalr    4   7                # กระโดดไปที่ combi อีกครั้ง (recursive call)

        add     6   5   5            # เพิ่มค่า stack pointer (sp = sp + 1)
        lw      5   2   stack        # โหลดค่า r จาก stack
        add     6   5   5            # เพิ่มค่า stack pointer (sp = sp + 1)
        lw      5   1   stack        # โหลดค่า n จาก stack
        add     6   1   1            # ลดค่า n (reg1 = reg1 - 1)
        add     6   2   2            # ลดค่า r (reg2 = reg2 - 1)
        lw      0   6   one          # โหลดค่า 1 ไปยัง register 6 (reg6 = 1)
        sw      5   3   stack        # เก็บค่า register 3 (ผลลัพธ์) ลงใน stack
        add     6   5   5            # เพิ่มค่า stack pointer (sp = sp + 1)
        jalr    4   7                # กระโดดไปที่ combi อีกครั้ง (recursive call)

        lw      0   6   neg1         # โหลดค่า -1 ไปยัง register 6 (reg6 = -1)    
        add     6   5   5            # เพิ่มค่า stack pointer (sp = sp + 1)
        lw      5   4   stack        # โหลดค่า register 4 จาก stack (เก็บผลลัพธ์ไว้ใน reg4)
        add     4   3   3            # บวกค่า reg4 เข้ากับ reg3 (เพิ่มผลลัพธ์)
        add     6   5   5            # เพิ่มค่า stack pointer (sp = sp + 1)
        lw      5   7   stack        # โหลดค่า return address จาก stack (เก็บไว้ใน reg7)
        lw      0   4   combiAddr    # โหลดที่อยู่ของฟังก์ชัน combi ไปยัง register 4 (reg4 = combiAddr)
        jalr    7   1                # กระโดดกลับไปยัง return address และเก็บ PC+1 ไว้ใน reg1
    #------------------------------------------------------------------------------#
    n                   .fill   3           # กำหนดค่า n เป็น 5
    r                   .fill   1           # กำหนดค่า r เป็น 2
    neg1                .fill   -1          # กำหนดค่า -1 สำหรับใช้ลดค่า
    one                 .fill   1           # กำหนดค่า 1 สำหรับการบวก
    combiAddr           .fill   combi       # ที่อยู่ของฟังก์ชัน combi
    stack               .fill   0           # หน่วยความจำสำหรับ stack
    #------------------------------------------------------------------------------#
