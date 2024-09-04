def format_to_indian_currency(num):
    integer_part, _, decimal_part = str(num).partition('.')
    
    if len(integer_part) > 3:
        last_three = integer_part[-3:]
        other_numbers = integer_part[:-3]
        other_numbers = ','.join([other_numbers[max(i-2, 0):i] for i in range(len(other_numbers), 0, -2)][::-1])
        formatted_number = other_numbers + ',' + last_three
    else:
        formatted_number = integer_part

    if decimal_part:
        formatted_number += '.' + decimal_part
    
    return formatted_number


formatted_number = format_to_indian_currency(1221232)
print(formatted_number)
