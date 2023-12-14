import time

PESEL_LENGTH = 11
PESEL_WEIGHT = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)

months_with_31_days = [1, 3, 5, 7, 8, 10, 12]
months_with_30_days = [4, 6, 9, 11]



# counters
total = correct = male = female = 0
invalid_length = invalid_digit = invalid_date = invalid_checksum = 0

file = open("1e6.dat", 'r')

start = time.time()

# main processing loop
for pesel in file:
    pesel = pesel.strip()
    total += 1
    is_correct = True

    if len(pesel) != PESEL_LENGTH:
        invalid_length += 1
        continue
    else:
        for character in pesel:
            if not character.isdigit():
                invalid_digit += 1
                is_correct = False
                break
    if is_correct:
        YY = int(pesel[0:2])
        MM = int(pesel[2:4])
        DD = int(pesel[4:6])
        month = MM % 20

        # the day of the birth cannot be "00"
        if DD == 0:
            invalid_date += 1
            continue

        # there is no month less than one and bigger than twelve
        elif not (0 < month < 13):
            invalid_date += 1
            continue

        # January, March, May, July, August, October and December have 31 days
        elif month in months_with_31_days:
            if DD > 31:
                invalid_date += 1
                continue

        # April, June, September and November have only 30 days
        elif month in months_with_30_days:
            if DD > 30:
                invalid_date += 1
                continue

        # checking if there is no leap year
        elif YY % 4 != 00 or (YY == 00 and (MM - MM % 20) != 20):
            if month == 2 and DD > 28:
                invalid_date += 1
                continue

        # checking if there is leap year
        elif YY % 4 == 0 or (YY == 0 and (MM - MM % 20) == 20):
            if month == 2 and DD > 29:
                invalid_date += 1
                continue

        checksum = 0

        for i in range(PESEL_LENGTH - 1):
            checksum += PESEL_WEIGHT[i] * int(pesel[i])

        checksum = (10 - (checksum % 10)) % 10

        if checksum != int(pesel[10]):
            invalid_checksum += 1
            continue

        else:
            correct += 1

            if int(pesel[9]) % 2 == 0:
                female += 1
            else:
                male += 1

file.close()

# show results
print(total, correct, female, male)
print(invalid_length, invalid_digit, invalid_date, invalid_checksum)
print("Runtime [s]= ", time.time()-start)
