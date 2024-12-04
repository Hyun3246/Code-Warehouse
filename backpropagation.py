import numpy as np

class MLP(object):

    # sigmoid function
    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
    
    # identity matrix
    @staticmethod
    def identity(x):
        return x
    
    # inverse of sigmoid
    @staticmethod
    def inv_sig(x):
        result = MLP.sigmoid(x)
        return result * (1 - result)
    
    def __init__(self, **kwargs):
        self.layers = kwargs['layers']      # list for layers
        self.activate = [MLP.identity]      # list for activation function
        self.weights = [1]                  # list for weights
        self.bias = [0]                     # list for bias
        self.learning_rate = 0.001          # learning rate

        # stack layers
        for i in range(1, len(self.layers)):

            # make weights and bias matrix
            self.weights.append(np.random.normal(0, 0.5, (self.layers[i-1], self.layers[i])))
            self.bias.append(np.random.normal(0, 0.5, self.layers[i]))
            
            # append activation function
            if i != len(self.layers) - 1:
                self.activate.append(MLP.sigmoid)
            else:
                self.activate.append(MLP.identity)
    
    # feed forward
    def feed_forward(self, xs):
        self.U = [xs]       # list for result of XW + b
        self.Z = [xs]       # list for result of a = g(z)

        for i in range(1, len(self.layers)):
            u = self.Z[i-1].dot(self.weights[i]) + self.bias[i]     # XW + b
            z = self.activate[i](u)                                 # a = g(z)
            self.U.append(u)
            self.Z.append(z)

        return self.Z[-1]       # return latest result
    
    # back propagation
    def back_propagate(self, xs, ys):
        pred_ys = self.feed_forward(xs)     # feed forward
        self.D = []                         # list for errors

        for i in reversed(range(1, len(self.layers))):

            # derivative
            if i == len(self.layers) - 1:       # for last layer
                d = pred_ys - ys
            else:                               # for other layers
                d = self.inv_sig(self.U[i]) * (self.D[-1].dot(self.weights[i+1].T))
            
            dW = self.Z[i-1].T.dot(d)
            db = np.sum(d, axis=0)

            # update weights and bias
            self.weights[i] -= self.learning_rate * dW
            self.bias[i] -= self.learning_rate * db
            
            self.D.append(d)
        return
    
    # evaluation function
    def evaluate(self, xs, ys):
        pred_ys = self.feed_forward(xs)
        d = pred_ys - ys
        return np.sqrt(np.mean(d**2))

# sample
if __name__ == '__main__':
    
    model = MLP(layers=[1,5,5,5,1])
    
    train_x = np.linspace(-5,5,10, dtype=np.float64)
    train_y = np.sin(train_x)

    xs = train_x.reshape(-1,1)
    ys = train_y.reshape(-1,1)

    pred_ys = model.feed_forward(xs)

    for i in range(50000):
        model.back_propagate(xs, ys)

        if (i+1) % 5000 == 0:
            error = model.evaluate(xs, ys)
            print('ITER={:05d}, RMSE={:.4f}'.format(i+1, error))
            
    pred_ys = model.feed_forward(xs)