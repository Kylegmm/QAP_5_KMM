#This code is to give a detailed policy listing report for one stop insurance
#created by Kyle March-Maccuish
#completed 2023-12-18

# Function to calculate insurance premium for a policy
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

def generate_policy_listing():
    # Read data from OSICDef.dat
    with open('OSICDef.dat', 'r') as def_file:
        data = def_file.readlines()
        first_car_premium = float(data[0])
        discount_rate = float(data[1])
        cost_liability = float(data[2])
        cost_glass = float(data[3])
        cost_loaner = float(data[4])

    # Read data from Policies.dat
    with open('Policies.dat', 'r') as policies_file:
        policies = policies_file.readlines()

    policy_listing = []
    total_policies = 0
    total_insurance = 0
    total_extra_costs = 0

    for policy in policies:
        policy_data = policy.strip().split(', ')
        policy_number, date, first_name, last_name, address, city, province, postal_code, phone, cars, \
        liability_option, glass_option, loaner_option, _, _ = policy_data

        # Calculate insurance premium
        cars = int(cars)
        insurance_premium = calculate_premium(first_car_premium, discount_rate, cars - 1)

        # Calculate extra costs
        extra_costs = calculate_extra_costs(liability_option, glass_option, loaner_option, cost_liability, cost_glass, cost_loaner)

        # Calculate total premium
        total_premium = insurance_premium + extra_costs

        # Add to the report
        policy_listing.append((policy_number, f"{last_name}, {first_name}", date, f"${insurance_premium:.2f}", f"${extra_costs:.2f}", f"${total_premium:.2f}"))

        # Increment totals
        total_policies += 1
        total_insurance += insurance_premium
        total_extra_costs += extra_costs

    # Generate detailed policy listing report
    print("ONE STOP INSURANCE COMPANY")
    print(f"POLICY LISTING AS OF {date}")
    print("POLICY CUSTOMER POLICY INSURANCE EXTRA TOTAL")
    print("NUMBER NAME DATE PREMIUM COSTS PREMIUM")
    print("=" * 80)
    for policy in policy_listing:
        print("{:<10} {:<25} {:<12} {:<9} {:<9} {:<9}".format(*policy))
    print("=" * 80)
    print(f"Total policies: {total_policies} ${total_insurance:.2f} ${total_extra_costs:.2f} ${(total_insurance + total_extra_costs):.2f}")

if __name__ == "__main__":
    generate_policy_listing()
