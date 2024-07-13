import cocotb
from cocotb.types import Logic
from cocotb.triggers import Timer
import random
import math
from random import randint

async def run_inputs(dut, a, b, debug):
    dut.rstn_.setimmediatevalue(0)
    await Timer(2, units="ns")
    dut.rstn_.setimmediatevalue(1)
    dut.a.setimmediatevalue(a)
    dut.b.setimmediatevalue(b)
    dut.en.setimmediatevalue(1)
    if (debug == True):
        time_pass = 0
        while (time_pass <= 28):
            await Timer(time_pass, units="ns")
            #assert dut.gen_pg[0].p_reg_array.value.integer == a ^ b
            #assert dut.gen_pg[0].g_reg_array.value.integer == a & b
            # print(dir(dut))
            # if (debug == 0):
            #     print(dut.gen_pg[0].p_reg_array.value.integer)
            #     assert dut.gen_pg[0].p_reg_array.value.integer == a ^ b
            #     assert dut.gen_pg[0].g_reg_array.value.integer == a & b
            # if (debug == 1):
            #     print(dut.gen_pg[1].p_reg_array.value.integer)
            p_reg_array_val_calc = 0
            g_reg_array_val_calc = 0
            i = 62
            while ( i >= 0 ):
                
                p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[0].p_reg_array.value[i+1]) & int(dut.gen_pg[0].p_reg_array.value[i]))
                # (pi & giprev) | gi
                g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[0].p_reg_array.value[i+1]) & int(dut.gen_pg[0].g_reg_array.value[i])) | (int(dut.gen_pg[0].g_reg_array.value[i+1]))
                if ( i > 0 ):
                    p_reg_array_val_calc = p_reg_array_val_calc << 1
                    g_reg_array_val_calc = g_reg_array_val_calc << 1
                    #print(p_reg_array_val_calc)
                i -= 1
                #assert dut.gen_pg[1].p_reg_array.value[i].integer == dut.gen_pg[0].p_reg_array[i+1].value.integer & dut.gen_pg[0].p_reg_array[i].value.integer
                #assert dut.gen_pg[1].g_reg_array.value[i].integer == (dut.gen_pg[0].p_reg_array[i+1].value.integer & dut.gen_pg[0].g_reg_array[i].value.integer) | dut.gen_pg[0].g_reg_array[i+1]
            #print(f"Expected gen_pg[1].p_reg_array value: {hex(p_reg_array_val_calc)}")
            #print(f"Actual gen_pg[1].p_reg_array value:   {hex(int(dut.gen_pg[1].p_reg_array.value))}")
            #print(f"Expected gen_pg[1].g_reg_array value: {hex(g_reg_array_val_calc)}")
            #print(f"Actual gen_pg[1].g_reg_array value:   {hex(int(dut.gen_pg[1].g_reg_array.value))}")

            p_reg_array_val_calc = 0
            g_reg_array_val_calc = 0
            i = 61
            while ( i >= 0 ):
                if ( i == 0 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[1].p_reg_array.value[1]) & int(dut.gen_pg[0].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[1].p_reg_array.value[1]) & int(dut.gen_pg[0].g_reg_array.value[0])) | (int(dut.gen_pg[1].g_reg_array.value[1]))
                elif ( i >= 1 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[1].p_reg_array.value[i+1]) & int(dut.gen_pg[1].p_reg_array.value[i-1]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[1].p_reg_array.value[i+1]) & int(dut.gen_pg[1].g_reg_array.value[i-1])) | (int(dut.gen_pg[1].g_reg_array.value[i+1]))
                if ( i > 0 ):
                    p_reg_array_val_calc = p_reg_array_val_calc << 1
                    g_reg_array_val_calc = g_reg_array_val_calc << 1
                i -= 1
            #print(f"Expected gen_pg[2].p_reg_array value: {hex(p_reg_array_val_calc)}")
            #print(f"Actual gen_pg[2].p_reg_array value:   {hex(int(dut.gen_pg[2].p_reg_array.value))}")
            #print(f"Expected gen_pg[2].g_reg_array value: {hex(g_reg_array_val_calc)}")
            #print(f"Actual gen_pg[2].g_reg_array value:   {hex(int(dut.gen_pg[2].g_reg_array.value))}")

            p_reg_array_val_calc = 0
            g_reg_array_val_calc = 0
            i = 59
            while ( i >= 0 ):
                if ( i == 0 ):
                    # (pi & giprev) | gi
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[2].p_reg_array.value[2]) & int(dut.gen_pg[0].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[2].p_reg_array.value[2]) & int(dut.gen_pg[0].g_reg_array.value[0])) | (int(dut.gen_pg[2].g_reg_array.value[2]))
                elif ( i == 1 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[2].p_reg_array.value[3]) & int(dut.gen_pg[1].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[2].p_reg_array.value[3]) & int(dut.gen_pg[1].g_reg_array.value[0])) | (int(dut.gen_pg[2].g_reg_array.value[3]))

                elif ( i >= 2 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[2].p_reg_array.value[i+2]) & int(dut.gen_pg[2].p_reg_array.value[i-2]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[2].p_reg_array.value[i+2]) & int(dut.gen_pg[2].g_reg_array.value[i-2])) | (int(dut.gen_pg[2].g_reg_array.value[i+2]))

                if ( i > 0 ):
                    p_reg_array_val_calc = p_reg_array_val_calc << 1
                    g_reg_array_val_calc = g_reg_array_val_calc << 1
                i -= 1
            #print(f"Expected gen_pg[3].p_reg_array value: {hex(p_reg_array_val_calc)}")
            #print(f"Actual gen_pg[3].p_reg_array value:   {hex(int(dut.gen_pg[3].p_reg_array.value))}")
            #print(f"Expected gen_pg[3].g_reg_array value: {hex(g_reg_array_val_calc)}")
            #print(f"Actual gen_pg[3].g_reg_array value:   {hex(int(dut.gen_pg[3].g_reg_array.value))}")

            p_reg_array_val_calc = 0
            g_reg_array_val_calc = 0
            i = 55
            while ( i >= 0 ):
                if ( i == 0 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[3].p_reg_array.value[4]) & int(dut.gen_pg[0].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[3].p_reg_array.value[4]) & int(dut.gen_pg[0].g_reg_array.value[0])) | (int(dut.gen_pg[3].g_reg_array.value[4]))
                elif ( i == 1 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[3].p_reg_array.value[5]) & int(dut.gen_pg[1].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[3].p_reg_array.value[5]) & int(dut.gen_pg[1].g_reg_array.value[0])) | (int(dut.gen_pg[3].g_reg_array.value[5]))
                elif ( i == 2 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[3].p_reg_array.value[6]) & int(dut.gen_pg[2].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[3].p_reg_array.value[6]) & int(dut.gen_pg[2].g_reg_array.value[0])) | (int(dut.gen_pg[3].g_reg_array.value[6]))
                elif ( i == 3 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[3].p_reg_array.value[7]) & int(dut.gen_pg[2].p_reg_array.value[1]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[3].p_reg_array.value[7]) & int(dut.gen_pg[2].g_reg_array.value[1])) | (int(dut.gen_pg[3].g_reg_array.value[7]))

                elif ( i >= 4 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[3].p_reg_array.value[i+4]) & int(dut.gen_pg[3].p_reg_array.value[i-4]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[3].p_reg_array.value[i+4]) & int(dut.gen_pg[3].g_reg_array.value[i-4])) | (int(dut.gen_pg[3].g_reg_array.value[i+4]))
                if ( i > 0 ):
                    p_reg_array_val_calc = p_reg_array_val_calc << 1
                    g_reg_array_val_calc = g_reg_array_val_calc << 1
                i -= 1
            #print(f"Expected gen_pg[4].p_reg_array value: {hex(p_reg_array_val_calc)}")
            #print(f"Actual gen_pg[4].p_reg_array value:   {hex(int(dut.gen_pg[4].p_reg_array.value))}")
            #print(f"Expected gen_pg[4].g_reg_array value: {hex(g_reg_array_val_calc)}")
            #print(f"Actual gen_pg[4].g_reg_array value:   {hex(int(dut.gen_pg[4].g_reg_array.value))}")

            p_reg_array_val_calc = 0
            g_reg_array_val_calc = 0
            i = 47
            while ( i >= 0 ):
                if ( i == 0 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[8]) & int(dut.gen_pg[0].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[8]) & int(dut.gen_pg[0].g_reg_array.value[0])) | (int(dut.gen_pg[4].g_reg_array.value[8]))
                elif ( i == 1 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[9]) & int(dut.gen_pg[1].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[9]) & int(dut.gen_pg[1].g_reg_array.value[0])) | (int(dut.gen_pg[4].g_reg_array.value[9]))
                elif ( i == 2 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[10]) & int(dut.gen_pg[2].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[10]) & int(dut.gen_pg[2].g_reg_array.value[0])) | (int(dut.gen_pg[4].g_reg_array.value[10]))
                elif ( i == 3 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[11]) & int(dut.gen_pg[2].p_reg_array.value[1]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[11]) & int(dut.gen_pg[2].g_reg_array.value[1])) | (int(dut.gen_pg[4].g_reg_array.value[11]))
                elif ( i == 4 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[12]) & int(dut.gen_pg[3].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[12]) & int(dut.gen_pg[3].g_reg_array.value[0])) | (int(dut.gen_pg[4].g_reg_array.value[12]))
                elif ( i == 5 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[13]) & int(dut.gen_pg[3].p_reg_array.value[1]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[13]) & int(dut.gen_pg[3].g_reg_array.value[1])) | (int(dut.gen_pg[4].g_reg_array.value[13]))
                elif ( i == 6 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[14]) & int(dut.gen_pg[3].p_reg_array.value[2]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[14]) & int(dut.gen_pg[3].g_reg_array.value[2])) | (int(dut.gen_pg[4].g_reg_array.value[14]))
                elif ( i == 7 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[15]) & int(dut.gen_pg[3].p_reg_array.value[3]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[15]) & int(dut.gen_pg[3].g_reg_array.value[3])) | (int(dut.gen_pg[4].g_reg_array.value[15]))
                elif ( i >= 8 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[i+8]) & int(dut.gen_pg[4].p_reg_array.value[i-8]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[4].p_reg_array.value[i+8]) & int(dut.gen_pg[4].g_reg_array.value[i-8])) | (int(dut.gen_pg[4].g_reg_array.value[i+8]))
                if ( i > 0 ):
                    p_reg_array_val_calc = p_reg_array_val_calc << 1
                    g_reg_array_val_calc = g_reg_array_val_calc << 1
                i -= 1
            #print(f"Expected gen_pg[5].p_reg_array value: {hex(p_reg_array_val_calc)}")
            #print(f"Actual gen_pg[5].p_reg_array value:   {hex(int(dut.gen_pg[5].p_reg_array.value))}")
            #print(f"Expected gen_pg[5].g_reg_array value: {hex(g_reg_array_val_calc)}")
            #print(f"Actual gen_pg[5].g_reg_array value:   {hex(int(dut.gen_pg[5].g_reg_array.value))}")
            
            p_reg_array_val_calc = 0
            g_reg_array_val_calc = 0
            i = 31
            while ( i >= 0 ):
                if ( i == 0 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[16]) & int(dut.gen_pg[0].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[16]) & int(dut.gen_pg[0].g_reg_array.value[0])) | (int(dut.gen_pg[5].g_reg_array.value[16]))
                elif ( i == 1 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[17]) & int(dut.gen_pg[1].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[17]) & int(dut.gen_pg[1].g_reg_array.value[0])) | (int(dut.gen_pg[5].g_reg_array.value[17]))
                elif ( i == 2 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[18]) & int(dut.gen_pg[2].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[18]) & int(dut.gen_pg[2].g_reg_array.value[0])) | (int(dut.gen_pg[5].g_reg_array.value[18]))
                elif ( i == 3 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[19]) & int(dut.gen_pg[2].p_reg_array.value[1]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[19]) & int(dut.gen_pg[2].g_reg_array.value[1])) | (int(dut.gen_pg[5].g_reg_array.value[19]))
                elif ( i == 4 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[20]) & int(dut.gen_pg[3].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[20]) & int(dut.gen_pg[3].g_reg_array.value[0])) | (int(dut.gen_pg[5].g_reg_array.value[20]))
                elif ( i == 5 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[21]) & int(dut.gen_pg[3].p_reg_array.value[1]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[21]) & int(dut.gen_pg[3].g_reg_array.value[1])) | (int(dut.gen_pg[5].g_reg_array.value[21]))
                elif ( i == 6 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[22]) & int(dut.gen_pg[3].p_reg_array.value[2]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[22]) & int(dut.gen_pg[3].g_reg_array.value[2])) | (int(dut.gen_pg[5].g_reg_array.value[22]))
                elif ( i == 7 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[23]) & int(dut.gen_pg[3].p_reg_array.value[3]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[23]) & int(dut.gen_pg[3].g_reg_array.value[3])) | (int(dut.gen_pg[5].g_reg_array.value[23]))
                elif ( i == 8 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[24]) & int(dut.gen_pg[4].p_reg_array.value[0]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[24]) & int(dut.gen_pg[4].g_reg_array.value[0])) | (int(dut.gen_pg[5].g_reg_array.value[24]))
                elif ( i == 9 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[25]) & int(dut.gen_pg[4].p_reg_array.value[1]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[25]) & int(dut.gen_pg[4].g_reg_array.value[1])) | (int(dut.gen_pg[5].g_reg_array.value[25]))
                elif ( i == 10 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[26]) & int(dut.gen_pg[4].p_reg_array.value[2]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[26]) & int(dut.gen_pg[4].g_reg_array.value[2])) | (int(dut.gen_pg[5].g_reg_array.value[26]))
                elif ( i == 11 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[27]) & int(dut.gen_pg[4].p_reg_array.value[3]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[27]) & int(dut.gen_pg[4].g_reg_array.value[3])) | (int(dut.gen_pg[5].g_reg_array.value[27]))
                elif ( i == 12 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[28]) & int(dut.gen_pg[4].p_reg_array.value[4]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[28]) & int(dut.gen_pg[4].g_reg_array.value[4])) | (int(dut.gen_pg[5].g_reg_array.value[28]))
                elif ( i == 13 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[29]) & int(dut.gen_pg[4].p_reg_array.value[5]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[29]) & int(dut.gen_pg[4].g_reg_array.value[5])) | (int(dut.gen_pg[5].g_reg_array.value[29]))
                elif ( i == 14 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[30]) & int(dut.gen_pg[4].p_reg_array.value[6]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[30]) & int(dut.gen_pg[4].g_reg_array.value[6])) | (int(dut.gen_pg[5].g_reg_array.value[30]))
                elif ( i == 15 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[31]) & int(dut.gen_pg[4].p_reg_array.value[7]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[31]) & int(dut.gen_pg[4].g_reg_array.value[7])) | (int(dut.gen_pg[5].g_reg_array.value[31]))
                elif ( i >= 16 ):
                    p_reg_array_val_calc = p_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[i+16]) & int(dut.gen_pg[5].p_reg_array.value[i-16]))
                    g_reg_array_val_calc = g_reg_array_val_calc | (int(dut.gen_pg[5].p_reg_array.value[i+16]) & int(dut.gen_pg[5].g_reg_array.value[i-16])) | (int(dut.gen_pg[5].g_reg_array.value[i+16]))
                if ( i > 0 ):
                    p_reg_array_val_calc = p_reg_array_val_calc << 1
                    g_reg_array_val_calc = g_reg_array_val_calc << 1
                i -= 1
            #print(f"Expected gen_pg[6].p_reg_array value: {hex(p_reg_array_val_calc)}")
            #print(f"Actual gen_pg[6].p_reg_array value:   {hex(int(dut.gen_pg[6].p_reg_array.value))}")
            #print(f"Expected gen_pg[6].g_reg_array value: {hex(g_reg_array_val_calc)}")
            #print(f"Actual gen_pg[6].g_reg_array value:   {hex(int(dut.gen_pg[6].g_reg_array.value))}")
            time_pass += 2
    else:
        await Timer(18, units="ns")    
    try:
        assert dut.out.value.integer == (a + b) & 0xffffffffffffffff #only 64 bits
    except AssertionError:
        print(f"Expected value: {hex((a + b) & 0xffffffffffffffff)}")
        print(f"Actual value:   {hex(dut.out.value.integer)}")
        print(f"a value: {a}")
        print(f"b value: {b}")

async def generate_clock(dut):
    """Generate clock pulses."""

    for cycle in range(30):
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")

@cocotb.test()
async def all_zeroes(dut):
    a = 0
    b = 0
    debug = False
    await cocotb.start(generate_clock(dut))
    await run_inputs(dut, a, b, debug)

@cocotb.test()
async def three(dut):
    a = 1
    b = 2
    debug = False
    await cocotb.start(generate_clock(dut))
    await run_inputs(dut, a, b, debug)

@cocotb.test()
async def twenty(dut):
    a = 15
    b = 5
    debug = False
    await cocotb.start(generate_clock(dut))
    await run_inputs(dut, a, b, debug)


@cocotb.test()
async def max(dut):
    a = 2**64-1
    b = 2**64-1
    debug = False
    await cocotb.start(generate_clock(dut))
    await run_inputs(dut, a, b, debug)

@cocotb.test()
async def rand(dut):
    a = 219562712927383529
    b = 1051223794508201066
    debug = False
    await cocotb.start(generate_clock(dut))
    await run_inputs(dut, a, b, debug)

@cocotb.test()
async def rand2(dut):
    a = 9
    b = 12
    debug = False
    await cocotb.start(generate_clock(dut))
    await run_inputs(dut, a, b, debug)

@cocotb.test()
async def random_nums(dut):
    test_num = 0
    debug = False
    for i in range(100000):
        a = randint(0, 2**64-1)
        b = randint(0, 2**64-1)
        #print (test_num)
        await cocotb.start(generate_clock(dut))
        await run_inputs(dut, a, b, debug)
        test_num += 1
