"""
Glicko-2 rating calculator for two-player games.
Reference solution — ported from lichess-org/scalachess.
"""

import math

MULTIPLIER = 173.7178
DEFAULT_RATING = 1500.0
CONVERGENCE_TOLERANCE = 0.000001
ITERATION_MAX = 1000


def _to_glicko2_rating(rating):
    return (rating - DEFAULT_RATING) / MULTIPLIER


def _to_glicko2_rd(rd):
    return rd / MULTIPLIER


def _to_glicko1_rating(mu):
    return mu * MULTIPLIER + DEFAULT_RATING


def _to_glicko1_rd(phi):
    return phi * MULTIPLIER


def _g(phi):
    return 1.0 / math.sqrt(1.0 + 3.0 * phi ** 2 / math.pi ** 2)


def _E(mu, mu_j, phi_j):
    return 1.0 / (1.0 + math.exp(-_g(phi_j) * (mu - mu_j)))


def _v(mu, mu_j, phi_j):
    e = _E(mu, mu_j, phi_j)
    g_val = _g(phi_j)
    return 1.0 / (g_val ** 2 * e * (1.0 - e))


def _delta(mu, mu_j, phi_j, score):
    e = _E(mu, mu_j, phi_j)
    g_val = _g(phi_j)
    v = _v(mu, mu_j, phi_j)
    return v * g_val * (score - e)


def _f(x, delta, phi, v, a, tau):
    ex = math.exp(x)
    num = ex * (delta ** 2 - phi ** 2 - v - ex)
    den = 2.0 * (phi ** 2 + v + ex) ** 2
    return num / den - (x - a) / tau ** 2


def _new_volatility(sigma, phi, v, delta, tau):
    a = math.log(sigma ** 2)

    A = a
    if delta ** 2 > phi ** 2 + v:
        B = math.log(delta ** 2 - phi ** 2 - v)
    else:
        k = 1.0
        B = a - k * abs(tau)
        while _f(B, delta, phi, v, a, tau) < 0:
            k += 1
            B = a - k * abs(tau)

    fA = _f(A, delta, phi, v, a, tau)
    fB = _f(B, delta, phi, v, a, tau)

    iterations = 0
    while abs(B - A) > CONVERGENCE_TOLERANCE and iterations < ITERATION_MAX:
        iterations += 1
        C = A + ((A - B) * fA) / (fB - fA)
        fC = _f(C, delta, phi, v, a, tau)
        if fC * fB <= 0:
            A = B
            fA = fB
        else:
            fA = fA / 2.0
        B = C
        fB = fC

    if iterations == ITERATION_MAX:
        raise RuntimeError("Glicko-2 volatility convergence failed")

    return math.exp(A / 2.0)


def _calculate_new_rd(phi, sigma, elapsed_periods):
    return math.sqrt(phi ** 2 + elapsed_periods * sigma ** 2)


def _update_player(rating, deviation, volatility, opp_rating, opp_deviation, score, tau, elapsed_periods):
    mu = _to_glicko2_rating(rating)
    phi = _to_glicko2_rd(deviation)
    sigma = volatility

    mu_j = _to_glicko2_rating(opp_rating)
    phi_j = _to_glicko2_rd(opp_deviation)

    v = _v(mu, mu_j, phi_j)
    delta = _delta(mu, mu_j, phi_j, score)

    new_sigma = _new_volatility(sigma, phi, v, delta, tau)

    phi_star = _calculate_new_rd(phi, new_sigma, elapsed_periods)

    new_phi = 1.0 / math.sqrt(1.0 / phi_star ** 2 + 1.0 / v)

    e = _E(mu, mu_j, phi_j)
    g_val = _g(phi_j)
    new_mu = mu + new_phi ** 2 * g_val * (score - e)

    return {
        "rating": _to_glicko1_rating(new_mu),
        "deviation": _to_glicko1_rd(new_phi),
        "volatility": new_sigma,
    }


def compute_game(white, black, outcome, tau=0.75, skip_deviation_increase=False):
    elapsed = 0 if skip_deviation_increase else 1

    if outcome == "white":
        s_white, s_black = 1.0, 0.0
    elif outcome == "black":
        s_white, s_black = 0.0, 1.0
    else:
        s_white, s_black = 0.5, 0.5

    w = _update_player(
        white["rating"], white["deviation"], white["volatility"],
        black["rating"], black["deviation"],
        s_white, tau, elapsed,
    )
    b = _update_player(
        black["rating"], black["deviation"], black["volatility"],
        white["rating"], white["deviation"],
        s_black, tau, elapsed,
    )
    return w, b
