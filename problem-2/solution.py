"""
CIEDE2000 color difference calculator.
Reference: Sharma, Wu, Dalal (2005)
"""

import math


def ciede2000(L1, a1, b1, L2, a2, b2, kL=1.0, kC=1.0, kH=1.0):
    """
    Compute the CIEDE2000 color difference between two CIELAB colors.

    Args:
        L1, a1, b1: CIELAB values for the first color
        L2, a2, b2: CIELAB values for the second color
        kL, kC, kH: parametric weighting factors (default 1.0)

    Returns:
        float: the CIEDE2000 color difference (ΔE00)
    """
    # Step 1: Calculate C*ab for each color
    C1 = math.sqrt(a1 ** 2 + b1 ** 2)
    C2 = math.sqrt(a2 ** 2 + b2 ** 2)
    avg_C = (C1 + C2) / 2.0

    # G factor
    avg_C7 = avg_C ** 7
    G = 0.5 * (1.0 - math.sqrt(avg_C7 / (avg_C7 + 25.0 ** 7)))

    # Modified a' values
    a1p = a1 * (1.0 + G)
    a2p = a2 * (1.0 + G)

    # C' (modified chroma)
    C1p = math.sqrt(a1p ** 2 + b1 ** 2)
    C2p = math.sqrt(a2p ** 2 + b2 ** 2)
    avg_Cp = (C1p + C2p) / 2.0

    # h' (hue angle in degrees, 0-360)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360.0

    # Step 2: delta L', delta C', delta H'
    delta_Lp = L2 - L1
    delta_Cp = C2p - C1p

    # delta h'
    if C1p * C2p == 0.0:
        delta_hp = 0.0
    elif abs(h2p - h1p) <= 180.0:
        delta_hp = h2p - h1p
    elif h2p - h1p > 180.0:
        delta_hp = h2p - h1p - 360.0
    else:
        delta_hp = h2p - h1p + 360.0

    # delta H'
    delta_Hp = 2.0 * math.sqrt(C1p * C2p) * math.sin(math.radians(delta_hp / 2.0))

    # Step 3: Calculate CIEDE2000
    avg_Lp = (L1 + L2) / 2.0

    # Mean hue
    if C1p * C2p == 0.0:
        avg_Hp = h1p + h2p
    elif abs(h1p - h2p) <= 180.0:
        avg_Hp = (h1p + h2p) / 2.0
    elif h1p + h2p < 360.0:
        avg_Hp = (h1p + h2p + 360.0) / 2.0
    else:
        avg_Hp = (h1p + h2p - 360.0) / 2.0

    # T
    T = (1.0
         - 0.17 * math.cos(math.radians(avg_Hp - 30.0))
         + 0.24 * math.cos(math.radians(2.0 * avg_Hp))
         + 0.32 * math.cos(math.radians(3.0 * avg_Hp + 6.0))
         - 0.20 * math.cos(math.radians(4.0 * avg_Hp - 63.0)))

    # S_L
    S_L = 1.0 + (0.015 * (avg_Lp - 50.0) ** 2) / math.sqrt(20.0 + (avg_Lp - 50.0) ** 2)

    # S_C
    S_C = 1.0 + 0.045 * avg_Cp

    # S_H
    S_H = 1.0 + 0.015 * avg_Cp * T

    # R_T (rotation term)
    delta_theta = 30.0 * math.exp(-((avg_Hp - 275.0) / 25.0) ** 2)
    avg_Cp7 = avg_Cp ** 7
    R_C = 2.0 * math.sqrt(avg_Cp7 / (avg_Cp7 + 25.0 ** 7))
    R_T = -R_C * math.sin(math.radians(2.0 * delta_theta))

    # Final calculation
    term_L = delta_Lp / (S_L * kL)
    term_C = delta_Cp / (S_C * kC)
    term_H = delta_Hp / (S_H * kH)

    return math.sqrt(term_L ** 2 + term_C ** 2 + term_H ** 2 + R_T * term_C * term_H)
