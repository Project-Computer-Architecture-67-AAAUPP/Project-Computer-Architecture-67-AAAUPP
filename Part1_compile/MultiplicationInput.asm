# Multiplication Assembler
        lw      0       1       mcand       # โหลดค่า multiplicand ลงใน reg1 (ตัวตั้ง)
        lw      0       2       mplier      # โหลดค่า multiplier ลงใน reg2 (ตัวคูณ)
        lw      0       3       zero        # โหลดค่า 0 ลงใน reg3 (ผลลัพธ์การคูณ)
        lw      0       4       one         # โหลดค่า 1 ลงใน reg4 สำหรับใช้ลูป
loop    beq     2       0       done        # ถ้า reg2 (multiplier) เป็น 0, ให้ข้ามไปที่ done
        add     3       1       3           # เพิ่ม reg1 (multiplicand) ลงใน reg3 (ผลลัพธ์)
        add     2       4       2           # ลดค่า reg2 (multiplier) ลง 1
        beq     0       0       loop        # กลับไปที่ loop เพื่อทำซ้ำ
done    halt                                # จบการทำงาน
mcand   .fill   6                           # ค่า multiplicand (ตัวตั้งคูณ) = 6
mplier  .fill   4                           # ค่า multiplier (ตัวคูณ) = 4
zero    .fill   0                           # กำหนดค่า 0
one     .fill   -1                          # กำหนดค่า -1 สำหรับใช้ลดค่า multiplier



