module pg_1plus (
    input logic pi_cur,
    input logic gi_cur,
    input logic pi_prev,
    input logic gi_prev,
    output logic pout,
    output logic gout
);

assign pout = pi_cur & pi_prev;
assign gout = gi_cur | (pi_cur & gi_prev);

endmodule