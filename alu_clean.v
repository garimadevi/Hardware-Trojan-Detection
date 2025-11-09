// alu_clean.v
// 4-bit Arithmetic Logic Unit - Clean Version
// Operations: ADD, SUB, AND, OR

module alu_clean(
    input [3:0] A,        // 4-bit input A
    input [3:0] B,        // 4-bit input B
    input [1:0] op,       // 2-bit operation selector
    output reg [3:0] result  // 4-bit result
);

    // Operation encoding:
    // 00 = ADD
    // 01 = SUB
    // 10 = AND
    // 11 = OR
    
    always @(*) begin
        case(op)
            2'b00: result = A + B;      // Addition
            2'b01: result = A - B;      // Subtraction
            2'b10: result = A & B;      // Bitwise AND
            2'b11: result = A | B;      // Bitwise OR
            default: result = 4'b0000;  // Default case
        endcase
    end

endmodule
