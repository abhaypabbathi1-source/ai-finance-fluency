def calculate_interest(amount,rate):
    return amount * rate 

result = calculate_interest(10000, 0.055)
print(result)

def calculate_interest(amount, rate=0.055):
    return amount * rate

print(calculate_interest(10000)) # uses default rate
print(calculate_interest(10000, 0.08)) #overrides it

def loan_category (amount):
    if amount > 15000:
        return "large loan"
    else:
        return "standard loan"
    
loan_amounts = [10000, 25000, 5000, 15000]
for amount in loan_amounts:
    category = loan_category(amount)
    print( f"{amount}:{category}")

def loan_summary(amount,rate=0.055):
    interest = calculate_interest(amount,rate)
    category = loan_category(amount)
    return f"Loan {amount} ({category}): interest owed: {interest}"

for amount in loan_amounts:
    print(loan_summary(amount))






    print(calculate_interest(10000))
    print(loan_category(amount))

def broken_function(amount):
    total = amount * 2

#notice: no return statement here

result = broken_function(10000)
print(result)  

