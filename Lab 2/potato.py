# Print 2 blank lines
print()
print()

# Part I of this lab is using input statements and arithmetic expressions

# Ask the user to input hours and hourly rate
# Complete or correct the following input statements

# NOTE:  both input items WILL be used in MATH calculations
#        the user may enter number WITH decimal places for hours and rate
#        complete the input statements and
#        use type conversion to allow this type input

hours = float(input("Enter the hours worked: "))

rate = float(input("Enter your hourly rate: "))

# Write an equation to compute gross pay using the variables above
# The gross pay calculation is hours multiplied by rate
# The overtime should be ONLY the hours OVER 40 hours * rate * 1.5
# You may assume hours will be AT LEAST 40 hours
    
grossPay = hours * rate
overtimePay = (hours - 40) * rate * 1.5

# Print 1 blank line in your output 
print()

# Print out hours, rate, gross pay and overtime pay
# Notice the capital 'P' in grossPay and overtimePay variable names
# See the sample output for a recommendation on how to display items

print("Hours =", hours)
print("Rate = ", rate)
print("Gross Pay = ", grossPay)
print("Overtime Pay = ", overtimePay)