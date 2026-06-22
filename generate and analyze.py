import numpy as np
import pandas as pd
from scipy import stats
import json
from datetime import datetime, timedelta

np.random.seed(42)

# ============================================================
# 1. GENERATE SYNTHETIC USER EVENT DATA (6 months, ~6000 users)
# ============================================================
N_USERS = 6000
start_date = datetime(2025, 1, 1)
months = pd.date_range(start_date, periods=6, freq='MS')

users = []
for i in range(N_USERS):
    cohort_month = pd.Timestamp(np.random.choice(months))
    users.append({
        'user_id': f'U{i+1:05d}',
        'signup_date': cohort_month,
        'cohort_month': cohort_month.strftime('%Y-%m')
    })
users_df = pd.DataFrame(users)

# Funnel stage probabilities (realistic e-commerce drop-off)
P_VIEW_TO_CART = 0.38      # 38% of viewers add to cart
P_CART_TO_PURCHASE = 0.42  # 42% of cart adds convert to purchase

events = []
for _, u in users_df.iterrows():
    events.append({'user_id': u['user_id'], 'event': 'view', 'cohort_month': u['cohort_month']})
    if np.random.random() < P_VIEW_TO_CART:
        events.append({'user_id': u['user_id'], 'event': 'cart', 'cohort_month': u['cohort_month']})
        if np.random.random() < P_CART_TO_PURCHASE:
            events.append({'user_id': u['user_id'], 'event': 'purchase', 'cohort_month': u['cohort_month']})

events_df = pd.DataFrame(events)

# ============================================================
# 2. FUNNEL ANALYSIS
# ============================================================
funnel_counts = events_df.groupby('event')['user_id'].nunique()
funnel = {
    'view': int(funnel_counts.get('view', 0)),
    'cart': int(funnel_counts.get('cart', 0)),
    'purchase': int(funnel_counts.get('purchase', 0))
}
funnel_pct = {
    'view': 100.0,
    'cart': round(funnel['cart'] / funnel['view'] * 100, 1),
    'purchase': round(funnel['purchase'] / funnel['view'] * 100, 1)
}
drop_off = {
    'view_to_cart': round((1 - funnel['cart']/funnel['view']) * 100, 1),
    'cart_to_purchase': round((1 - funnel['purchase']/funnel['cart']) * 100, 1)
}

# ============================================================
# 3. COHORT RETENTION (simulate repeat purchase behavior over 3 months post-signup)
# ============================================================
# For each cohort, simulate % of purchasers who return in month 1, 2, 3 (declining realistic retention)
cohort_retention = []
base_retention = {'M0': 100, 'M1': 0, 'M2': 0, 'M3': 0}
for month in sorted(users_df['cohort_month'].unique()):
    cohort_size = len(users_df[users_df['cohort_month'] == month])
    purchasers = int(cohort_size * (funnel['purchase']/funnel['view']))
    # realistic decaying retention with slight random noise
    m1 = max(0, np.random.normal(34, 4))
    m2 = max(0, m1 * np.random.uniform(0.55, 0.7))
    m3 = max(0, m2 * np.random.uniform(0.55, 0.75))
    cohort_retention.append({
        'cohort': month,
        'cohort_size': cohort_size,
        'purchasers': purchasers,
        'M0': 100.0,
        'M1': round(m1, 1),
        'M2': round(m2, 1),
        'M3': round(m3, 1)
    })

# ============================================================
# 4. A/B TEST SIMULATION: New checkout flow (B) vs old (A)
# ============================================================
n_a, n_b = 3000, 3000
true_rate_a = 0.42
true_rate_b = 0.475  # hypothesized improvement from simplified checkout

conv_a = np.random.binomial(1, true_rate_a, n_a)
conv_b = np.random.binomial(1, true_rate_b, n_b)

rate_a = conv_a.mean()
rate_b = conv_b.mean()

# Two-proportion z-test
count = np.array([conv_a.sum(), conv_b.sum()])
nobs = np.array([n_a, n_b])
p_pool = count.sum() / nobs.sum()
se = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
z = (rate_b - rate_a) / se
p_value = 2 * (1 - stats.norm.cdf(abs(z)))

lift = round((rate_b - rate_a) / rate_a * 100, 1)
significant = p_value < 0.05

ab_test = {
    'variant_a': {'name': 'Original Checkout', 'n': n_a, 'conversions': int(conv_a.sum()), 'rate': round(rate_a*100, 2)},
    'variant_b': {'name': 'Simplified Checkout', 'n': n_b, 'conversions': int(conv_b.sum()), 'rate': round(rate_b*100, 2)},
    'lift_pct': lift,
    'z_score': round(z, 2),
    'p_value': round(p_value, 4),
    'significant': bool(significant),
    'confidence_level': '95%'
}

# ============================================================
# SAVE ALL RESULTS
# ============================================================
results = {
    'funnel': funnel,
    'funnel_pct': funnel_pct,
    'drop_off': drop_off,
    'cohort_retention': cohort_retention,
    'ab_test': ab_test,
    'meta': {
        'total_users': N_USERS,
        'dataset_note': 'Synthetic dataset generated with realistic e-commerce conversion distributions'
    }
}

with open('/home/claude/funnel_project/results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(json.dumps(results, indent=2))
