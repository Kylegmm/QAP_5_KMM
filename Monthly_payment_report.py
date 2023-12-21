#This code is to give a detailed policy listing report for one stop insurance
#created by Kyle March-Maccuish
#completed 2023-12-18

# Function to calculate insurance premium for a policy
from datetime import date


def calculate_premium(first_car_premium, discount_rate, num_additional_cars):
    return first_car_premium + (num_additional_cars * first_car_premium * discount_rate)

# Function to calculate extra costs for a policy
def calculate_extra_costs(liability_option, glass_option, loaner_option, cost_liability, cost_glass, cost_loaner):
    extra_costs = 0
    if liability_option == 'Y':
        extra_costs += cost_liability
    if glass_option == 'Y':
        extra_costs += cost_glass
    if loaner_option == 'Y':
        extra_costs += cost_loaner
    return extra_costs

def generate_monthly_payment_listing():
    # Read data from OSICDef.dat
    with open('OSICDef.dat', 'r') as def_file:
        data = def_file.readlines()
        _, _, _, _, _, _, _, hst_rate, processing_fee = map(float, data)

    # Read data from Policies.dat
    with open('Policies.dat', 'r') as policies_file:
        policies = policies_file.readlines()

    monthly_payment_listing = []
    total_premium_exception = 0
    total_hst = 0
    total_monthly_payment = 0

    for policy in policies:
        policy_data = policy.strip().split(', ')
        payment_option, down_payment = policy_data[-2:]

        if payment_option == 'Monthly' or payment_option == 'Down Pay':
            first_car_premium = float(data[0])
            discount_rate = float(data[1])
            cost_liability = float(data[2])
            cost_glass = float(data[3])
            cost_loaner = float(data[4])

            insurance_premium = calculate_premium(first_car_premium, discount_rate, int(policy_data[8]) - 1)
            extra_costs = calculate_extra_costs(policy_data[9], policy_data[10], policy_data[11], cost_liability, cost_glass, cost_loaner)
            total_premium = insurance_premium + extra_costs
            hst = total_premium * hst_rate
            total_cost = total_premium + hst

            if payment_option == 'Down Pay':
                total_cost -= float(down_payment)

            monthly_payment = (total_cost + processing_fee) / 12 if payment_option == 'Down Pay' else (total_cost + processing_fee) / 12 - float(down_payment) / 12

            monthly_payment_listing.append((policy_data[0], f"{policy_data[3]}, {policy_data[2]}", f"${total_premium:.2f}", f"${hst:.2f}", f"${total_cost:.2f}", f"${down_payment:.2f}", f"${monthly_payment:.2f}"))
            total_premium_exception += total_premium
            total_hst += hst
            total_monthly_payment += monthly_payment

    # Generate monthly payment exception report
    print("ONE STOP INSURANCE COMPANY")
    print(f"MONTHLY PAYMENT LISTING AS OF {date}")
    print("POLICY CUSTOMER TOTAL TOTAL DOWN MONTHLY")
    print("NUMBER NAME PREMIUM HST COST PAYMENT PAYMENT")
    print("=" * 80)
    for payment in monthly_payment_listing:
        print("{:<10} {:<25} {:<12} {:<9} {:<9} {:<9} {:<9}".format(*payment))
    print("=" * 80)
    print(f"Total policies: {len(monthly_payment_listing)} ${total_premium_exception:.2f} ${total_hst:.2f} ${total_premium_exception + total_hst:.2f} ${total_monthly_payment:.2f}")

if __name__ == "__main__":
    generate_monthly_payment_listing()
