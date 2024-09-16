# -*- coding: utf-8 -*-

# pip install Pillow

# Chapter 1: The Gatekeeper

from PIL import Image
import time


def modify_image(file_path):
    '''Chapter 1: Convert Image and Calculate Red Pixel Values'''
    try:
        # Generate the number
        current_time = int(time.time())
        generated_number = (current_time % 100) + 50
        if generated_number % 2 == 0:
            generated_number += 10

        # Open an image and modify it
        img = Image.open(file_path)
        img = img.convert('RGB')  # Ensure it's in RGB format
        pixels = img.load()

        # Modify the pixels
        for i in range(img.width):
            for j in range(img.height):
                r, g, b = pixels[i, j]
                pixels[i, j] = ((r + generated_number) % 256,
                                (g + generated_number) % 256,
                                (b + generated_number) % 256)

        # Save the new image
        img.save('C:\\Users\\synth\\OneDrive\\Documents\\HIT137\\chapter1out.png')

        # Calculate the sum of the red pixel values
        red_sum = sum(pixels[i, j][0] for i in range(img.width) for j in range(img.height))
        return red_sum
    except IOError:
        print("Error: The file could not be opened or found.")
    except Exception as exc:
        print(f"An error occurred: {exc}")

    return 0


# Chapter 2: The Chamber of Strings
def process_string(long_str):
    '''Chapter 2: Separate Even number and strings and convert them to ASCII Values'''
    if len(long_str) < 16:
        raise ValueError("String must be at least 16 characters long")

    # Separate numbers and letters
    number_string = ''.join(filter(str.isdigit, long_str))
    print("Number String: " + number_string)

    letter_string = ''.join(filter(str.isalpha, long_str))
    print("Letter String: " + letter_string + "\n")

    # Separate Even Numbers and Convert to their ASCII values
    even_num_string = ""
    ascii_numbers = []
    for num in number_string:
        if int(num) % 2 == 0:
            even_num_string += num + " "
            ascii_numbers += [str(ord(num))]

    print("Even Numbers: " + even_num_string)
    print("ASCII Values of Even Numbers: " + str(ascii_numbers) + "\n")

    # Separate Upper-case letters and Convert to their ASCII values
    upper_string = ""
    ascii_upper = []
    for letter in letter_string:
        if letter.isupper():
            upper_string += letter + " "
            ascii_upper += [str(ord(letter))]

    print("Upper Case Letters: " + upper_string)
    print("ASCII Values of Upper Case Letters: " + str(ascii_upper) + "\n")
    ascii_uppercase = [str(ord(char)) for char in letter_string if char.isupper()]

    return ascii_numbers + ascii_uppercase


# Chapter 3: Decrypting a Cryptogram
def decipher_cryptogram(text, shift):
    '''Decrypt the cryptogram and find the original quote and shift value'''
    if not text.strip():  # Check if text is not empty or just whitespace
        raise ValueError("Text must not be empty")

    shift = shift % 26  # Normalize shift to handle larger numbers

    decrypted_text = []
    for char in text:
        if char.isalpha():  # Only decrypt alphabetical characters
            shifted = ord(char) - shift
            if char.isupper():
                if shifted < ord('A'):
                    shifted += 26
            elif shifted < ord('a'):
                shifted += 26
            decrypted_text.append(chr(shifted))
        else:
            decrypted_text.append(char)  # Non-alphabetic characters are not changed
    return ''.join(decrypted_text)


def main():
    '''Main function'''
    # Chapter 1: Example for Chapter1.jpg
    print("Chapter 1:")
    red_pixel_sum = modify_image('C:\\Users\\synth\\OneDrive\\Documents\\HIT137\\chapter1.jpg')
    print(red_pixel_sum)

    # Chapter 2: Example for Separating Upper-case letters and Converting to their ASCII values
    print("\nChapter 2:")
    try:
        input_string = "56aAww1984sktr235270aYmn145ss785fsq31D0"
        result = process_string(input_string)
        print("The Combined Result: " + str(result))
    except Exception as e:
        print(e)

    # Chapter 3: Decrypt the given cryptogram and Find out the original quote with the shift key
    print("\nChapter 3:")
    try:
        cipher_text = "VZ FRYSVFU VZCNGVRAG NAQ N YVGGYR VAFRPHER V ZNXR ZVFGNXRF V NZ BHG BS PBAGEBY NAQ NG GVZRF UNEQ GB UNAQYR OHG VS LBH PNAG UNAQYR ZR NG ZL JBEFG GURA LBH FHER NF URYY QBAG QRFREIR ZR NG ZL ORFG ZNEVYLA ZBAEBR"

        # Trying different shifts
        for shift in range(26):
            decrypted_message = decipher_cryptogram(cipher_text, shift)
            print(f"Shift {shift}: {decrypted_message}")
        print("")
        print("From the result, we have found that the Shift Key is 13\n")
        decrypted_text = decipher_cryptogram(cipher_text, 13)
        print("Original Quote is: " + decrypted_text)
    except Exception as exp:
        print(exp)


# Driver code
if __name__ == '__main__':
    # Example of The Quest for the Hidden Treasure
    main()
