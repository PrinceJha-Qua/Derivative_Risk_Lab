from payoff import call_payoff # -----> uses vectorization so can't use here ig.

def stock_moves(S, u, d):
    Su = S * u
    Sd = S * d
    return Su, Sd

def call_payoff(Stike_Price, Stock_price):
    return max(Stock_price - Stike_Price, 0)

def option_payoffs(Su, Sd, K):
    Cu = call_payoff(K, Su)
    Cd = call_payoff(K, Sd)
    return Cu, Cd

def hedge_ratio(Cu, Cd, Su, Sd):
    delta = (Cu - Cd) / (Su - Sd)
    return delta

def bond_position(Cu, delta, Su, r):
    return (Cu - delta * Su) / (1 + r)

def option_price(S, delta, B):
    return delta * S + B
 
def price_one_step_call(S, K, u, d, r):

    Su, Sd = stock_moves(S, u, d)

    Cu, Cd = option_payoffs(Su, Sd, K)

    delta = hedge_ratio(Cu, Cd, Su, Sd)

    B = bond_position(Cu, delta, Su, r)

    price = option_price(S, delta, B)

    return {
        "Su": Su,
        "Sd": Sd,
        "Cu": Cu,
        "Cd": Cd,
        "delta": delta,
        "bond": B,
        "price": price
    }