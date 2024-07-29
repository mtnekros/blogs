# import os
# import io
# import sys
# # import logging

# # logging.basicConfig(level=logging.INFO)

# def unbuffered_logs():
#     ...

# # io.DEFAULT_BUFFER_SIZE = 1
# # buffer_size = 8192
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer.raw, line_buffering=True)
# sys.stderr = io.TextIOWrapper(sys.stderr.buffer.raw, line_buffering=True)

# print(io.DEFAULT_BUFFER_SIZE)
# # logging.info("This is the start")
# for i in range(1000):
#     sys.stderr.write(f"[ERR]: {i} This is the std err print statements okay?" * 3 + "\n") #, file=sys.stderr, flush=True)
#     # sys.stderr.flush()
#     sys.stdout.write(f"[OUT]: {i} STDOUT STDOUT STDOUT STDOUT STDOUT STDOUT STDOUT STDOUT STDOUT" * 3 + "\n") # , flush=True)
#     # sys.stdout.flush()
#     # if i == 100:
#     #     # logging.info("This is the before exception")
#     #     raise KeyboardInterrupt

# print(f"write_through: {sys.stdout.write_through}")
# print(f"line_buffering: {sys.stdout.line_buffering}")
# print(f"newline: {sys.stdout.newlines}")

# # logging.info("This is the end")


import io
import sys
import logging

logging.basicConfig(level=logging.INFO)
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer.raw, line_buffering=False)
# sys.stderr = io.TextIOWrapper(sys.stderr.buffer.raw, line_buffering=True)

logging.info("This is the start")
for i in range(3):
    print(f"[STDOUT] == {i}")
    # print(f"[STDERR] >> {i}", file=sys.stderr)
    sys.stderr.write(f"[STDERR] >> {i}\n")
logging.info("This is the end")