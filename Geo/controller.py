from Geo import DBhelper

def find_zone(long,lati):
    '''

    :param long:
    :param lati:
    :return: if the location is valid, return the corresponding zone otherwise return -1
    '''
    if long < 0 or lati < 0 or long > 90 or lati > 90:
        return -1
    return  (long)//10 + (lati)//10*10

def get_search_zones(long,lati,distance,zone):
    '''
    judge whether needs to search the drivers in the neighbour zones, if so put the zone into res
    :param long:
    :param lati:
    :param distance:
    :param zone:
    :return: A list of zones to search for nearby drivers
    '''
    res = []
    res.append(zone)
    over_right = False
    over_left = False
    over_up = False
    over_down = False
    if find_zone(long,lati+distance) != zone and find_zone(long,lati+distance) != -1:
        over_up = True
        res.append(find_zone(long,lati+distance))
    if find_zone(long,lati-distance) != zone and find_zone(long,lati-distance) != -1:
        over_down = True
        res.append(find_zone(long,lati-distance))
    if find_zone(long+distance,lati) != zone and find_zone(long+distance,lati) != -1:
        over_right = True
        res.append(find_zone(long+distance,lati))
    if find_zone(long-distance,lati) != zone and find_zone(long-distance,lati) != -1:
        over_left = True
        res.append(find_zone(long-distance,lati))
    if over_left and over_up:
        res.append(zone+9)
    if over_right and over_up:
        res.append(zone+11)
    if over_down and over_left:
        res.append(zone-11)
    if over_down and over_right:
        res.append(zone-9)
    return res

def sort_nearest_drivers(drivers):
    '''
    sort the drivers according to their distance to the pickup location and return the top 10 drivers_id
    :param drivers
    :return: the top 10 drivers_id
    '''
    def swap(l,index1,index2):
        l[index1],l[index2] = l[index2],l[index1]
        return index2
    def bubble_down(drivers,index):
        left_child_index = index*2+1
        right_child_index = index*2+2
        if left_child_index < len(drivers):
            if right_child_index < len(drivers):
                if drivers[index].distance > drivers[left_child_index].distance\
                or drivers[index].distance > drivers[right_child_index].distance:
                    index = swap(drivers,index,left_child_index) \
                    if drivers[left_child_index].distance < drivers[right_child_index].distance\
                        else swap(drivers,index,right_child_index)
                    bubble_down(drivers,index)
            else:
                if drivers[index].distance > drivers[left_child_index].distance:
                    index = swap(drivers, index, left_child_index)
                    bubble_down(drivers, index)
    for index in range((len(drivers)-2)//2,-1,-1):
        bubble_down(drivers,index)
    return drivers[0:10]

def find_nearest_drivers(pickup_location,distance=4):
    drivers = []
    longitude = pickup_location[0]
    latitude = pickup_location[1]
    zone_of_pickup_location = find_zone(longitude,latitude)
    search_zones = get_search_zones(longitude,latitude,distance,zone_of_pickup_location)
    nearby_drivers = DBhelper.get_nearby_drivers(longitude,latitude,distance,search_zones)
    sorted_drivers = sort_nearest_drivers(nearby_drivers)
    return sorted_drivers
