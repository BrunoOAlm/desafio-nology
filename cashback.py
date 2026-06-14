"""
Cashback calculation - Nology Challenge.

Rules consolidated from the 3 documents in the brief:
  Doc 1: base cashback = 5% on the FINAL amount (after discounts).
         VIP clients get an extra +10% on top of the base cashback.
  Doc 2: purchases with a final amount above R$ 500 -> cashback doubled (everyone).
  Doc 3: calculation order -> base cashback first, then the VIP bonus.

Assumptions (where the brief is intentionally ambiguous):
  - The "above R$ 500" rule is checked against the ALREADY-discounted amount,
    consistent with Doc 1 (the whole calculation is based on the final amount).
  - The promotion (doubling) is applied last, on the cashback that already
    includes the VIP bonus.
"""

BASE_CASHBACK = 0.05        # 5%
VIP_BONUS = 0.10            # +10% on top of the base cashback
PROMO_THRESHOLD = 500.0     # above this amount, cashback doubles
PROMO_MULTIPLIER = 2


def calculate_cashback(client_type: str, purchase_amount: float, coupon_discount: float = 0.0) -> float:
    """Return the final cashback in BRL, rounded to 2 decimal places."""
    # 1. apply the coupon discount (cashback is based on the final amount)
    final_amount = purchase_amount * (1 - coupon_discount / 100)

    # 2. base cashback of 5%
    cashback = final_amount * BASE_CASHBACK

    # 3. VIP bonus: +10% on top of the base cashback
    is_vip = client_type.strip().lower() == "vip"
    if is_vip:
        cashback *= (1 + VIP_BONUS)

    # 4. promotion: double above R$ 500 (applies to everyone, including VIPs)
    if final_amount > PROMO_THRESHOLD:
        cashback *= PROMO_MULTIPLIER

    return round(cashback, 2)


if __name__ == "__main__":
    # Quick demo for questions 2, 3 and 4 of the challenge
    scenarios = [
        ("Question 2", "vip",     600, 20),
        ("Question 3", "regular", 600, 10),
        ("Question 4", "vip",     600, 15),
    ]
    for label, client, amount, coupon in scenarios:
        result = calculate_cashback(client, amount, coupon)
        print(f"{label}: client={client}, purchase=R${amount}, coupon={coupon}% -> cashback=R${result:.2f}")
