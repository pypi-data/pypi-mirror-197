from __future__ import annotations

import math


class Numeric:
    """
    Base class for tracking numeric values
    """

    def __init__(
        self,
        value: float,
        children: tuple[Numeric, Numeric | None] = (),
        generative_op: str = "",
        _pass_local_derivative: callable = lambda: None,
        grad: float = 0.0,
    ) -> None:
        """Children & Parent naming can be confusing as for forward calculation and backward calculation they are opposite.
        We will name the attributes in a way that the 'generative_op' applied on children will generate self on the forward pass.


        :param value: Numeric value
        :type value: float
        :param children: Child nodes in backprop and parent node in forward pass
        :type children: Numeric
        :param generative_op: Function that generated self by applied on children
        :type generative_op: str
        :param _backward_func: Function that backpropagates the gradients from self to children
        :type _backward_func: Callable
        :param grad: Gradient of the root of the Network (last layer/neuron) wrt. self
        :type grad: Float
        """
        self.value = value
        self.children = children
        self.generative_op = generative_op
        self._pass_local_derivative = _pass_local_derivative
        self.grad = grad

    def __repr__(self) -> str:
        return f"Numeric(value={self.value})"

    def __add__(self, other: float | Numeric) -> Numeric:
        """self + other

        :param other: Value to sum
        :type other: float | Numeric
        :return: Summed up Numeric type
        :rtype: Numeric
        """
        if type(other) != Numeric:
            other = Numeric(other)

        out = Numeric(
            value=self.value + other.value,
            children=(self, other),
            generative_op="+",
        )

        def _func_to_pass_local_derivative():
            # += is used below because if self and other are same object like b = a + a, whithout + grads are overwriting each other.
            self.grad += 1 * out.grad
            other.grad += 1 * out.grad

        out._pass_local_derivative = _func_to_pass_local_derivative

        return out

    def __radd__(self, other: float | Numeric) -> Numeric:
        """other + self

        :param other: Value to sum
        :type other: float | Numeric
        :return: Summed up Numeric type
        :rtype: Numeric
        """
        return self + other

    def __mul__(self, other: float | Numeric) -> Numeric:
        """self * other

        :param other: value to multiply
        :type other: float | Numeric
        :return: Multiplied Numeric
        :rtype: Numeric
        """

        if type(other) != Numeric:
            other = Numeric(other)

        out = Numeric(value=self.value * other.value, children=(self, other))

        def _func_to_pass_local_derivative() -> None:
            """Defining when multiplication is applied but run during backward pass.

            :return: None
            :rtype: None
            """
            # += is used below because if self and other are same object like b = a + a, whithout + grads are overwriting each other.
            self.grad += other.value * out.grad
            other.grad += self.value * out.grad

        out._pass_local_derivative = _func_to_pass_local_derivative

        return out

    def __rmul__(self, other: float | Numeric) -> Numeric:
        """other * self

        :param other: value to multiply
        :type other: float | Numeric
        :return: Multiplied Numeric
        :rtype: Numeric
        """
        return self * other

    def __sub__(self, other: float | Numeric) -> Numeric:
        """self - other

        :param other: Value to sum
        :type other: float | Numeric
        :return: Subtracted Numeric type
        :rtype: Numeric
        """
        if type(other) != Numeric:
            other = Numeric(other)

        out = Numeric(value=self.value - other.value, children=(self, other))

        def _func_to_pass_local_derivative() -> None:
            """Defining when subtraction is applied but run during backward pass.

            :return: None
            :rtype: None
            """
            self.grad += 1 * out.grad
            other.grad += -1 * out.grad

        out._pass_local_derivative = _func_to_pass_local_derivative

        return out

    def __rsub__(self, other: float | Numeric) -> Numeric:
        """other - self

        :param other: Value to sum
        :type other: float | Numeric
        :return: Subtracted Numeric type
        :rtype: Numeric
        """
        return other + (-1 * self)

    def __pow__(self, power: float | Numeric) -> Numeric:
        """self**power

        :param power: Value to take power of self
        :type power: float | Numeric
        :return: powered Numeric
        :rtype: Numeric
        """
        if type(power) != Numeric:
            power = Numeric(power)

        out = Numeric(value=self.value**power.value, children=(self, power))

        def _func_to_pass_local_derivative() -> None:
            """Defining when power operation is applied but run during backward pass.

            :return: None
            :rtype: None
            """
            self.grad += (
                power.value * ((self.value) ** (power.value - 1)) * out.grad
            )  # Derivative wrt. base
            power.grad += (
                math.log(self.value) * ((self.value) ** (power.value)) * out.grad
            )  # derivative wrt. power

        out._pass_local_derivative = _func_to_pass_local_derivative

        return out

    def __rpow__(self, base: float | Numeric) -> Numeric:
        """base**self

        :param base: Value to be powered by self
        :type base: float | Numeric
        :return: Subtracted Numeric
        :rtype: Numeric
        """

        if type(base) != Numeric:
            base = Numeric(base)

        return base**self

    def __truediv__(self, other: float | Numeric) -> Numeric:
        """self / other

        :param other: Value to divide self
        :type other: float | Numeric
        :return: divided Numeric
        :rtype: Numeric
        """
        return self * (other**-1)

    def __rtruediv__(self, other: float | Numeric) -> Numeric:
        """other / self

        :param other: Value to be divided by self
        :type other: float | Numeric
        :return: divided Numeric
        :rtype: Numeric
        """
        return (self**-1) * other

    def sigmoid(self) -> Numeric:
        """Apply sigmoid activation/transformation on self

        :return: transformed Numeric
        :rtype: Numeric
        """
        out = Numeric(1 / (1 + math.exp(-self.value)), children=(self, None))

        def _func_to_pass_local_derivative() -> None:
            """Defining when sigmoid is applied but run during backward pass.

            :return: None
            """
            self.grad += out.value * (1 - out.value) * out.grad

        out._pass_local_derivative = _func_to_pass_local_derivative
        return out

    def tanH(self) -> Numeric:
        """Apply tanH activation/transformation on self

        :return: transformed Numeric
        :rtype: Numeric
        """
        out = Numeric(math.tanh(self.value), children=(self, None))

        def _func_to_pass_local_derivative() -> None:
            """Defining when tanH is applied but run during backward pass.

            :return: None
            """
            self.grad += (1 - out.value**2) * out.grad

        out._pass_local_derivative = _func_to_pass_local_derivative
        return out

    def ReLU(self) -> Numeric:
        """Apply ReLU activation/transformation on self

        :return: transformed Numeric
        :rtype: Numeric
        """
        out = Numeric(max(0, self.value), children=(self, None))

        def _func_to_pass_local_derivative() -> None:
            """Defining when ReLU is applied but run during backward pass.

            :return: None
            """
            self.grad += (self.value > 0) * out.grad

        out._pass_local_derivative = _func_to_pass_local_derivative
        return out

    def leaky_ReLU(self, leakage_slope: float = 0.0) -> Numeric:
        """Apply leaky ReLU activation/transformation on self

        :param leakage_slope: slope of the leaky part of ReLU
        :type leakage_slope: float
        :return: transformed Numeric
        :rtype: Numeric
        """
        assert leakage_slope >= 0, "leakage_slope must be non-negative"

        out = Numeric(
            max(leakage_slope * self.value, self.value), children=(self, None)
        )

        def _func_to_pass_local_derivative() -> None:
            """Defining when leaky ReLU is applied but run during backward pass.

            :return: None
            """
            self.grad += (
                (self.value > 0) + leakage_slope * (self.value <= 0)
            ) * out.grad

        out._pass_local_derivative = _func_to_pass_local_derivative

        return out

    @staticmethod
    def softmax(numerics: list[Numeric, ...]) -> list[Numeric, ...]:
        pass

    @staticmethod
    def parse_till_leaf(
        current_node, parsed_nodes_from_leaf_to_root=[], visited_nodes=[]
    ) -> list:
        if current_node not in visited_nodes:
            visited_nodes.append(current_node)
            for child_node in current_node.children:
                Numeric.parse_till_leaf(
                    child_node, parsed_nodes_from_leaf_to_root, visited_nodes
                )

            parsed_nodes_from_leaf_to_root.append(current_node)

        if (
            all(item in parsed_nodes_from_leaf_to_root for item in visited_nodes)
            and len(visited_nodes) != 0
        ):
            return parsed_nodes_from_leaf_to_root

    def backward(self) -> None:
        """Calculates gradients for all nodes below self -- Doesn't make an update step

        :return: None
        :rtype: None
        """

        # Backpropagate the loss and calculate derivatives for each node
        self.grad = 1
        for node in reversed(Numeric.parse_till_leaf(self)):
            node._pass_local_derivative()

    def zero_grad(self) -> None:
        """Set gradients to zero from self to leaves

        :return: None
        :rtype: None
        """
        for node in Numeric.parse_till_leaf(self):
            node.grad = 0
