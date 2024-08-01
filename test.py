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


# import io
# import sys
# import logging

# logging.basicConfig(level=logging.INFO)
# # sys.stdout = io.TextIOWrapper(sys.stdout.buffer.raw, line_buffering=False)
# # sys.stderr = io.TextIOWrapper(sys.stderr.buffer.raw, line_buffering=True)

# logging.info("This is the start")
# for i in range(3):
#     print(f"[STDOUT] == {i}")
#     # print(f"[STDERR] >> {i}", file=sys.stderr)
#     sys.stderr.write(f"[STDERR] >> {i}\n")
# logging.info("This is the end")


import io
import sys

g_original_stdout = sys.stdout

class CustomOutputWrapper():
    def __init__(self, prefix):
        self.prefix = prefix
        self.stream = io.StringIO()

    def write(self, message):
        if not message.strip():
            self.stream.write(message)
            return
        # All this extra stuff is to make sure we only add the prefix when
        # there's a newline The inner python code, both the prints during
        # execptions and normal print statemments they add extra stuff to the
        # stream before printing. For example, a normal print statement will
        # add a newline after the print. Exception msgs gets pushed to sys.stderr
        # and it prints the tracebacks and the error msgs in the exception.
        # Hence to ensure the code executes as expected, we are only adding the
        # prefix, during the first write or any newline after that.
        written_msg = self.stream.getvalue()
        self.stream.truncate(0)
        if not written_msg or written_msg.endswith("\n"):
            self.stream.write(written_msg + self.prefix + message)
        else:
            self.stream.write(written_msg + message)

    def flush(self):
        final_msg = self.stream.getvalue()
        g_original_stdout.write(final_msg)
        self.stream.truncate(0)

sys.stdout = CustomOutputWrapper("[STDOUT]: ")
sys.stderr = CustomOutputWrapper("[ERR] >> ")

for i in range(3):
    print(i)
    print(i, file=sys.stderr)
    if i == 2:
        raise Exception("Raised")
