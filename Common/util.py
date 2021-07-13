def swap(l,index1,index2):
        '''
        swap the two given index element in the list and return the index2
        :param l:
        :param index1:
        :param index2:
        :return: index2
        '''
        l[index1],l[index2] = l[index2],l[index1]
        return index2

def bubble_down(drivers, index):
    '''
    helper function for the heap sort of drivers
    :param drivers:
    :param index:
    :return:
    '''
    left_child_index = index * 2 + 1
    right_child_index = index * 2 + 2
    if left_child_index < len(drivers):
        if right_child_index < len(drivers):
            if drivers[index].distance > drivers[left_child_index].distance \
                    or drivers[index].distance > drivers[right_child_index].distance:
                index = swap(drivers, index, left_child_index) \
                    if drivers[left_child_index].distance < drivers[right_child_index].distance \
                    else swap(drivers, index, right_child_index)
                bubble_down(drivers, index)
        else:
            if drivers[index].distance > drivers[left_child_index].distance:
                index = swap(drivers, index, left_child_index)
                bubble_down(drivers, index)
