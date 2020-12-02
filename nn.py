import numpy as np
from Tensor import Tensor
from Loss import MSELoss


class Linear():

    def __init__(self, in_feats, out_feats, bias=True):
        self.in_feats = in_feats
        self.out_feats = out_feats
        self.weights = Tensor.random_uniform(self.in_feats, self.out_feats)
        self.bias_flag = bias

        if self.bias_flag:
            self.bias = Tensor.random_uniform(1, self.out_feats)

    def forward(self, input):
        return input.dot(self.weights)+self.bias

    def __call__(self, input):
        return input.dot(self.weights)+self.bias


class ReLU():
    # Missing init method here

    @staticmethod
    def __call__(input):
        output = Tensor(np.maximum(input.value, 0),
                        children=(input,), fun='ReLUBackward')

        def _backward():
            input.grad += output.grad*(output.value)

        output._backward = _backward

        return output


class Sigmoid():

    @staticmethod
    def __call__(input):

        val = 1/(1+np.exp(-(input.value)))

        output = Tensor(val,
                        children=(input,), fun='SigmoidBackard')

        def _backward():
            input.grad += output.grad*(val*(1-val))

        output._backward = _backward

        return output


class Softmax():
    @staticmethod
    def __call__(input, dim):
        exp = input.exp()
        sum = (input.exp()).sum(dim)
        sum.expand_dim(dim)
        return exp/sum


class LogSoftmax():

    @staticmethod
    def __call__(input, dim):
        exp = np.exp(input.value)
        sum = np.sum(np.exp(input.value), 1)
        sum = np.expand_dims(sum, 1)
        val = np.log(exp/sum)
        output = Tensor(val,
                        children=(input,), fun='LogSoftmaxBackward')

        # Complete credit to TinyGrad for this gradient...
        def _backward():
            input.grad += (output.grad)-(np.exp(val) *
                                         (np.sum(output.grad, axis=1).reshape((-1, 1))))

        output._backward = _backward

        return output


if __name__ == "__main__":

    x = Tensor([[0.001, 0.2, -1, 3], [3.2, 1, 3, 1]])

    softmax = LogSoftmax()

    y = softmax(x, dim=1)

    print(y)

    actual_out = Tensor([[1, 2, 3, 4], [3.2, 1, 3, 1]])

    mse = MSELoss()
    loss = mse(y, actual_out)
    loss.backward()
    print(x.grad)

    import torch

    x = torch.tensor([[0.001, 0.2, -1, 3], [3.2, 1, 3, 1]], requires_grad=True)
    softmax = torch.nn.LogSoftmax(dim=1)
    y = softmax(x)
    print(y)

    actual_out = torch.tensor(
        [[1, 2, 3, 4], [3.2, 1, 3, 1]], requires_grad=True)
    mse = torch.nn.MSELoss()
    loss = mse(y, actual_out)
    loss.backward()
    print(x.grad)
