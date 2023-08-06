ETW={
    'A':'Q',
    'B':'W',
    'C':'E',
    'D':'R',
    'E':'T',
    'F':'Z',
    'G':'U',
    'H':'I',
    'I':'O',
    'J':'A',
    'K':'S',
    'L':'D',
    'M':'F',
    'N':'G',
    'O':'H',
    'P':'J',
    'Q':'K',
    'R':'P',
    'S':'Y',
    'T':'X',
    'U':'C',
    'V':'V',
    'W':'B',
    'X':'N',
    'Y':'M',
    'Z':'L'
}
NTOA={
    0:'A',
    1:'B',
    2:'C',
    3:'D',
    4:'E',
    5:'F',
    6:'G',
    7:'H',
    8:'I',
    9:'J',
    10:'K',
    11:'L',
    12:'M',
    13:'N',
    14:'O',
    15:'P',
    16:'Q',
    17:'R',
    18:'S',
    19:'T',
    20:'U',
    21:'V',
    22:'W',
    23:'X',
    24:'Y',
    25:'Z'
}
ATON={
    'A':0,
    'B':1,
    'C':2,
    'D':3,
    'E':4,
    'F':5,
    'G':6,
    'H':7,
    'I':8,
    'J':9,
    'K':10,
    'L':11,
    'M':12,
    'N':13,
    'O':14,
    'P':15,
    'Q':16,
    'R':17,
    'S':18,
    'T':19,
    'U':20,
    'V':21,
    'W':22,
    'X':23,
    'Y':24,
    'Z':25
}
W1=[
    'J',
    'G',
    'D',
    'Q',
    'O',
    'X',
    'U',
    'S',
    'C',
    'A',
    'M',
    'I',
    'F',
    'R',
    'V',
    'T',
    'P',
    'N',
    'E',
    'W',
    'K',
    'B',
    'L',
    'Z',
    'Y',
    'H'
]
W2=[
    'N',
    'T',
    'Z',
    'P',
    'S',
    'F',
    'B',
    'O',
    'K',
    'M',
    'W',
    'R',
    'C',
    'J',
    'D',
    'I',
    'V',
    'L',
    'A',
    'E',
    'Y',
    'U',
    'X',
    'H',
    'G',
    'Q'
]

W3=[
    'J',
    'V',
    'I',
    'U',
    'B',
    'H',
    'T',
    'C',
    'D',
    'Y',
    'A',
    'K',
    'E',
    'Q',
    'Z',
    'P',
    'O',
    'S',
    'G',
    'X',
    'N',
    'R',
    'M',
    'W',
    'F',
    'L'
]
R={
    'A':'Q',
    'B':'Y',
    'C':'H',
    'D':'O',
    'E':'G',
    'F':'N',
    'G':'E',
    'H':'C',
    'I':'V',
    'J':'P',
    'K':'U',
    'L':'Z',
    'M':'T',
    'N':'F',
    'O':'D',
    'P':'J',
    'Q':'A',
    'R':'X',
    'S':'W',
    'T':'M',
    'U':'K',
    'V':'I',
    'W':'S',
    'X':'R',
    'Y':'B',
    'Z':'L'
}

class EnigmaMachine:
    def __init__(self, w1n, w2n, w3n):
        """
            Initialize an Enigma machine with specified starting positions.

            Parameters
            ----------
            w1n : int
                Starting position of the first wheel.
            w2n : int
                Starting position of the second wheel.
            w3n : int
                Starting position of the third wheel.
            """
        self.wheel1 = W1[w1n:] + W1[:w1n]
        self.wheel2 = W2[w2n:] + W2[:w2n]
        self.wheel3 = W3[w3n:] + W3[:w3n]

    def rotate_wheels(self):
        """
            Rotate the wheels of the Enigma machine.
            """
        self.wheel1 = self.wheel1[1:] + self.wheel1[:1]
        if self.wheel2.index('R') == 0:
            self.wheel2 = self.wheel2[1:] + self.wheel2[:1]
            self.wheel3 = self.wheel3[1:] + self.wheel3[:1]
        elif self.wheel3.index('F') == 0:
            self.wheel2 = self.wheel2[1:] + self.wheel2[:1]

    def encrypt_char(self, char):
        """
            Encrypt a single character using the Enigma machine.

            Parameters
            ----------
            char : str
                The character to be encrypted.

            Returns
            -------
            str
                The encrypted character.
        """
        temp = R[self.wheel3[ATON[self.wheel2[ATON[self.wheel1[ATON[ETW[char]]]]]]]]
        temp2 = self._find_key_by_value(ETW, NTOA[self.wheel1.index(NTOA[self.wheel2.index(NTOA[self.wheel3.index(temp)])])])
        self.rotate_wheels()
        return temp2

    def encrypt_message(self, message):
        """
            Encrypt a message using the Enigma machine.

            Parameters
            ----------
            message : str
                The message to be encrypted.

            Returns
            -------
            str
                The encrypted message.
        """
        encrypted = ""
        for char in message:
            if char.isalpha():
                encrypted += self.encrypt_char(char.upper())
            else:
                encrypted += char
        return encrypted

    def _find_key_by_value(self, dictionary, value):
        """
           Find a key in a dictionary based on its value.

           Parameters
           ----------
           dictionary : dict
               The dictionary to search for the key.
           value : any
               The value to find the corresponding key for.

           Returns
           -------
           any
               The key corresponding to the provided value.
        """
        for key, val in dictionary.items():
            if val == value:
                return key
        return None