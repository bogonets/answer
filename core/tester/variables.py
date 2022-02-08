# -*- coding: utf-8 -*-

UID_PERFORMANCE_TEST_SKIP = True
UID_PERFORMANCE_ITERATION = 10000
# [Redis] Localhost 10000 iteration average is 0.0006s (WIN, x5 faster)
# [PgSQL] Localhost 10000 iteration average is 0.0031s

GRPC_PACKET_PERFORMANCE_TEST_SKIP = True
GRPC_PACKET_PERFORMANCE_ITERATION = 10000
GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE = "GRPC Packet performance testing is off"
# Pickle                grpc-pipe echo-data 10000 iteration 25.9940s (4,457 byte/packet)
# Msgpack               grpc-pipe echo-data 10000 iteration 25.7207s (4,742 byte/packet)
# Orjson                grpc-pipe echo-data 10000 iteration 25.6654s (5,902 byte/packet)

# Msgpack+zlib(level=1) grpc-pipe echo-data 10000 iteration 27.1403s (1,821 byte/packet)
# Msgpack+zlib(level=9) grpc-pipe echo-data 10000 iteration 27.1509s (1,745 byte/packet)
# Msgpack+gzip(level=1) grpc-pipe echo-data 10000 iteration 28.2962s (1,833 byte/packet)
# Msgpack+gzip(level=9) grpc-pipe echo-data 10000 iteration 28.6674s (1,757 byte/packet)
# Msgpack+bz2(level=1)  grpc-pipe echo-data 10000 iteration 35.2526s (2,084 byte/packet)
# Msgpack+bz2(level=9)  grpc-pipe echo-data 10000 iteration 34.9677s (2,084 byte/packet)
# Msgpack+lzma          grpc-pipe echo-data 10000 iteration 56.4002s (1,732 byte/packet)

# Orjson+zlib(level=1)  grpc-pipe echo-data 10000 iteration 26.7126s (1,790 byte/packet)
# Orjson+zlib(level=9)  grpc-pipe echo-data 10000 iteration 27.0982s (1,621 byte/packet)
# Orjson+gzip(level=1)  grpc-pipe echo-data 10000 iteration 28.0648s (1,802 byte/packet)
# Orjson+gzip(level=9)  grpc-pipe echo-data 10000 iteration 28.0872s (1,633 byte/packet)
# Orjson+bz2(level=1)   grpc-pipe echo-data 10000 iteration 35.3671s (1,820 byte/packet)
# Orjson+bz2(level=9)   grpc-pipe echo-data 10000 iteration 35.3782s (1,820 byte/packet)
# Orjson+lzma           grpc-pipe echo-data 10000 iteration 57.2244s (1,608 byte/packet)
