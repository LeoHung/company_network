from gen_data.gen_c2p2c_network import gen, gen_b2b_network

input_filenames = ["files/%d0000000.json" %i for i in range(10)]
c2p2c_output_filename = "out/c2p2c.json"
index_output_filename = "out/index.json"
b2b_output_filename = "out/b2b.json"

# gen(
#     input_filenames=input_filenames,
#     c2p2c_output_filename=c2p2c_output_filename,
#     index_output_filename=index_output_filename
# )
gen_b2b_network(
    c2p2c_filename=c2p2c_output_filename,
    index_output_filename=index_output_filename,
    b2b_output_filename=b2b_output_filename
)
