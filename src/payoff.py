
import numpy as np

# ==========================================
# Primitive Payoff Geometry
# ==========================================

def call_payoff(strike_p, stock_p):
    payoff = np.maximum(stock_p - strike_p, 0)
    return payoff


def put_payoff(strike_p, stock_p):
    payoff = np.maximum(strike_p - stock_p, 0)
    return payoff


def long_stock(stock_p, stock_purchase_price):
    return stock_p - stock_purchase_price


# ====================================
# ====================================

def long_call(strike_p, stock_p):
    return call_payoff(strike_p, stock_p)


def short_call(strike_p, stock_p):
    return -1 * call_payoff(strike_p, stock_p)


def long_put(strike_p, stock_p):
    return put_payoff(strike_p, stock_p)


def short_put(strike_p, stock_p):
    return -1 * put_payoff(strike_p, stock_p)


# ==============================
# Profit & Loss Positions
# ==============================

def long_call_profit(strike_p, stock_p, premium):
    return long_call(strike_p, stock_p) - premium


def short_call_profit(strike_p, stock_p, premium):
    return short_call(strike_p, stock_p) + premium


def long_put_profit(strike_p, stock_p, premium):
    return long_put(strike_p, stock_p) - premium


def short_put_profit(strike_p, stock_p, premium):
    return short_put(strike_p, stock_p) + premium


# ==========================================
# Strategy Composition
# ==========================================
#
# Phase 1:
# Building more complex option structures from simple payoff blocks.

def bull_call_spread(high_strike, low_strike, stock_p):
    return long_call(low_strike,stock_p) + short_call(high_strike, stock_p) 

def covered_call(strike_p, stock_p, stock_purchase_p, premium):
    return long_stock(stock_p, stock_purchase_p) + short_call_profit(strike_p, stock_p, premium)

def protective_put(strike_p, stock_p, stock_purchase_p, premium):
    return long_put_profit(strike_p, stock_p, premium) + long_stock(stock_p, stock_purchase_p)

def long_straddle(same_strike_p, stock_p, call_premium, put_premium):
    return long_call_profit(same_strike_p, stock_p, call_premium) + long_put_profit(same_strike_p, stock_p, put_premium)

def long_strangle(high_strike, low_strike, stock_p, call_premium, put_premium):
    return long_call_profit(high_strike, stock_p, call_premium) + long_put_profit(low_strike, stock_p, put_premium)


# ==================================
# Future Strategies
# ==================================
#
# Bear Put Spread
# Iron Condor
# Butterfly Spread
# Collar
#