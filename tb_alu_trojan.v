// tb_alu_trojan.v
// Testbench for Trojan ALU - similar to clean but operates on trojan ALU

`timescale 1ns/1ps

module tb_alu_trojan;

    // Inputs
    reg [3:0] A;
    reg [3:0] B;
    reg [1:0] op;
    
    // Outputs
    wire [3:0] result;
    
    // Instantiate the Trojan ALU
    alu_trojan uut (
        .A(A),
        .B(B),
        .op(op),
        .result(result)
    );
    
    integer i, j, k;
    
    initial begin
        $dumpfile("alu_trojan.vcd");
        $dumpvars;

        
        for (k = 0; k < 4; k = k + 1) begin
            op = k[1:0];
            for (i = 0; i < 16; i = i + 1) begin
                A = i[3:0];
                for (j = 0; j < 16; j = j + 1) begin
                    B = j[3:0];
                    #10;
                end
            end
        end
        
        $finish;
    end

endmodule
