import config
import jdatetime
async def qua(year, month, day, gender):
    # Example Jalali date (e.g., 1403-10-25)
    jalali_date = jdatetime.date(year, month, day)
    miladi_date = jalali_date.togregorian()
    year = miladi_date.year
    print(year)
    if year < 2000:
        if gender == "female":
            sum_year_two = int(str(year)[2]) + int(str(year)[3])
            print("first sum", sum_year_two)
            if len(str(sum_year_two)) == 2:
                sum_year_two = int(str(sum_year_two)[0]) + int(str(sum_year_two)[1])
                print("two sum", sum_year_two)
            if sum_year_two == 5:
                return 8
            sum_year_two += 5
            if len(str(sum_year_two)) == 2:
                sum_year_two = int(str(sum_year_two)[0]) + int(str(sum_year_two)[1])
            return sum_year_two
        else:
            sum_year_two = int(str(year)[2]) + int(str(year)[3])
            if len(str(sum_year_two)) == 2:
                sum_year_two = int(str(sum_year_two)[0]) + int(str(sum_year_two)[1])
            if sum_year_two == 5:
                return 2
            sum_year_two = 10 - sum_year_two
            return sum_year_two
    else:
        if gender == "female":
            sum_year_two = int(str(year)[2]) + int(str(year)[3])
            if len(str(sum_year_two)) == 2:
                sum_year_two = int(str(sum_year_two)[0]) + int(str(sum_year_two)[1])
            if sum_year_two == 5:
                return 8
            sum_year_two += 6
            if len(str(sum_year_two)) == 2:
                sum_year_two = int(str(sum_year_two)[0]) + int(str(sum_year_two)[1])
            if sum_year_two == 10:
                return 1
            return sum_year_two
        else:
            sum_year_two = int(str(year)[2]) + int(str(year)[3])
            if len(str(sum_year_two)) == 2:
                sum_year_two = int(str(sum_year_two)[0]) + int(str(sum_year_two)[1])
            if sum_year_two == 5:
                return 2
            sum_year_two = 9 - sum_year_two
            if sum_year_two == 0:
                return 9
            return sum_year_two
        

async def zoo(year, month, day):
    jalali_date = jdatetime.date(year, month, day)
    miladi_date = jalali_date.togregorian()
    year = miladi_date.year
    zoo_num = year % 12
    name = config.zoo[zoo_num]
    about = config.zoo_about[zoo_num]
    image = f"images/zoo/{zoo_num}.jpg"
    return name, about, image