from payoff import call_payoff # -----> uses vectorization so can't use here ig.

def stock_moves(S, u, d):
    Su = S * u
    Sd = S * d
    return Su, Sd

def call_payoff(Stike_Price, Stock_price):
    return max(Stock_price - Stike_Price, 0)

def option_payoffs(Su, Sd, K):
    Cu = call_payoff(K, Su)
    Cd = call_payoff(K, Sd)   # ------> Its 0 in most case.
    return Cu, Cd

def hedge_ratio(Cu, Cd, Su, Sd):
    delta = (Cu - Cd) / (Su - Sd)
    return delta

def bond_position(Cu, delta, Su, r):
    return (Cu - delta * Su) / (1 + r)  # -------> Its the price of the portfolio at the current time by discounting using the interest rate.

def option_price(S, delta, B):
    return delta * S + B # -------->  
 
def price_one_step_call(S, K, u, d, r):

    Su, Sd = stock_moves(S, u, d)

    Cu, Cd = option_payoffs(Su, Sd, K)

    delta = hedge_ratio(Cu, Cd, Su, Sd)

    B = bond_position(Cu, delta, Su, r)

    price = option_price(S, delta, B)

    return (Su, Sd, Cu, Cd, delta, B, price)




#------- going for a Multi- Step Tree now :

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Stock_tree:
    def __init__(self, up, down, rate_of_interest): 
        self.up = up
        self.down = down
        self.rate = rate_of_interest
        self.p = (1 + self.rate - self.down)/ (self.up - self.down)
        
    def make_tree(self,  level, max_level, index, stock_price):
        if level > max_level :
            return None
        MyNode = Node(stock_price)
        MyNode.left = self.make_tree(level + 1, max_level, 2**index, stock_price * self.down)
        MyNode.right = self.make_tree(level + 1, max_level, 2**index + 1, stock_price * self.up)

        return MyNode
    
    def make_tree_list(self, level, max_level, stock_price):
        if level == max_level:
            return stock_price

        return [
            stock_price,
            self.make_tree_list(level + 1, max_level, stock_price * self.down),
            self.make_tree_list(level + 1, max_level, stock_price * self.up) ]
    # no need for trees and nodes... like we can just use.. S  = S0 * u**up_step * d**(step - up_step)
    
    def reduced_tree(self, max_level, stock_price):
        stock_tree = [ ]
        for step in range(max_level + 1):
            level = []

            for up_moves in range(step + 1):

                S = round(stock_price * (self.up ** up_moves) * (self.down ** (step - up_moves)), 2)

                level.append(S)

            stock_tree.append(level)
        return stock_tree
    
    def option_pricing(self, stock_tree, strike_price):
        option_payoff = []
        for i in stock_tree[-1]:
            option_payoff.append(max(i - strike_price, 0))
        return option_payoff
    
    def backward_induction(self, payoffs):

        values = payoffs

        while len(values) > 1:

            new_values = []

            for i in range(len(values)-1):

                Vd = values[i]
                Vu = values[i+1]

                V = (
                self.p * Vu +
                (1-self.p) * Vd
                )/(1+self.rate)

                new_values.append(round(V,2))

            print(new_values)

            values = new_values

        return values[0]