import math
import numpy as np
from numpy.typing import NDArray

def gradient_descent(x: NDArray, y: NDArray):
    m_curr = 0
    b_curr = 0
    n = len(x)
    iterations = 1000
    learning_rate = 0.0005

    for i in range(iterations):
        y_predicted = m_curr * x + b_curr
        md = -(2/n) * sum(x * (y-y_predicted))
        bd = -(2/n) * sum(y-y_predicted)
        m_curr = m_curr - learning_rate * bd
        b_curr = b_curr - learning_rate * md
        loss = 1/n * sum( err*err for err in (y-y_predicted) )
        is_close = abs(loss) < 0.99
        if is_close: break
