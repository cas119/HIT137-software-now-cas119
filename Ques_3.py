'''Question 3 - Solved By Hussein Salami & Synthia Islam'''


def find_key():
    '''Find Key Function'''
    total = 0
    for i in range(5):
        for j in range(3):
            if i+j == 5:
                total += i + j
            else:
                total -= i - j

    counter = 0
    while counter < 5:
        if total < 13:
            total += 1
        elif total > 13:
            total -= 1
        else:
            counter += 2

    print("\nKey: " + str(total))
    return total


def decrypt(encrypted_text, key):
    '''decrypt method'''
    decrypted_text = ""
    for char in encrypted_text:
        if char.isalpha():  # Check if the character is alphabetical
            shifted = ord(char) - key
            if char.islower():  # Wrap around for lowercase letters
                if shifted < ord('a'):
                    shifted += 26
            elif char.isupper():  # Wrap around for uppercase letters
                if shifted < ord('A'):
                    shifted += 26
            decrypted_text += chr(shifted)
        else:
            decrypted_text += char  # Non-alphabetic characters are unchanged
    return decrypted_text


def main():
    '''Main function'''
    # Example encrypted code and a hypothetical key
    key = find_key()

    encrypted_code = """
    tybony_inevnoyr = 100
    zl_qvpg = {'xrl1': 'inyhr1', 'xrl2': 'inyhr2', 'xrl3': 'inyhr3'}

    qrs cebprff_ahzoref():
        tybony tybony_inevnoyr
        ybpny_inevnoyr = 5
        ahzoref = [1, 2, 3, 4, 5]

        juvyr ybpny_inevnoyr > 0:
            vs ybpny_inevnoyr % 2 == 0:
                ahzoref.erzbir(ybpny_inevnoyr)
            ybpny_inevnoyr -= 1

        erghea ahzoref

    zl_frg = {1, 2, 3, 4, 5, 5, 4, 3, 2, 1}
    erfhyg = cebprff_ahzoref(ahzoref=zl_frg)

    qrs zbqvsl_qvpg():
        ybpny_inevnoyr = 10
        zl_qvpg['xrl4'] = ybpny_inevnoyr

    zbqvsl_qvpg(5)

    qrs hcqngr_tybony():
        tybony tybony_inevnoyr
        tybony_inevnoyr += 10

    sbe v va enatr(5):
        cevag(v)
        v += 1

    vs zl_frg vf abg Abar naq zl_qvpg['xrl4'] == 10:
        cevag("Pbaqvgvba zrg!")

    vs 5 abg va zl_qvpg:
        cevag("5 abg sbhaq va gur qvpgvbanel!")

    cevag(tybony_inevnoyr)
    cevag(zl_qvpg)
    cevag(zl_frg)
    """

    # Decrypt the code
    original_code = decrypt(encrypted_code, key)
    print("Decrypted Original Code:")
    print("---------------")
    print(original_code)
    print("\nCorrected Code With Comments:")
    print("-------------------------------")


# Driver code
if __name__ == '__main__':
    # Encryption-decryption Code
    main()


# Correct the Errors and Provide the Comments in the Original Code
global_variable = 100
my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}


def process_numbers(numbers):  # Added 'numbers' as a parameter
    '''process_numbers function'''  # Added Function Docstring
    # Removed global definition of global_variable as there is no use of it
    # global global_variable
    local_variable = 5
    # Removed initialization of 'numbers' as we have used it as a parameter
    # numbers = [1, 2, 3, 4, 5]

    while local_variable > 0:
        if local_variable % 2 == 0:
            numbers.remove(local_variable)
        local_variable -= 1

    return numbers


# Sets automatically remove duplicates, initial set defined with duplicates unnecessarily
# my_set = {1, 2, 3, 4, 5, 5, 4, 3, 2, 1}
my_set = {1, 2, 3, 4, 5}
result = process_numbers(numbers=my_set)


def modify_dict():
    '''Method of Modifying Dictionary'''  # Added Method Docstring
    local_variable = 10
    my_dict['key4'] = local_variable


modify_dict()  # Removed the erroneous parameter


def update_global():
    '''Method of Updating Global variable'''  # Added Method Docstring
    global global_variable
    global_variable += 10


update_global()  # Correctly call the function to update global variable


for i in range(5):
    print(i)
    # Incrementing 'i' inside the loop has no effect due to the nature of Python loops, so removing it
    # i += 1

if my_set is not None and my_dict['key4'] == 10:
    print("Condition met!")

if 5 not in my_dict:
    print("5 not found in the dictionary!")

print(global_variable)
print(my_dict)
print(my_set)


# After Decryption, the below code is original code
#     global_variable = 100
#     my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

#     def process_numbers():
#         '''process_numbers function'''
#         global global_variable
#         local_variable = 5
#         numbers = [1, 2, 3, 4, 5]

#         while local_variable > 0:
#             if local_variable % 2 == 0:
#                 numbers.remove(local_variable)
#             local_variable -= 1

#         return numbers

#     my_set = {1, 2, 3, 4, 5, 5, 4, 3, 2, 1}
#     result = process_numbers(numbers=my_set)

#     def modify_dict():
#         local_variable = 10
#         my_dict['key4'] = local_variable

#     modify_dict(5)

#     def update_global():
#         global global_variable
#         global_variable += 10

#     for i in range(5):
#         print(i)
#         i += 1

#     if my_set is not None and my_dict['key4'] == 10:
#         print("Condition met!")

#     if 5 not in my_dict:
#         print("5 not found in the dictionary!")

#     print(global_variable)
#     print(my_dict)
#     print(my_set)
