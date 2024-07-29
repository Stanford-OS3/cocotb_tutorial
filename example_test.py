import cocotb
from cocotb.triggers import Timer

@cocotb.test
async def test_1(dut):
    dut.a.setimmediatevalue(1)
    dut.b.setimmediatevalue(1)
    await Timer(2, units="ns")
    assert dut.p.value.integer == 1 ^ 1
    assert dut.g.value.integer == 1 & 1