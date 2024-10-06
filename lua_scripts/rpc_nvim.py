import pynvim

nvim = pynvim.attach("tcp", address="127.0.0.1", port=666)

buffer = nvim.current.buffer

buffer.append("This is going to be added on the last line")

buffer[:] = ["This is going to be added on the first line"] + buffer[:]

buffer[0] = "Replace the first line"

nvim.command("vpslit")
