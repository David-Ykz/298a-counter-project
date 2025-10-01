module counter_8bit (
    input  wire        clk,       // Clock input
    input  wire        rst_n,     // Active-low asynchronous reset
    input  wire        load,      // Synchronous load enable
    input  wire        en,        // Output enable for tri-state
    input  wire        up_down,   // 1 for count up
    input  wire [7:0]  data_in,   // Load value
    output wire [7:0]  q          // Tri-state output
);

    reg [7:0] count_reg;

    // Asynchronous reset and synchronous load/count
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count_reg <= 8'b0;                 // async reset to 0
        end else if (load) begin
            count_reg <= data_in;              // synchronous load
        end else begin
            if (up_down)
                count_reg <= count_reg + 1;    // count up
            else
                count_reg <= count_reg - 1;    // count down
        end
    end

    // Tri-state output
    assign q = en ? count_reg : 8'bz;

endmodule