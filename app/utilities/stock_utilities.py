def calculate_revenue_growth(revenues):
    growth_rates = []
    for i in range(1, len(revenues)):
        growth_rate = (revenues[i] - revenues[i - 1]) / revenues[i - 1]
        growth_rates.append(growth_rate)
    return growth_rates