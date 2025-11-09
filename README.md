# Hardware Trojan Detection via Side-Channel Analysis

## Overview
This project demonstrates hardware security analysis by detecting hidden malicious logic (Trojans) in digital circuits using switching activity comparison.

## Project Structure
- `alu_clean.v` - Clean 4-bit ALU implementation
- `alu_trojan.v` - Trojan-infected 4-bit ALU
- `tb_alu_clean.v` - Testbench for clean ALU
- `tb_alu_trojan.v` - Testbench for Trojan ALU
- `vcd_analysis.py` - Python script for VCD parsing and analysis
- `trojan_detection_analysis.png` - Visualization results

## How to Run

### Simulation


iverilog -o clean.out alu_clean.v tb_alu_clean.v
vvp clean.out


iverilog -o trojan.out alu_trojan.v tb_alu_trojan.v
vvp trojan.out


### Analysis


## Trojan Design
The Trojan activates only when both inputs A and B equal 1111 (binary), flipping the LSB of the result. This rare trigger condition (0.1% of test cases) makes it extremely stealthy and undetectable through basic side-channel analysis.

## Results
The analysis shows 0% deviation between clean and Trojan designs, demonstrating how sophisticated hardware Trojans can evade detection by activating only under rare conditions.

## Tools Used
- Icarus Verilog (simulation)
- Python (NumPy, Matplotlib)



