#!/usr/bin/env python3
NAME = 'Simple Hasher'
VERSION = 0.1
AUTHOR = 'RadicalEd'
LICENSE = 'Whatever'
BANNER = """
  sSSs   .S   .S_SsS_S.    .S_sSSs    S.        sSSs         .S    S.    .S_SSSs      sSSs   .S    S.     sSSs   .S_sSSs    
 d%%SP  .SS  .SS~S*S~SS.  .SS~YS%%b   SS.      d%%SP        .SS    SS.  .SS~SSSSS    d%%SP  .SS    SS.   d%%SP  .SS~YS%%b   
d%S'    S%S  S%S `Y' S%S  S%S   `S%b  S%S     d%S'          S%S    S%S  S%S   SSSS  d%S'    S%S    S%S  d%S'    S%S   `S%b  
S%|     S%S  S%S     S%S  S%S    S%S  S%S     S%S           S%S    S%S  S%S    S%S  S%|     S%S    S%S  S%S     S%S    S%S  
S&S     S&S  S%S     S%S  S%S    d*S  S&S     S&S           S%S SSSS%S  S%S SSSS%S  S&S     S%S SSSS%S  S&S     S%S    d*S  
Y&Ss    S&S  S&S     S&S  S&S   .S*S  S&S     S&S_Ss        S&S  SSS&S  S&S  SSS%S  Y&Ss    S&S  SSS&S  S&S_Ss  S&S   .S*S  
`S&&S   S&S  S&S     S&S  S&S_sdSSS   S&S     S&S~SP        S&S    S&S  S&S    S&S  `S&&S   S&S    S&S  S&S~SP  S&S_sdSSS   
  `S*S  S&S  S&S     S&S  S&S~YSSY    S&S     S&S           S&S    S&S  S&S    S&S    `S*S  S&S    S&S  S&S     S&S~YSY%b   
   l*S  S*S  S*S     S*S  S*S         S*b     S*b           S*S    S*S  S*S    S&S     l*S  S*S    S*S  S*b     S*S   `S%b  
  .S*P  S*S  S*S     S*S  S*S         S*S.    S*S.          S*S    S*S  S*S    S*S    .S*P  S*S    S*S  S*S.    S*S    S%S  
sSS*S   S*S  S*S     S*S  S*S          SSSbs   SSSbs        S*S    S*S  S*S    S*S  sSS*S   S*S    S*S   SSSbs  S*S    S&S  
YSS'    S*S  SSS     S*S  S*S           YSSP    YSSP        SSS    S*S  SSS    S*S  YSS'    SSS    S*S    YSSP  S*S    SSS  
        SP           SP   SP                                       SP          SP                  SP           SP          
        Y            Y    Y                                        Y           Y                   Y            Y           
"""
################################################
# Imports

from PIL import Image
import numpy as np
import argparse
import sys

# End of Imports
################################################
# Args

parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    usage='%(prog)s [options] <image_file>',
    description='Calculates an Image Hash for Fingerprinting, Using a Greyscale Average Hash Algorithm. (aHash Algorithm)'
)
parser.add_argument('image', type=str, help='The Image To Process')
parser.add_argument('-b', '--blocksize', type=int, help='How Big of a Block to Calculate Hash from. The Default is 8 which would use an 8x8 block and produce a 64bit hash (8 * 8 = 64)', required=False, default=8)
parser.add_argument('-s', '--string', action=argparse.BooleanOptionalAction, help='Output Hash as A String of 1s and 0s Instead of the default Integer')

args = parser.parse_args()

# End of Args
################################################
# Functions

def calculate_hash (block_size, image_file):
	# Open Image file
	image = Image.open(image_file)
	 
	# Resize Image
	small_img = image.resize((block_size, block_size), Image.NEAREST)

	# Convert to Numpy Array
	image_array = np.array(small_img)

	# Ignore Numpy Overflow Warnings
	np.seterr(over='ignore')

	# Calculate Average Grey while storing Greys
	greys = []
	for d in image_array:
		for p in d:
			grey = round(( p[0] + p[1] + p[2] ) / 3)
			greys.append(grey)
	average_grey = round(sum(greys) / len(greys))

	# Calculate Hash From Greys vs Average Grey
	bit_array = []
	for g in greys:
		if (g < average_grey):
			bit_array.append(1)
		else:
			bit_array.append(0)

	return bit_array

def bit_shift(bit_array):
	# Much Faster than Int Casting (~5x)
	out = 0
	for bit in bit_array:
		out = (out << 1) | bit
	return out

def int_cast(bit_array):
	# Int Casting, not as fast as bit shifting
	return int(''.join(list(map(str, bit_array))), 2)

def int_to_bit_array(integer):
	return [int(x) for x in '{:08b}'.format(integer)]

def array_as_string(arr):
	return ''.join(list(map(str, arr)))

def test_data_conversion(bit_array):
	# Show Original Bit Array as String
	print(array_as_string(bit_array))
	# Convert to Integer
	hash_int = bit_shift(bit_array)
	# Convert Integer back to Bit Array
	hash_out = int_to_bit_aray(hash_int)
	# Show New Array for Comparison
	print(array_as_string(hash_out))

# End of Functions
################################################
# Execution

	# Hash Image
bit_array = calculate_hash(args.blocksize, args.image)

	# Print Hash to User
if (args.string):
	print(array_as_string(bit_array))
else:
	print(int_cast(bit_array))

# End of Execution
################################################
