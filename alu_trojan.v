// alu_trojan.v
// 4-bit Arithmetic Logic Unit - Trojan Version
// Contains hidden malicious logic that activates under specific conditions

module alu_trojan(
    input [3:0] A,        // 4-bit input A
    input [3:0] B,        // 4-bit input B
    input [1:0] op,       // 2-bit operation selector
    output reg [3:0] result  // 4-bit result
);

    // Normal ALU operations
    always @(*) begin
        case(op)
            2'b00: result = A + B;      // Addition
            2'b01: result = A - B;      // Subtraction
            2'b10: result = A & B;      // Bitwise AND
            2'b11: result = A | B;      // Bitwise OR
            default: result = 4'b0000;
        endcase
        
        // TROJAN LOGIC: Activate when A=1111 and B=1111
        // This creates a rare condition that flips the LSB
        if (A == 4'b1111 && B == 4'b1111) begin
            result = result ^ 4'b0001;  // XOR with 0001 (flip LSB)
        end
    end

endmodule
