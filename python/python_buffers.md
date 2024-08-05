# Why Are Log Outputs Disordered? Python Buffering Explained

Ever had your print statements or logs appear in a completely unexpected order?
If you've ever worked with a separate logging service like AWS CloudWatch, you
probably have! It can feel like you've fallen down a rabbit hole, with
everything seeming random and chaotic. But fear not, because we're diving into
the delightful world of Python buffering and unravel this mystery.

## Introduction
Python, like many other programming languages, uses
buffers to enhance performance during input/output operations. A buffer is a
temporary storage area where data is held before being sent to its final
destination such as a console, a log file, or external service. Understanding
buffering can help you manage log outputs more effectively and aviod confusion.

## Understanding Buffering Modes

Python uses three main types of buffering, depending on the context and the
nature of output.

1. No Bufferring: Data is written immediately. This mode is typically used
   interactive environment where immediate feedback is crucial.
2. Line Buffering: Data is written whenever a character is encountered. This is
   the mode for `stdout` when connected to a terminal .i.e. when logs are
   getting printed to the terminal.
3. Full Buffering: Data is stored until the buffer is full before being written
   out. This is commonly used for files to optimize write operations (When
   writing to a file or when logs are pointed to a file or external service).

# Buffering in Action: The Curious Case of Jumbled Logs

How do you think the following script is going to print its logs?

```python
"""
test.py
Disclaimer: While I wouldn’t typically recommend mixing print statements with logs from the logging module in the same project, experimenting with both can provide valuable insights into how buffering and logging work.
"""
import sys
import logging

logging.basicConfig(level=logging.INFO)

logging.info("This is the start")
for i in range(3):
    print(f"[STDOUT]: {i}")
    print(f"[ERR]: {i}", file=sys.stderr)
logging.info("This is the end")
```

When you run it on the terminal, with `python test.py`. You get the expected output.
```log
$ python test.py
INFO:root:This is the start
[STDOUT] == 0
[STDERR] >> 0
[STDOUT] == 1
[STDERR] >> 1
[STDOUT] == 2
[STDERR] >> 2
INFO:root:This is the end
```

When you run it on the terminal with `python test.py &> output.txt` or `python test.py &> >(cat)`.
Note: With &> We are specifying that both error `2` and standard output `1` to be written to output.txt.
```log
$ python test.py &> >(cat)
INFO:root:This is the start
[ERR]: 0
[ERR]: 1
[ERR]: 2
ERROR:root:This is the end
[STDOUT]: 0
[STDOUT]: 1
[STDOUT]: 2
```

>> We have chosen to use process substitution with `python test.py &> (cat)` instead of piping with `python test.py | cat` because pipes only send stdout to the next command, missing stderr. Process substitution creates a file-like object for the command output, allowing both stdout and stderr to be captured and used together, like a file.  This way, cat can handle both outputs seamlessly, ensuring no output is lost or separated. If you try using a pipe, stderr output will be printed first, without being piped through cat, and then the rest will get `cat`ed out which does not accurately reflect what python is doing with the intended log order.

# What's Happening?

We have three differnt types of logs in the code:
1. **Standard output** are buffered in python when the logs are redirected to a
   file or through a log driver. That is why they are getting printed at the
   end when the buffer is cleared at the end of the script.
2. However, standard errors are unbuffered by default in all cases. So they are
   printed  as soon as the code reaches that part.
3. So what about the logs printed using the logging module? They all also seem
   to be printed immediately. That is true to an extent. They are line-buffered
   & that's why the logs seem unordered.

Here's a more in depth explanation:
1. **Non-Interactive Mode/Script Execution:** 
   If Python isn't being run interactively, and logs aren't redirected to any
   file or pipe, standard input and output are still line-buffered, while
   standard error remains unbuffered.
   - **stdin:** Line Buffered when connected to a terminal
   - **stdout:** Line Buffered when connected to a terminal
   - **stderr:** Unbuffered

2. **Redirection to Files/Pipes:** 
   When outputs are redirected (e.g., python script.py | cat or python script.py > output.txt), buffering behavior changes:
   - **stdin:** Fully Buffered
   - **stdout:** Fully Buffered
   - **stderr:** Unbuffered

3. **Logging module**
The logging module in Python operates differently from standard output because
of how it handles of streams and buffering. It employs its own streams and can
be configured with various handlers, each potentially having distinct buffering
behaviors. By default, the logging module uses line buffering, which means that
log messages are flushed to the destination as soon as a newline character is
encountered. This approach ensures that log entries are promptly displayed,
making them appear more consistent and immediate compared to standard output
(When logs are redirected).

## Why do we even need buffers?

Because buffers are like a magical cauldron that cooks up performance benefits:

1. **Performance:** Directly writing data to a physical device can be slow. Buffers help by accumulating data and writing it in larger chunks, significantly speeding things up.
2. **Smoothing:** Buffers help to smooth out data flow, preventing sudden bursts of output that could overwhelm your system.

# Disabling Buffering with PYTHONUNBUFFERED

Sometimes, you just want things printed right away, without any buffering delay. Enter the `PYTHONUNBUFFERED` environment variable! By setting `PYTHONUNBUFFERED=1`, you disable buffering, ensuring everything is printed instantly. This can be super useful for real-time logging or debugging.
You may have seen the follwing line in dockerfiles of python projects.

```bash
ENV PYTHONUNBUFFERED=1
```

# The flush() Method

Want to manually empty the buffer and get that data out immediately? Use the `flush()` method!

```python
import sys

print("Hello, world!")
sys.stdout.flush()  # Forces the buffer to be emptied
```

# Customizing Buffer Behavior

You can customize how your standard output and error streams behave in terms of buffering. Here's how you can disable line buffering:

```python
import io
import sys
import logging

logging.basicConfig(level=logging.INFO)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer.raw, line_buffering=False) # Setting line_buffering to True will give you line bufferred print statements
sys.stderr = io.TextIOWrapper(sys.stderr.buffer.raw, line_buffering=False)

logging.info("This is the start")
for i in range(3):
    print(f"[STDOUT]: {i}")
    print(f"[ERR]: {i}", file=sys.stderr)
logging.info("This is the end")
```

Output:
```log
$ python test.py 
INFO:root:This is the start
INFO:root:This is the end
[ERR]: 0
[ERR]: 1
[ERR]: 2
[STDOUT]: 0
[STDOUT]: 1
[STDOUT]: 2
```

Now, no matter the environment, your output will be fully buffered. even when we have set the PYTHONUNBUFFERED env variable to 1.

# Going Even Further: Custom Output Wrappers

Want to add a custom prefix to your `stdout` and `stderr` messages? You can
create a custom output wrapper. The only requirements for an class
to be compatible with sys.stdout & sys.stderr is to have the following two things:
1. Must have an `write` instance method
   * that takes message as an argument
   * that adds the message to an internal stream
2. Must have a `flush` instance method
   * that flushes the stream and prints to the console or logs to a file

```python
import io
import sys

g_original_stdout = sys.stdout

class CustomOutputWrapper():
    def __init__(self, prefix: str, name: str):
        self.prefix = prefix
        self.name = name
        self.stream = io.StringIO()

    def write(self, message):
        # The logic here ensures that the prefix is only added at the start of a new line.
        # Python's internal print mechanism writes to the buffer multiple times before flushing.
        # These writes often include whitespace or partial chunks of the same line.
        # This behavior can occur with both regular print statements and exception messages
        # (which are sent to sys.stderr and include tracebacks).
        # To avoid adding the prefix in the middle of a line or between chunks of the same line,
        # we only prepend it when we're at the start of a new line or after a previous newline.
        written_msg = self.stream.getvalue()
        if not written_msg or written_msg.endswith("\n"):
            self.stream.write(self.prefix)
        self.stream.write(message)

    def flush(self):
        final_msg = self.stream.getvalue()
        g_original_stdout.write(final_msg)
        if final_msg and not final_msg.endswith("\n"):
            g_original_stdout.write("\n")
        g_original_stdout.write(f"{self.name} stream is flushed\n")
        self.stream.truncate(0)

sys.stdout = CustomOutputWrapper("[STDOUT]: ", name="Standard output")
sys.stderr = CustomOutputWrapper("[ERR] >> ", name="Standard error")

for i in range(3):
    print(i)
    print(i, file=sys.stderr)
    if i == 2:
        # raising an exception to see how error messages gets printed
        raise Exception("Raised")
```

Output:
```log
$ python test.py 
[ERR] >> 0
[ERR] >> 1
[ERR] >> 2
Standard error stream is flushed
[STDOUT]: 0
[STDOUT]: 1
[STDOUT]: 2
Standard output stream is flushed
[ERR] >> Traceback (most recent call last):
[ERR] >>   File "C:\Users\mtnek\projects\personal\blogs\test.py", line 92, in <module>
    raise Exception("Raised")
[ERR] >> Exception: Raised
Standard error stream is flushed
Standard output stream is flushed
Standard error stream is flushed
```

While not generally recommended for production, playing with these customizations can be a fun way to explore Python's flexibility. Also, we can see that the logs related to the error messages are
pushed to the stderr stream instead of the stdout stream. Which makes total sense, but it's nice
to see it clearly using this example. Also, we can see from the logs when the streams was flused as well. Standard error stream was flushed before and after the exception was raised and before the
python script exited.

## Why stop here? Let's add enable line buffering as well in our custom output wrapper.
```python
...

class CustomOutputWrapper():
    def __init__(self, prefix: str, name: str, line_buffering: bool=False):
        self.prefix = prefix
        self.name = name
        self.stream = io.StringIO()
        self.line_buffering = line_buffering

    def write(self, message):
        ...
        written_msg = self.stream.getvalue()
        if not written_msg or written_msg.endswith("\n"):
            self.stream.write(self.prefix)
        self.stream.write(message)
        if self.line_buffering and ("\n" in message):
            self.flush()
    ...

sys.stdout = CustomOutputWrapper("[STDOUT]: ", name="Standard output", line_buffering=True)
sys.stderr = CustomOutputWrapper("[ERR] >> ", name="Standard error", line_buffering=True)

...
```

With this simple change, we have line buffering enabled as well. And now, we can see that the our stream is getting flushed whenever it encounters a newline in the logs below.

Output:
```
$ python custom_print_wrapper.py
[STDOUT]: 0
Standard output stream is flushed
[ERR] >> 0
Standard error stream is flushed
[STDOUT]: 1
Standard output stream is flushed
[ERR] >> 1
Standard error stream is flushed
[STDOUT]: 2
Standard output stream is flushed
[ERR] >> 2
Standard error stream is flushed
Standard error stream is flushed
Standard output stream is flushed
[ERR] >> Traceback (most recent call last):
Standard error stream is flushed
[ERR] >>   File "C:\Users\mtnek\projects\personal\blogs\test.py", line 136, in <module>
Standard error stream is flushed
[ERR] >>     raise Exception("Raised")
Standard error stream is flushed
[ERR] >> Exception: Raised
Standard error stream is flushed
Standard error stream is flushed
Standard output stream is flushed
Standard error stream is flushed
```

## Some points to be noted

While buffers are great, they can occasionally lead to tricky situations:

1. **Lost Data:** If a program crashes and doesn't exit properly before the buffer is flushed, any buffered data might be lost.
2. **Delayed Output:** Sometimes you need immediate feedback, and buffering can delay this.
3. **Debugging:** Buffers can obscure the order of events, making debugging harder. Use `flush()` or the `-u` flag for immediate output.
4. **Explore Alternatives:** For large datasets or performance-critical apps, look into writing directly to files or using specialized libraries.
5. **Be Platform-Aware:** Buffering behavior can vary between platforms, so test accordingly.
5. **File Buffers/Streams:** All the things we discussed on standard output & error also apply to files. However, file write is always fully buffered by default for the purposes of efficiency.

## Conclusion
I hope you found the blog informative and gained a deeper understanding of Python's buffering mechanisms and how they can impact the order and timing of your logs. To solidify your knowledge, experiment with different code examples and explore further customizations. The more you tinker with these concepts, the more intuitive they'll become, enhancing your ability to manage and optimize your Python applications. Happy Coding!

So, next time you see unexpected output order, don't fret! Just remember this journey through the whimsical world of Python buffering and all the magic it holds.

## References:
[Python documention on IO](https://docs.python.org/3/library/io.html)
