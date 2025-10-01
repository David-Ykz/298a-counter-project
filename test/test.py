# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start counter test")

    # Clock setup
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    dut._log.info("Reset released")

    # --- Load value 10 ---
    dut.ui_in.value = 10
    dut.uio_in.value = 0b01   # bit0=load=1, bit1=up_down=0 (don’t care)
    await ClockCycles(dut.clk, 1)
    dut.uio_in.value = 0b00   # clear load
    await ClockCycles(dut.clk, 1)

    assert int(dut.uo_out.value) == 10, f"Expected 10, got {int(dut.uo_out.value)}"
    dut._log.info(f"Loaded value OK: {int(dut.uo_out.value)}")

    # --- Count up for 5 cycles ---
    dut.uio_in.value = 0b10   # bit1=up_down=1
    await ClockCycles(dut.clk, 5)
    expected = 10 + 5
    assert int(dut.uo_out.value) == expected, f"Expected {expected}, got {int(dut.uo_out.value)}"
    dut._log.info(f"Count up OK: {int(dut.uo_out.value)}")

    # --- Count down for 3 cycles ---
    dut.uio_in.value = 0b00   # bit1=up_down=0
    await ClockCycles(dut.clk, 3)
    expected = expected - 3
    assert int(dut.uo_out.value) == expected, f"Expected {expected}, got {int(dut.uo_out.value)}"
    dut._log.info(f"Count down OK: {int(dut.uo_out.value)}")

    # --- Test tri-state (disable outputs) ---
    dut.ena.value = 0
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.is_resolvable == False, "Expected high-Z on outputs when disabled"
    dut._log.info("Tri-state output OK")
