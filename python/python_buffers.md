

# Introduction
Have you ever come accross a situation where your print statements or logs are
coming in the wrong order? If you have been working with a separate logging
service such as AWS Cloudwatch, it's highly like that you have. I encountered
the same situation and went into the rabbit hole of learning about python buffering.
Even though at first it felt like the print order was random, it was being printed
as it should be in the given situation.


# Example 1
```python
import sys
import logging

logging.basicConfig(level=logging.INFO)

logging.info("This is the start")
for i in range(3):
    print(f"[STDOUT]: {i}")
    print(f"[ERR]: {i}", file=sys.stderr)
logging.info("This is the end")
```

# What are the code smells you see in the above code?
1. I am using both logging and print statement.
   * Use logging as it has more options for {insert the benefits of logging
     module}. But at the very least, be consistent with what logging mechanism
     you use and just use either print statements or logging module throughout
     the project.

I am sure you expected the logs to be as follows:
```log
INFO:root:This is the start
[STDOUT] == 0
[STDERR] >> 0
[STDOUT] == 1
[STDERR] >> 1
[STDOUT] == 2
[STDERR] >> 2
INFO:root:This is the end
```

And yes in the console, it will be the case. But when you run it in a container
and point the logs to cloudwatch, the logs are a whole lot different.
```log
INFO:root:This is the start
[STDERR] >> 0
[STDERR] >> 1
[STDERR] >> 2
INFO:root:This is the end
[STDOUT] == 0
[STDOUT] == 1
[STDOUT] == 2
```
# What is happening?
Python, like many programming languages, employs buffers to enhance performance
and efficiency during input/output operations. A buffer is essentially a
temporary storage area where data is held before being written to its final
destination (like a file or the console). So, when we run any print statement or logs,
it is intially written to a buffer, and then when the buffer is full, it gets written to
the console or file. And the default settings for buffering also differs based
on which env it is run on. There are two modes:
1. INTERACTIVE MODE (e.g., in a terminal or REPL)
   When python is run interactively in a terminal, standard input and output
   streams are line-buffered. This means the output to the terminal is flushed
   whenever a newline chaaracter is encountered. The stand error system is
   unbuffered. (Gets printed immediately)

   * stdin => Line Buffered
   * stdout => Line Buffered
   * stderr => Unbuffered
2. NON INTERACTIVE MODE/Script Excecution
   When run in non interactive mode and if the logs aren't redirected to any
   file/pipes, standard output & standard input are line buffered. And standard
   error is again unbuffered.
   * stdin => Line Buffered when associated with a terminal (TTY)
   * stdout => Line Buffered when associated with a terminal (TTY)
   * stderr => Unbuffered
3. Redirection to Files/Pipes
   If you pipe the outputs to another cmd or redirect the outputs to a file or
   AWS Cloudwatch or any other logging system, io will follow the following rule.
   * stdin => Fully Buffered
   * stdout => Fully Buffered
   * stderr => Unbuffered
   Note:
   You can try the script with cmd: `python test.py | cat` or `python test.py > output.txt`
   to get the result easily.

## Why Buffers?

Performance: Writing data to a physical device is relatively slow. By
accumulating data in a buffer and writing it in larger chunks, Python can
significantly improve performance.

Smoothing: Buffering helps to smooth out the flow of data, preventing sudden
bursts of output that can overwhelm the system.

# PYTHONUNBUFFERED
If you didn't know,  

## Types of Buffers in Python
Python primarily uses three buffering strategies:

1. No Buffering: Data is written directly without any intermediate storage.
   This is typically used for interactive environments.
2. Line Buffering: Data is stored until a newline character is encountered, and
   then it's written to the output. This is the default behavior for stdout
   when connected to a terminal.
3. Full Buffering: Data is stored until the buffer is full, and then it's
   written to the output. This is commonly used for files.

## The flush() Method
To ensure that all data in the buffer is written to the output immediately, you
can use the flush() method.

```python
import sys

print("Hello, world!")
sys.stdout.flush()  # Forces the buffer to be emptied
Use code with caution.
```


## When Buffers Can Be Problematic
While buffering is generally beneficial, it can sometimes lead to unexpected
behavior:

1. Lost Data: If a program crashes before the buffer is flushed, the data in
   the buffer might be lost.
2. Delayed Output: In certain scenarios, you might want immediate output, but
   buffering can cause delays.

Practical Examples
1. Logging: When rotating log files, understanding buffer behavior is crucial
   to prevent data loss.
2. Debugging: Buffering can sometimes obscure the order of events, making
   debugging challenging. Using flush() or the -u flag can help.
3. Performance Optimization: For I/O-bound applications, fine-tuning buffer
   sizes can significantly impact performance.
4. Concurrent Programming: Buffering can introduce complexities in
   multi-threaded or multi-process environments.

Best Practices
1. Use flush() when immediate output is critical.
2. Consider the trade-off between performance and data integrity when adjusting
   buffer behavior.
3. For large datasets or performance-critical applications, explore alternative
   approaches like writing to files or using specialized libraries.
4. Be aware of platform-specific differences in buffering behavior.

Conclusion
Python's buffering mechanism is a powerful tool for optimizing performance. By
understanding its intricacies and applying best practices, you can write more
efficient and reliable Python code.

Useful Ideas:

1. Can I set buffersize for print?
2. Recreate situations with python code that will:
    * Fail to flush the buffer (print buffer & file buffer)
    * Mess up the log vs print ordering
3. Add example code when trying to log to a file?
4. Give an overview of what buffer is in general software engineering & list
   the ways it's used in all areas.
   * Networks
   * Prints
   * Writing to files, etc


References:
* Buffering in file: https://docs.python.org/3/library/functions.html#open