import zip_util
import math

def get_loc(codes):
    index = str(input("Enter a ZIP Code to lookup =>"))
    for code in codes:
        if code[0] == index:
            return f'ZIP Code {code[0]} is in {code[3]}, {code[4]}, {code[5]}, coordinates: {code[1]}, {code[2]}'
    return "ZIP Code not found"


def get_zip(codes):
    user_city = str(input("Enter a city name to lookup =>")).lower().title()
    user_state = str(input("Enter the state name to lookup =>")).upper()
    result = f'The following ZIP Code(s) found for {user_city}, {user_state}: '
    for code in codes:
        if code[3] == user_city and code[4] == user_state:
            result += code[0] + ', '
    return result


def calculate_dist(point1, point2):
    # pi - число pi, rad - радиус сферы (Земли)
    rad = 6372795

    # координаты двух точек
    llat1 = point1[0]
    llong1 = point1[1]

    llat2 = point2[0]
    llong2 = point2[1]

    # в радианах
    lat1 = llat1 * math.pi / 180.
    lat2 = llat2 * math.pi / 180.
    long1 = llong1 * math.pi / 180.
    long2 = llong2 * math.pi / 180.

    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисления длины большого круга
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    dist = ad * rad
    dist_miles = dist * 0.000621371
    return dist_miles


def get_dist(codes):
    zip1 = str(input("Enter the first ZIP Code =>"))
    zip2 = str(input("Enter the second ZIP Code =>"))
    zip1_list = []
    zip2_list = []
    for code in codes:
        if code[0] == zip1 and len(zip1_list) == 0:
            zip1_list = code[0]
        if code[0] == zip2 and len(zip2_list) == 0:
            zip2_list = code[0]
    if len(zip1_list) > 0 and len(zip2_list) > 0:
        point1 = [float(zip1_list[1]), float(zip1_list[2])]
        point2 = [float(zip2_list[1]), float(zip2_list[2])]
        print(type(zip1_list[1]))
        dist = calculate_dist(point1, point2)
        return f"The distance between {zip1} and {zip2} is {dist} miles"
    if len(zip1_list) == 0:
        return "ZIP Code 1 not found"
    if len(zip2_list) == 0:
        return "ZIP Code 2 not found"


def program(codes):
    while True:
        command = str(input("Command ('loc', 'zip', 'dist', 'end') =>"))
        if command.lower() == 'loc':
            print(get_loc(codes))
        if command.lower() == 'zip':
            print(get_zip(codes))
        if command.lower() == 'dist':
            print(get_dist(codes))
        if command.lower() == 'end':
            break



if __name__ == '__main__':
    zip_codes = zip_util.read_zip_all()
    program(zip_codes)