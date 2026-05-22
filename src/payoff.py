
import numpy as np
def call_payoff(strike_p, stock_p):
    payoff = np.maximum(stock_p - strike_p, 0)
    return payoff



def long_call(strike_p, stock_p):
    return call_payoff(strike_p, stock_p)

def short_call(strike_p, stock_p):
    return -1 * call_payoff(strike_p, stock_p)

def long_put(strike_p, stock_p):
    return call_payoff(stock_p , strike_p)  # put_payoff(strick_p, stock_p) ----> return max(stock_p - strike_p)

def short_put(strike_p, stock_p):
    return -1 * call_payoff(stock_p , strike_p)  # put_payoff(strick_p, stock_p) ----> return max(stock_p - strike_p)                                                                                                                               



def long_call_profit(strike_p, stock_p, premium):
    return call_payoff(strike_p, stock_p) - premium

def short_call_profit(strike_p, stock_p, premium):
    return -1 * call_payoff(strike_p, stock_p) + premium

def long_put_profit(strike_p, stock_p, premium):
    return call_payoff(stock_p , strike_p) - premium # put_payoff(strick_p, stock_p) ----> return max(stock_p - strike_p, 0)

def short_put_profit(strike_p, stock_p, premium):
    return -1 * call_payoff(stock_p , strike_p) + premium # put_payoff(strick_p, stock_p) ----> return max(stock_p - strike_p, 0)                                                                                                                               