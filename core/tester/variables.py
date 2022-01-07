# -*- coding: utf-8 -*-

UID_PERFORMANCE_TEST_SKIP = True
UID_PERFORMANCE_ITERATION = 10000
# [Redis] Localhost 10000 iteration average is 0.0006s (WIN, x5 faster)
# [PgSQL] Localhost 10000 iteration average is 0.0031s

GRPC_PACKET_PERFORMANCE_TEST_SKIP = True
GRPC_PACKET_PERFORMANCE_ITERATION = 10000
GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE = "GRPC Packet performance testing is off"
# Pickle               grpc-pipe echo-data 10000 iteration 25.1275s (4,671 byte/packet)
# Orjson               grpc-pipe echo-data 10000 iteration 25.5181s (5,902 byte/packet)
# Orjson+zlib(level=1) grpc-pipe echo-data 10000 iteration 26.8770s (1,790 byte/packet)
# Orjson+zlib(level=9) grpc-pipe echo-data 10000 iteration 26.9768s (1,621 byte/packet)
# Orjson+gzip(level=1) grpc-pipe echo-data 10000 iteration 28.9337s (1,802 byte/packet)
# Orjson+gzip(level=9) grpc-pipe echo-data 10000 iteration 28.4226s (1,633 byte/packet)
# Orjson+bz2(level=1)  grpc-pipe echo-data 10000 iteration 34.7503s (1,820 byte/packet)
# Orjson+bz2(level=9)  grpc-pipe echo-data 10000 iteration 35.5534s (1,820 byte/packet)
# Orjson+lzma          grpc-pipe echo-data 10000 iteration 58.4753s (1,608 byte/packet)
