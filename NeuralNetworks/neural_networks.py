import numpy as np

def sigmoid(in_data):
    return 1/(1+np.exp(-in_data))

def feedforward(in_data, weight, bias):
    return sigmoid(np.dot(weight.T, in_data) + b)

def backward(x, r_y, c_y, w, b, learn_rate=0.1):
    gradient_w = learn_rate * c_y * (1-c_y) * (c_y-r_y) * x
    gradient_b = learn_rate * c_y * (1-c_y) * (c_y-r_y)
    w = w - gradient_w
    b = b - gradient_b
    return w,b



X = [[0, 0], [0, 1], [1, 0], [1, 1]]
Y = [[0],[0],[0],[1]]
w1 = [0,0]
w2 = [0,0]
b1 = 0
b2 = 0

for i in range(1000):
    for j in len(X):
        input2hidden_y = feedforward(X[j], w1, b1)
        hidden2output_y = feedforward(input2hidden_y, w2 ,b2)

        w2, b2 = backward(input2hidden_y, Y[j], hidden2output_y, w2, b2)
        w1, b1 = backward(X[J], Y[j], input2hidden_y, w1, b1)
        
