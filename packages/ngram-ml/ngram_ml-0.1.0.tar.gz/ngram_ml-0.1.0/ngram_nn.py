import torch


class NGramNeuralNet(torch.nn.Module):
    """
    A neural network that takes in a sequence of words and predicts the next word.
    """

    def __init__(self, n_grams, in_size, embed_size=100):
        super().__init__()

        self.embedding = torch.nn.Embedding(in_size, embed_size)
        self.linear = torch.nn.Linear(embed_size * (n_grams - 1), in_size)

    def forward(self, x: torch.tensor) -> torch.tensor:
        """
        Forward pass of the neural network.
        :param x: input tensor
        :type x: torch.tensor
        :return: Network output
        :rtype: torch.tensor
        """

        x = self.embedding(x)
        x = x.view(x.shape[0], -1)
        x = self.linear(x)
        return x

    def train(self, x, y, n_epochs=100, lr=0.01) -> None:
        """
        Train the neural network.
        :param x: input tensor
        :type x: torch.tensor
        :param y: target tensor
        :type y: torch.tensor
        :param n_epochs: number of epochs to train for, defaults to 100
        :type n_epochs: int, optional
        :param lr: learning rate, defaults to 0.01
        :type lr: float, optional
        :return: None
        :rtype: None
        """
        loss_fn = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.parameters(), lr=lr)

        for epoch in range(n_epochs):
            y_pred = self.forward(x)
            loss = loss_fn(y_pred, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if epoch % 10 == 0:
                print(f"Epoch: {epoch}, Loss: {loss.item()}")
