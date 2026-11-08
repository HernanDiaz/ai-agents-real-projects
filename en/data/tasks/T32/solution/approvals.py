"""Repair shop estimates that need the customer's approval before starting."""
from estimates import repair_estimate

APPROVAL_THRESHOLD = 150   # dollars, sales tax included: above it we call the customer


def estimate_with_approval(parts, hours, purchase_date, today, cause):
    """The estimate of a repair with one more field, "approval": whether to call the
    customer before starting. If any part has no price yet, there is no total and we
    have to call: the repair shop does not make up prices."""
    if any(price is None for _, price in parts):
        return {"total": None, "approval": True}
    estimate = repair_estimate(parts, hours, purchase_date, today, cause)
    return dict(estimate, approval=estimate["total"] > APPROVAL_THRESHOLD)
