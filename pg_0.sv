module pg_0 (
    input logic a,
    input logic b,
    output logic p,
    output logic g
);

assign p = a ^ b;
assign g = a & b;

endmodule