from payoff import call_payoff  # -----> uses vectorization so can't use here ig.
import plotly.graph_objects as go


# ====================================
# One-Step Binomial Pricing
# ====================================

def stock_moves(S, u, d):
    Su = S * u
    Sd = S * d
    return Su, Sd


def call_payoff(Stike_Price, Stock_price):
    return max(Stock_price - Stike_Price, 0)


def put_payoff(Strike_Price, Stock_price):
    return max(Strike_Price - Stock_price, 0)


def option_payoffs(Su, Sd, K, option_type="call"):

    if option_type == "call":
        Cu = call_payoff(K, Su)
        Cd = call_payoff(K, Sd)

    elif option_type == "put":
        Cu = put_payoff(K, Su)
        Cd = put_payoff(K, Sd)

    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return Cu, Cd


def hedge_ratio(Cu, Cd, Su, Sd):
    delta = (Cu - Cd) / (Su - Sd)
    return delta


def bond_position(Cu, delta, Su, r):
    return (Cu - delta * Su) / (1 + r)
    # -------> Its the price of the portfolio at the current time
    # by discounting using the interest rate.


def option_price(S, delta, B):
    return delta * S + B


def price_one_step_option(S, K, u, d, r, option_type="call"):
    Su, Sd = stock_moves(S, u, d)
    Cu, Cd = option_payoffs(
        Su,
        Sd,
        K,
        option_type=option_type
    )
    delta = hedge_ratio(Cu, Cd, Su, Sd)
    B = bond_position(Cu, delta, Su, r)
    price = option_price(S, delta, B)

    return (Su, Sd, Cu, Cd, delta, B, price)


# ==============================================
# Multi-Step Binomial Pricing
# ==============================================

class Stock_tree:

    def __init__(self, up, down, rate_of_interest):

        self.up = up
        self.down = down
        self.rate = rate_of_interest
        # Risk Neutral Probability
        self.p = (
            (1 + self.rate - self.down)
            / (self.up - self.down)
        )

    def reduced_tree(self, max_level, stock_price):
        stock_tree = []
        for step in range(max_level + 1):
            level = []
            for up_moves in range(step + 1):
                S = round(
                    stock_price
                    * (self.up ** up_moves)
                    * (self.down ** (step - up_moves)),
                    2
                )
                level.append(S)
            stock_tree.append(level)

        return stock_tree

    def option_pricing(
        self,
        stock_tree,
        strike_price,
        option_type="call"
    ):

        option_payoff = []

        for S in stock_tree[-1]:

            if option_type == "call":
                option_payoff.append(
                    max(S - strike_price, 0)
                )

            elif option_type == "put":
                option_payoff.append(
                    max(strike_price - S, 0)
                )

        return option_payoff

    def backward_induction(self, payoffs):
        values = payoffs
        while len(values) > 1:
            new_values = []
            for i in range(len(values) - 1):
                Vd = values[i]
                Vu = values[i + 1]
                V = (
                    self.p * Vu
                    + (1 - self.p) * Vd
                ) / (1 + self.rate)
                new_values.append(round(V, 2))
            values = new_values

        return values[0]

    def option_tree(self, payoffs):
        layers = [payoffs]
        values = payoffs
        while len(values) > 1:
            new_values = []
            for i in range(len(values) - 1):
                Vd = values[i]
                Vu = values[i + 1]
                V = (
                    self.p * Vu
                    + (1 - self.p) * Vd
                ) / (1 + self.rate)
                new_values.append(round(V, 2))

            layers.append(new_values)
            values = new_values
        layers.reverse()

        return layers


# =============================================
# Visualization
# =============================================
# ----> Here Comes Visualization, completely done using AI
# Keeping it separate from pricing logic.
#
# =============================================

def plot_stock_tree(tree):

    fig = go.Figure()

    for level, nodes in enumerate(tree):

        for pos, value in enumerate(nodes):

            fig.add_trace(
                go.Scatter(
                    x=[level],
                    y=[pos - level / 2],
                    mode="markers+text",
                    text=[round(value, 2)],
                    textposition="top center",
                    showlegend=False
                )
            )

            if level > 0:

                if pos < len(tree[level - 1]):

                    fig.add_shape(
                        type="line",
                        x0=level - 1,
                        y0=pos - ((level - 1) / 2),
                        x1=level,
                        y1=pos - (level / 2)
                    )

                if pos > 0:

                    fig.add_shape(
                        type="line",
                        x0=level - 1,
                        y0=(pos - 1) - ((level - 1) / 2),
                        x1=level,
                        y1=pos - (level / 2)
                    )

    fig.update_layout(
        title="Binomial Stock Tree",
        xaxis_title="Time Step",
        yaxis_visible=False
    )

    fig.show()


def plot_option_tree(option_tree):

    fig = go.Figure()

    for level, nodes in enumerate(option_tree):

        for pos, value in enumerate(nodes):

            fig.add_trace(
                go.Scatter(
                    x=[level],
                    y=[pos - level / 2],
                    mode="markers+text",
                    text=[round(value, 2)],
                    textposition="top center",
                    showlegend=False
                )
            )

            if level > 0:

                if pos < len(option_tree[level - 1]):

                    fig.add_shape(
                        type="line",
                        x0=level - 1,
                        y0=pos - ((level - 1) / 2),
                        x1=level,
                        y1=pos - (level / 2)
                    )

                if pos > 0:

                    fig.add_shape(
                        type="line",
                        x0=level - 1,
                        y0=(pos - 1) - ((level - 1) / 2),
                        x1=level,
                        y1=pos - (level / 2)
                    )

    fig.update_layout(
        title="Binomial Option Tree",
        xaxis_title="Backward Induction Levels",
        yaxis_visible=False
    )

    fig.show()


# ============================================================================
# Early Binary Tree Attempt (Preserved)
# ============================================================================
#
# Started with explicit nodes and recursion.
# Later realized:
#
# Sud == Sdu
#
# so a full binary tree is unnecessary.
#
# Keeping this here because it reflects the evolution of the project.
#
# ============================================================================

class Node:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


"""
def make_tree(self, level, max_level, index, stock_price):

    if level > max_level:
        return None

    MyNode = Node(stock_price)

    MyNode.left = self.make_tree(
        level + 1,
        max_level,
        2**index,
        stock_price * self.down
    )

    MyNode.right = self.make_tree(
        level + 1,
        max_level,
        2**index + 1,
        stock_price * self.up
    )

    return MyNode


def make_tree_list(self, level, max_level, stock_price):

    if level == max_level:
        return stock_price

    return [
        stock_price,

        self.make_tree_list(
            level + 1,
            max_level,
            stock_price * self.down
        ),

        self.make_tree_list(
            level + 1,
            max_level,
            stock_price * self.up
        )
    ]
"""