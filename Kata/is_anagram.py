def is_anagram(message1, message2):
    return sorted(message1.replace(' ', '')) == sorted(message2.replace(' ', ''))
    #druga ver  return sorted(message1) == sorted(message2)
    #return set(message1) == set(message2) #<-- to jest to samo co niżej
    # for char in message2:
    #     if char not in message1:
    #         return False
    # for char in message1:
    #     if char not in message2:
    #         return False
    # return True
