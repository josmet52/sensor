# cDriver8x8.py
# -*- coding: utf-8 -*-

"""---------------------------------------------------------------------------- 

 class cDriver8x8.py
 --------------------
 
 driver to display texts and numbers on the Adafruit 8x8 leds display with Adafruit backpack
     - low case character are converted in upper case
     - special character are not accepted and generate errors
     - scroll speed is not changable
     - 
 v1.0 jan 2017
 J. Metrailler / joseph.metrailler@bluewin.ch

 call example :
 display8x8 = cDriver8x8()
 display8x8.display_scroll(vTxt, txtColor, scrollNonStop, txtSize)

 with  vTxt : the text to display. 
       optional txtColor : the color of the displayed text : 0=black, 1=green, 2=red, 3=orange
       optional scrollNonStop : when True the text restart at the begin when finished
       optional txtSize : 1 = small, 2 = medium (the best choice), 3 = big

       default values are :
       - txtColor = 1 (green)
       - scrollNonStop = True
       - txtSize = 2 (medium 6x4)

-----------------------------------------------------------------------------"""

import time
from Adafruit_LED_Backpack import BicolorMatrix8x8
    
# Digit value to bitmask mapping:
# the correspondance table in a dictionary
class cDriver8x8:

    def __init__(self):

        # char size 7x5 dots
        DIGIT_VALUES_7x5 = {
        ' ' : '000 000', 
        '%' : '064 050 008 038 001 000', 
        '+' : '008 008 062 008 008 000',
        '-' : '008 008 008 008 008 000',
        '.' : '064 000',
        ',' : '096 000',
        ':' : '034 000',
        ';' : '098 000',
        '!' : '095 000',
        '/' : '064 048 008 006 001 000',
        '\\' : '001 006 008 048 064 000',
        '<' : '008 020 034 065 000',
        '>' : '065 034 020 008 000',
        '^' : '016 008 004 008 016 000',
        '=' : '020 020 020 020 020 000',
        '0' : '062 065 065 065 062 000',
        '1' : '066 127 064 000',
        '2' : '066 097 081 073 070 000',
        '3' : '034 065 073 073 054 000',
        '4' : '008 012 010 127 008 000',
        '5' : '039 069 069 069 057 000',
        '6' : '062 073 073 073 050 000',
        '7' : '097 017 009 005 003 000',
        '8' : '054 073 073 073 054 000',
        '9' : '006 073 073 073 062 000',
        'A' : '124 010 009 010 124 000',
        'B' : '127 073 073 073 054 000',
        'C' : '062 065 065 065 034 000',
        'D' : '127 065 065 065 062 000',
        'E' : '127 073 073 073 065 000',
        'F' : '127 009 009 009 001 000',
        'G' : '062 065 081 081 050 000',
        'H' : '127 008 008 008 127 000',
        'I' : '065 127 065 000',
        'J' : '032 065 065 065 063 000',
        'K' : '127 008 020 034 065 000',
        'L' : '127 064 064 064 064 000',
        'M' : '127 002 004 002 127 000',
        'N' : '127 002 004 008 127 000',
        'O' : '127 065 065 065 127 000',
        'P' : '127 009 009 009 006 000',
        'Q' : '062 065 081 033 094 000',
        'R' : '127 009 025 041 070 000',
        'S' : '038 073 073 073 050 000',
        'T' : '001 001 127 001 001 000',
        'U' : '063 064 064 064 063 000',
        'V' : '007 024 096 024 007 000',
        'W' : '127 032 016 032 127 000',
        'X' : '099 020 008 020 099 000',
        'Y' : '001 002 124 002 001 000',
        'Z' : '097 081 073 069 067 000',
        }

        # char size 7x4 dots
        DIGIT_VALUES_7x4 = {
        ' ' : '000 000', 
        '%' : '064 050 008 038 001 000', 
        '+' : '008 008 062 008 008 000',
        '-' : '008 008 008 008 008 000',
        '.' : '064 000',
        ',' : '096 000',
        ':' : '034 000',
        ';' : '098 000',
        '!' : '095 000',
        '/' : '064 048 008 006 001 000',
        '\\' : '001 006 008 048 064 000',
        '<' : '008 020 034 065 000',
        '>' : '065 034 020 008 000',
        '^' : '016 008 004 008 016 000',
        '=' : '020 020 020 020 000',
        '0' : '062 065 065 062 000',
        '1' : '066 127 064 000',
        '2' : '098 081 073 070 000',
        '3' : '065 073 073 054 000',
        '4' : '008 012 010 127 008 000',
        '5' : '039 069 069 057 000',
        '6' : '062 073 073 050 000',
        '7' : '097 017 013 003 000',
        '8' : '054 073 073 054 000',
        '9' : '006 073 073 062 000',
        'A' : '126 009 009 126 000',
        'B' : '127 073 073 054 000',
        'C' : '062 065 065 034 000',
        'D' : '127 065 065 062 000',
        'E' : '127 073 073 065 000',
        'F' : '127 009 009 001 000',
        'G' : '062 065 081 050 000',
        'H' : '127 008 008 127 000',
        'I' : '065 127 065 000',
        'J' : '032 065 065 063 000',
        'K' : '127 020 034 065 000',
        'L' : '127 064 064 064 000',
        'M' : '127 002 004 002 127 000',
        'N' : '127 002 004 008 127 000',
        'O' : '127 065 065 127 000',
        'P' : '127 009 009 006 000',
        'Q' : '030 017 033 094 000',
        'R' : '127 025 041 070 000',
        'S' : '038 073 073 050 000',
        'T' : '001 001 127 001 001 000',
        'U' : '063 064 064 063 000',
        'V' : '007 024 096 024 007 000',
        'W' : '127 032 016 032 127 000',
        'X' : '099 020 008 020 099 000',
        'Y' : '003 004 120 004 003 000',
        'Z' : '097 089 069 067 000',
        }

        # char size 4x3 dots
        DIGIT_VALUES_4x3 = {
        ' ' : '000 000', 
        '%' : '009 004 018 000', 
        '+' : '004 012 004 000',
        '-' : '004 004 004 000',
        '.' : '016 000',
        ':' : '010 000',
        '!' : '023 000',
        '°' : '002 000',
        ',' : '016 008 000',
        '/' : '024 004 024 000',
        '>' : '017 010 004 000',
        '<' : '004 010 017 000',
        '^' : '004 002 004 000',
        '=' : '010 010 010 000',
        '0' : '014 017 014 000',
        '1' : '002 031 000',
        '2' : '018 025 022 000',
        '3' : '017 021 010 000',
        '4' : '007 004 030 000',
        '5' : '023 021 009 000',
        '6' : '014 021 012 000',
        '7' : '017 013 003 000',
        '8' : '014 021 014 000',
        '9' : '007 005 031 000',
        'A' : '031 005 031 000',
        'B' : '031 021 010 000',
        'C' : '014 017 017 000',
        'D' : '031 017 014 000',
        'E' : '031 021 017 000',
        'F' : '031 005 001 000',
        'G' : '014 021 025 000',
        'H' : '031 004 031 000',
        'I' : '031 000',
        'J' : '008 016 015 000',
        'K' : '031 012 019 000',
        'L' : '031 016 016 000',
        'M' : '031 002 031 000',
        'N' : '031 001 031 000',
        'O' : '031 017 031 000',
        'P' : '031 005 007 000',
        'Q' : '015 009 031 000',
        'R' : '031 013 023 000',
        'S' : '023 021 029 000',
        'T' : '001 031 001 000',
        'U' : '031 016 031 000',
        'V' : '007 024 007 000',
        'W' : '031 008 031 000',
        'X' : '027 004 027 000',
        'Y' : '003 028 003 000',
        'Z' : '025 021 019 000',
        }

        self.DV75 = DIGIT_VALUES_7x5 # the dictionary to use for big size char
        self.DV74 = DIGIT_VALUES_7x4 # the dictionary to use for big size char
        self.DV43 = DIGIT_VALUES_4x3 # the dictionary to use for small size char


    # function to call to display scroling text on the matrix
    
    def DisplayScroll(self, vTxt, txtColor=1, scrollNonStop=True, txtSize=2):

        vTxt = vTxt.upper() # lower case char are converted in upper case
##        for c in vTxt:
##            print(ord(c))
        
        # Create display instance on default I2C address (0x70) and bus number.
        display = BicolorMatrix8x8.BicolorMatrix8x8()
        display.begin()
        display.clear()
        display.write_display()
        
        nBlackCol = 8 # let the 7 first column black when stating a display scroll
#        nRow = 8 # 8x8 leds matrix

        vDisp=[[0,0,0,0,0,0,0,0]]*8
        
        # Prepare the display matrix
        for vChar in vTxt: # for each char in vTxtx
            
#            print(vChar,ord(vChar))
            
            if txtSize == 1:
                d = self.DV43[vChar].split()
            elif txtSize == 2:
                d = self.DV74[vChar].split()
            else :
                d = self.DV75[vChar].split()
                
            for iStr in d:
                
                b0=b1=b2=b3=b4=b5=b6=b7=0

                i=int(iStr)
                
                # codage du caractere
                if i&1 > 0: b0=txtColor # bit0
                    
                if i&2 <> 0: b1=txtColor # bit1
                    
                if i&4 <> 0: b2=txtColor # bit2
                    
                if i&8 <> 0: b3=txtColor # bit 3
                    
                if i&16 <> 0: b4=txtColor # bit 4
                    
                if i&32 <> 0: b5=txtColor # bit 5
                    
                if i&64 <> 0: b6=txtColor # bit 6
                    
                if i&128 <> 0: b7=txtColor # bit 7

                vDisp.append([b0,b1,b2,b3,b4,b5,b6,b7])
                
        for i in range(nBlackCol):
            vDisp.append([0,0,0,0,0,0,0,0])

        # for i,vData in enumerate(vDisp):
        #     print(vData)
        # print('')
        
        if not scrollNonStop:
            for i in range (len(vDisp)-nBlackCol):
                for d in range(i,i+nBlackCol):
                    for j,c in enumerate(vDisp[d]):
                        # print(i,d,j,c)
                        display.set_pixel(7-j,d-i,c)
                    display.write_display()
                    # print('')
                time.sleep(0.10)
        else:
            while True:
                for i in range (len(vDisp)-nBlackCol):
                    for d in range(i,i+nBlackCol):
                        for j,c in enumerate(vDisp[d]):
                            # print(i,d,j,c)
                            display.set_pixel(7-j,d-i,c)
                        display.write_display()
                        # print('')
                    time.sleep(0.10)
                     
            
        
    
                        
