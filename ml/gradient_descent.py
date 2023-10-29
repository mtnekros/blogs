import math
import numpy as np
from numpy.typing import NDArray

def gradient_descent(x: NDArray, y: NDArray):
    m_curr = 0
    b_curr = 0
    n = len(x)
    iterations = 1000
    learning_rate = 0.005

    for i in range(iterations):
        y_predicted = m_curr * x + b_curr
        md = -(2/n) * sum( x * (y-y_predicted) )
        bd = -(2/n) * sum( y-y_predicted )
        m_curr = m_curr - learning_rate * bd
        b_curr = b_curr - learning_rate * md
        loss = 1/n * sum( err*err for err in (y-y_predicted) )
        is_close = abs(loss) < 0.99

        print(f"i: {i} m: {m_curr:.4f} b: {b_curr:.4f} loss = {loss:.4f} close: {is_close}")
        if is_close:
            break


x = np.array([1, 2, 3, 4, 5])
y = np.array([5, 7, 9, 11, 13])
gradient_descent(x, y)
