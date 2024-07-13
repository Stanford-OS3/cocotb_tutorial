/*
    This is a Kogge Stone Adder. This version was not designed for pipelining and only
    allows one calculation to begin every log2(N) cycles. 
*/
module ks_add #(
    parameter N = 64
)
(
    input  logic         clk,
    input  logic         rstn_,
    input  logic         en,
    input  logic [N-1:0] a,
    input  logic [N-1:0] b,
    output logic [N-1:0] out
);

    //add local params for readability
    localparam int stages = $clog2(N) + 1;
    localparam int log2_arr[0:63] = {0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5};

    genvar i;
    generate
        for (i = 0; i < stages; i++) begin : gen_pg
            logic [(N-(2**(i-1)))-1:0] g_reg_array;
            logic [(N-(2**(i-1)))-1:0] p_reg_array;
            logic [(N-(2**(i-1)))-1:0] p_out_array;
            logic [(N-(2**(i-1)))-1:0] g_out_array;
        end
    endgenerate
    
    genvar j;
    generate
        for (j = 0; j < stages; j++) begin : reg_assign
            always_ff @( posedge clk ) begin
                if ( !rstn_ ) begin
                    gen_pg[j].g_reg_array <= 0;
                    gen_pg[j].p_reg_array <= 0;
                end
                else if ( en ) begin
                    gen_pg[j].g_reg_array <= gen_pg[j].g_out_array;
                    gen_pg[j].p_reg_array <= gen_pg[j].p_out_array;
                end
                else begin
                    gen_pg[j].g_reg_array <= gen_pg[j].g_reg_array;
                    gen_pg[j].p_reg_array <= gen_pg[j].p_reg_array;
                end
            end
        end
    endgenerate

    genvar step;
    generate 
        for (i = 0; i < N; i++) begin
            pg_0 step0(a[i], b[i], gen_pg[0].p_out_array[i], gen_pg[0].g_out_array[i]);
        end

        for (step = 1; step <= stages; step++) begin
            for (i = 0; i < N-2**(step-1); i++) begin 
                if (step == 1) begin
                    pg_1plus stepn(gen_pg[0].p_reg_array[i+1],  
                                 gen_pg[0].g_reg_array[i+1], 
                                 gen_pg[0].p_reg_array[i], 
                                 gen_pg[0].g_reg_array[i], 
                                 gen_pg[step].p_out_array[i], 
                                 gen_pg[step].g_out_array[i]);
                end
                if (step > 1) begin
                    //step 2 onwards
                    if (i==0) begin
                        pg_1plus stepn(gen_pg[step-1].p_reg_array[i+2**(step-2)],  
                                 gen_pg[step-1].g_reg_array[i+2**(step-2)], 
                                 gen_pg[0].p_reg_array[0], 
                                 gen_pg[0].g_reg_array[0], 
                                 gen_pg[step].p_out_array[0], 
                                 gen_pg[step].g_out_array[0]);
                    end

                    else if (i < 2**(step-2)) begin 
                        pg_1plus stepn(gen_pg[step-1].p_reg_array[i+2**(step-2)],                                         
                                 gen_pg[step-1].g_reg_array[i+2**(step-2)],                                            
                                 gen_pg[log2_arr[i]+1].p_reg_array[i-2**(log2_arr[i])], 
                                 gen_pg[log2_arr[i]+1].g_reg_array[i-2**(log2_arr[i])],
                                 gen_pg[step].p_out_array[i], 
                                 gen_pg[step].g_out_array[i]);
                    end

                    else begin //at later stages
                        pg_1plus stepn(gen_pg[step-1].p_reg_array[i+2**(step-2)],  
                                 gen_pg[step-1].g_reg_array[i+2**(step-2)], 
                                 gen_pg[step-1].p_reg_array[i-2**(step-2)], 
                                 gen_pg[step-1].g_reg_array[i-2**(step-2)], 
                                 gen_pg[step].p_out_array[i], 
                                 gen_pg[step].g_out_array[i]);
                    end
                end
            end
        end
    endgenerate

    generate
        for (i = 0; i < N; i++) begin
            if ( i==0 ) begin
                assign out[0] = gen_pg[0].p_reg_array[0];
            end
            else if ( i==1 ) begin
                assign out[1] = gen_pg[0].p_reg_array[1] ^ gen_pg[0].g_reg_array[0];
            end
            else if (i <= N/2) begin //1 through (N/2)
                assign out[i] = (gen_pg[0].p_reg_array[i]) ^ (gen_pg[log2_arr[i-1]+1].g_reg_array[(i-1)-2**log2_arr[i-1]]); 
                        //    2                    2                        0                              1                                0
                        //    3                    2                        1                              2                                0
                        //    4                    3                        0                              2                                1
                        //    5                    3                        1                              3                                0
                        //    6                    3                        2                              3                                1

                        //    32                   6                        0                              5                                15
            end
            else begin
                assign out[i] = gen_pg[0].p_reg_array[i] ^ gen_pg[stages-1].g_reg_array[(i-1)-(N/2)]; 
                        //    33                  6                  1                    6                  0
                        //    34                  6                  2                    6                  1
                           
                        //    63                  6                 31                    6                 30
            end
        end
    endgenerate

endmodule