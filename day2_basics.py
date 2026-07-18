# A variable is like a named cell
loan_amount = 10000    # int - like a number in a cell
interest_rate = 0.055 # float - like a percentage cell
borrower_name = "Alex" # string - like a text cell
is_default = False   # boolean - like a true/false cell

print (loan_amount)
print (borrower_name)
loan_amounts = [10000, 25000, 5000, 15000]
print(loan_amounts[0])  # first item - Excel would call this row 1
print(len(loan_amounts)) # how many items - like COUNT ()
print(sum(loan_amounts)) # like SUM()

loan = {
    "borrower": "Alex",
    "amount": 10000,
    "rate": 0.055,
    "defaulted": False
}
print(loan["amount"])
print(loan["borrower"])

loan_amounts = [10000, 25000, 5000, 15000]
for amount in loan_amounts:
    interest = amount *0.055
    print(f"Loan {amount}, interest owed: {interest}")

for amount in loan_amounts:
    if amount > 15000:
        print(f"{amount}: large loan")
    else:
        print(f"{amount}: standard loan")