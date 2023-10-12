from utils.googleSheetLib import GoogleSheetClient

def price_in_range(inv_price, dealer_price):
    if dealer_price and not inv_price <= dealer_price:
        return False
    return True

def matching_reg_number(inv_reg_number, dealer_reg_number):
    return inv_reg_number.startswith(dealer_reg_number)

def matching_dealer_reqs(inv_list, dealer_requests, exclude_scrap=False, only_scrap=False):
    matching_values = []

    for request in dealer_requests:
        req_car_name = request[1]
        try:
            dealer_price = request[9]
        except IndexError :
            dealer_price = None
        dealer_reg_number = request[6]

        for item in inv_list:
            inv_car_name = item[1]
            inv_price = item[9]
            inv_reg_number = item[6]
            inv_car_insurance = item[7]
            inv_car_model = item[2]
            inv_car_owners = item[4]

            if req_car_name == inv_car_name and price_in_range(inv_price, dealer_price) and matching_reg_number(inv_reg_number, dealer_reg_number):
                matching_values.append([inv_car_name, inv_car_model, inv_car_owners, inv_car_insurance, inv_reg_number, inv_price])
                break
    print(matching_values)
    return matching_values



def main():
    google_sheet = GoogleSheetClient("1V0Y1gm2tTHfLdS3J-KWOJCnVrWvnoL_INz4fBummo74")
    inventory_list = google_sheet.read_values("Inventory", "A2:K")
    if not inventory_list:
        print("No values found")
        exit(1)

    # result = google_sheet.update_values("Inventory", "A4:B5", [['A', 'B'], ['C', 'D']])

    dealer_sheet = GoogleSheetClient("1LP0q3jNpao1PWl_7D6kPwIXvtICEV1fpZ_ezP0EGWMY")
    dealer_reqs = dealer_sheet.read_values("DealerRequirements", "A2:J")
    if not dealer_reqs:
        print("No values found")
        exit(1)
    dealer_sheet.clear_values_in_range("Matches", "A2:F")

    matched_values = matching_dealer_reqs(dealer_requests=dealer_reqs, inv_list=inventory_list)

    dealer_sheet.update_values("Matches", "A2:F", matched_values)

    # matched_values = matching_dealer_reqs(dealer_requests=dealer_reqs, inv_list=inventory_list, exclude_scrape=False)
    # matched_values = matching_dealer_reqs(inventory_list, dealer_reqs)
    # matched_values = matching_dealer_reqs(inventory_list, dealer_reqs, False)

if __name__ == '__main__':
     main()
