class Hello:
    def hello():
        a = 10
        print(Hello)

# ******************************************************************************************
# $$$$$$$$$$$$$$$$ # program 01 Comment out print  $$$$$$$$$$$$$$$$$$

# // Type - 01


"""with open("comment.txt", "r") as fp:
    for line in fp:
        line = line.strip()

        if line.startswith("/*"):
            print("\nMultiline Comment:")
            print(line)
            for line in fp:
                print(line.strip())
                if line.strip().endswith("*/"):
                    break
        elif line.startswith("//"):
            print("\nSingleline Comment:")
            print(line.strip())

"""

# // Type - 02

# with open("comment.txt", "r") as file:
#     lines = file.readlines()
#     comment = False
#     for line in lines:
#         line = line.strip()
#         if line.startswith("//"):
#             print("\nSingle line Comment:")
#             print(line)
#         elif line.startswith("/*"):
#             comment = True
#             print("\nMulti line Comment:")
#             print(line)
#         elif line.endswith("*/") and comment:
#             comment = False
#             print(line)
#         elif line.startswith("#"):
#             print("\nSingle line Comment:")
#             print(line)
#         elif line.startswith('"""') or line.startswith("'''"):
#             if not comment:
#                 comment = True
#                 print("\nMultiline Comment:")
#                 print(line)
#             else:
#                 comment = False
#         elif '"""' in line or "'''" in line:
#             if not comment:
#                 comment = True
#                 print("\nMultiline Comment:")
#                 print(line)
#             else:
#                 comment = False
#         elif comment:
#             print(line)


# ///////////////////// Text File Content ////////////////
# File name : comment.txt
'''
this is text file
//one-line comment
another line
another line

/*multi
line
comment*/
last line


"""
essay, an analytic, interpretative, or critical literary composition usually much shorter and less systematic and formal than a dissertation or thesis and usually dealing with its subject from a limited and often personal point of view."""


'''


# ******************************************************************************************
# $$$$$$$$$$$$$$$$ # program 02 Count digit , Char, Symbole  $$$$$$$$$$$$$$$$$$

"""
str = input("Enter a string: ")
digits, vowels, consonants, symbols = 0, 0, 0, 0

for char in str:
    if char.isdigit():
        digits += 1
    elif char.isalpha():
        if char in "aeiouAEIOU":
            vowels += 1
        else:
            consonants += 1
    else:
        symbols += 1

print("Digits:", digits)
print("Vowels:", vowels)
print("Consonants:", consonants)
print("Symbols:", symbols)

"""

# ******************************************************************************************
# $$$$$$$$$$$$$$$$ # program 03 End od "ab"  $$$$$$$$$$$$$$$$$$


# *********************************************************
# $$$$$$$$$$$$$ Type 1 $$$$$$$$$$$$$$$$$$$$$

# Note : End With all char --> "ab"

"""
str = input("Enter the string: ")
state = 0

for char in str:
    if state == 0:
        if char == 'a':
            state = 1
        elif char == 'b':
            state = 0
        else:
            state = -1
    elif state == 1:
        if char == 'b':
            state = 2
        elif char == 'a':
            state = 1
        else:
            state = -1
    elif state == 2:
        if char == 'a':
            state = 1
        elif char == 'b':
            state = 0
        else:
            state = -1
    elif state == -1:
        if char == 'a':
            state = 1
        elif char == 'b':
            state = 0
        else:
            state = -1

if state == 2:
    print("\nString is valid.")
else:
    print("\nString is invalid.")

"""
# *********************************************************
# $$$$$$$$$$$$$ Type 2 $$$$$$$$$$$$$$$$$$$$$
# Note : End With all char --> "ab"
"""
str = input("Enter the string: ")
state = 0

for char in str:
    switcher = {
        0: {'a': 1, 'b': 0, 'default': -1},
        1: {'a': 1, 'b': 2, 'default': -1},
        2: {'a': 1, 'b': 0, 'default': -1},
        -1: {'a': 1, 'b': 0, 'default': -1}
    }
    state = switcher.get(state, switcher[-1]) \
        .get(char, switcher[state]['default'])

if state == 2:
    print("\nString is valid.")
else:
    print("\nString is invalid.")
"""

# ******************************************************************************************
# $$$$$$$$$$$$$$$$ # program 04 Number Automata  $$$$$$$$$$$$$$$$$$

"""
# // https://cs.nyu.edu/~gottlieb/courses/2000s/2007-08-fall/compilers/lectures/diagrams/trans-dia-num.png
MAX_STR_LEN = 20

str = input("Enter the string: ")

state = 0

for i in range(len(str)-1):
    if state == -1:
        break

    if state == 0:
        if str[i].isdigit():
            state = 1
        else:
            state = -1
    elif state == 1:
        if str[i].isdigit():
            state = 1
        elif str[i] == '.':
            state = 2
        elif str[i] == 'e':
            state = 4
        else:
            state = -1
    elif state == 2:
        if str[i].isdigit():
            state = 3
        else:
            state = -1
    elif state == 3:
        if str[i].isdigit():
            state = 3
        elif str[i] == 'e':
            state = 4
        else:
            state = -1
    elif state == 4:
        if str[i].isdigit():
            state = 6
        elif str[i] == '+' or str[i] == '-':
            state = 5
        else:
            state = -1
    elif state == 5:
        if str[i].isdigit():
            state = 6
        else:
            state = -1
    elif state == 6:
        if str[i].isdigit():
            state = 6
        else:
            state = -1

if state != -1:
    print("\nNumber is valid.")
else:
    print("\nInvalid number.")
"""

# ******************************************************************************************
# $$$$$$$$$$$$$$$$ # program 05 Validation Of password  $$$$$$$$$$$$$$$$$$

"""
import string
MAX_USERNAME_LEN = 16
MAX_PASSWORD_LEN = 16

username = input("Enter username: ")
password = input("Enter password: ")

checku = checkl = checkn = checks = 0

if len(password) >= 8 and len(password) <= 16:
    for ch in password:
        if ch.isupper():
            checku = 1
        if ch.islower():
            checkl = 1
        if ch.isdigit():
            checkn = 1
        if ch in string.punctuation:
            checks = 1

if checkl == 1 and checku == 1 and checkn == 1 and checks == 1:
    print("\nPassword accepted.")
else:
    print("\nPassword does not match all criterias.")
"""


# ******************************************************************************************
# $$$$$$$$$$$$$$$$ # program 06 Lexical Analyzer  $$$$$$$$$$$$$$$$$$

"""
import re

# Define the token patterns using regular expressions
TOKENS = [
    ('NUMBER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'/'),
]

# Define a function that takes a string of code and returns a list of tokens


def lex(code):
    # Create an empty list to store the tokens
    tokens = []
    # Remove any whitespace from the code
    code = code.strip()
    # Keep looping until the code is empty
    while code:
        # Check each token pattern in turn
        for token_name, token_pattern in TOKENS:
            # Try to match the pattern at the start of the code
            match = re.match(token_pattern, code)
            if match:
                # If there is a match, add the token to the list
                token = (token_name, match.group(0))
                tokens.append(token)
                # Remove the matched code from the start of the string
                code = code[len(match.group(0)):].strip()
                # Break out of the loop and try again
                break
        else:
            # If none of the token patterns match, raise an error
            raise ValueError(f'Invalid syntax: {code}')
    # Return the list of tokens
    return tokens


code = '3 + 4 * 2 - 1 / 5'

tokens = lex(code)
print(tokens)
# Output: [('NUMBER', '3'), ('PLUS', '+'), ('NUMBER', '4'), ('MULTIPLY', '*'), ('NUMBER', '2'), ('MINUS', '-'), ('NUMBER', '1'), ('DIVIDE', '/'), ('NUMBER', '5')]
"""

# $$$$$$$$$$$$$$$$$$$$$$$$$$ C Language Program $$$$$$$$$$$$$$$$$$$$$$$$$$

# ******************************************************************************************
# $$$$$$$$$$$$$$$$ # program 01 Comment $$$$$$$$$$$$$$$$$$
# 01
"""
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    FILE *fp = fopen("comment.txt", "r");
    if (fp == NULL)
    {
        printf("Error opening file %s\n", argv[1]);
        return 1;
    }

    int c;
    while ((c = fgetc(fp)) != EOF)
    {
        if (c == '/')
        {
            c = fgetc(fp);
            if (c == '*')
            {
                printf("\nMultiline Comment:\n");

                c = fgetc(fp);
                while (c != EOF)
                {
                    printf("%c", c);
                    if (c == '*')
                    {
                        c = fgetc(fp);
                        if (c == '/')
                        {
                            printf("%c\b\b  ", c);
                            break;
                        }
                    }
                    else
                    {
                        c = fgetc(fp);
                    }
                }
            }
            else if (c == '/')
            {
                printf("\nSingleline Comment:\n");

                c = fgetc(fp);
                while (c != EOF && c != '\n')
                {
                    printf("%c", c);
                    c = fgetc(fp);
                }
                printf("\n");
            }
        }
    }

    fclose(fp);
    
    printf("\n");
    system("pause");
    return 0;
}

"""


# ******************************************************************************************
# $$$$$$$$$$$$$$$$ # program 02 Count  $$$$$$$$$$$$$$$$$$

"""
#include <stdio.h>
#include <ctype.h>

#define MAX_STRING_LEN 100

int main()
{
    char str[MAX_STRING_LEN + 1];
    int digits = 0, vowels = 0, consonants = 0, symbols = 0;

    printf("Enter a string: ");
    fgets(str, MAX_STRING_LEN, stdin);


    for (int i = 0; str[i] != '\0'; i++)
    {
        if (isdigit(str[i]))
        {
            digits++;
        }
        else if (isalpha(str[i]))
        {
            if (str[i] == 'a' || str[i] == 'e' || str[i] == 'i' || str[i] == 'o' || str[i] == 'u' ||
                str[i] == 'A' || str[i] == 'E' || str[i] == 'I' || str[i] == 'O' || str[i] == 'U')
            {
                vowels++;
            }
            else
            {
                consonants++;
            }
        }
        else
        {
            symbols++;
        }
    }

    printf("Digits: %d\n", digits);
    printf("Vowels: %d\n", vowels);
    printf("Consonants: %d\n", consonants);
    printf("Symbols: %d\n", symbols);

    return 0;
}

"""

# ******************************************************************************************
# $$$$$$$$$$$$$$$$ # program 03 End with ab  $$$$$$$$$$$$$$$$$$
"""
#include <stdio.h>
#include <string.h>

#define MAX_STR_LEN 100

int main()
{
    char str[MAX_STR_LEN + 1];
    int state = 0;

    printf("Enter the string: ");
    fgets(str, MAX_STR_LEN, stdin);

    for (int i=0; i < strlen(str)-1; i++)
    {
        switch (state)
        {
        case 0:
            if (str[i] == 'a')
            {
                state = 1;
            }
            else if (str[i] == 'b')
            {
                state = 0;
            }
            else {
                state = -1;
            }
            break;
        case 1:
            if (str[i] == 'b')
            {
                state = 2;
            }
            else if (str[i] == 'a')
            {
                state = 1;
            }
            else
            {
                state = -1;
            }
            break;
        case 2:
            if (str[i] == 'a')
            {
                state = 1;
            }
            else if (str[i] == 'b')
            {
                state = 0;
            }
            else
            {
                state = -1;
            }
            break;
        case -1:
            if (str[i] == 'a')
            {
                state = 1;
            }
            else if (str[i] == 'b')
            {
                state = 0;
            }
            else
            {
                state = -1;
            }
            break;
        
        default:
            break;
        }
    }

    if (state == 2)
    {
        printf("\nString is valid.");
    }
    else
    {
        printf("\nString is invalid.");
    }

    return 0;
}

"""

# ******************************************************************************************
# $$$$$$$$$$$$$$$$ # program 04 Number Automata  $$$$$$$$$$$$$$$$$$

"""
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    FILE *fp = fopen("code.txt", "r");
    char buffer[100]; int ind = 0;
    if (fp == NULL)
    {
        printf("Error opening file %s\n", argv[1]);
        return 1;
    }

    char ch;
    while (ch != EOF)
    {
        ch = fgetc(fp);
        if (ch != EOF)
        {
            buffer[ind++] = ch;
        }
    }

    int prev_char = 0, print_iden = 0, loop = 0;
    char iden[32];
    for (int ind = 0; buffer[ind] != '\0'; ind++)
    {
        if (print_iden == 1)
        {
            printf(" is an identifier.\n");
            loop = 0;
            print_iden = 0;
            prev_char = 0;
        }

        //keywords
        if (buffer[ind] == 'n' && buffer[ind+1] == 'u' && buffer[ind+2] == 'm' && buffer[ind+3] == ' ')
        {
            printf("num keyword encountered.\n");
        }

        //operators
        else if (buffer[ind] == '+' || buffer[ind] == '-' || buffer[ind] == '*' || (buffer[ind-1] != '/' && buffer[ind] == '/' && buffer[ind+1] != '/') || buffer[ind] == '=' || buffer[ind] == '%')
        {
            printf("%c operator encountered.\n", buffer[ind]);
        }

        //; = end of statement
        else if (buffer[ind] == ';')
        {
            printf("; encountered -> end of statement.\n\n");
        }

        //comment
        else if (buffer[ind] == '/' && buffer[ind+1] == '/')
        {
            char tbuff[100];
            int tind = 0;
            for (int j = ind; buffer[j] != '\n'; j++)
            {
                tbuff[tind] = buffer[j];
                tind++;
            }
            tbuff[strlen(tbuff)-1] = '\0';
            printf("'%s' is comment.\n", tbuff);
            int occur = 0;
            for (int j = ind; j < strlen(buffer); j++)
            {
                if (buffer[j] == '\n')
                {
                    occur++;
                }
                if (occur == 1)
                {
                    occur = j;
                    break;
                }
            }
            ind = occur;
            print_iden = 0;
            prev_char = 0;
        }
        
        //identifier
        else if (isalpha(buffer[ind]))
        {
            int temp = ind;
            if (temp > 1)
            {
                if (buffer[temp-1] == ' ' || buffer[temp-1] == '\n' || prev_char == 1)
                {
                    while (temp <= strlen(buffer) && (buffer[temp] != '\0' && buffer[temp] != ' ' && buffer[temp] != ';'))
                    {
                        printf("%c", buffer[temp]);
                        iden[loop] = buffer[temp];

                        if ((buffer[temp+1] == ' ' || buffer[temp+1] == ';') && buffer[temp+1] != '\0')
                        {
                            print_iden = 1;
                        }
                        
                        prev_char = 1;
                        temp++;
                    }
                }
            }
        }
    }

    return 0;
}

"""

# ******************************************************************************************
# $$$$$$$$$$$$$$$$ # program 04 Number Automata  $$$$$$$$$$$$$$$$$$


"""
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX_STR_LEN 20

int main()
{
    char str[MAX_STR_LEN + 1];
    int state = 0;

    printf("Enter the string: ");
    fgets(str, MAX_STR_LEN, stdin);

    for (int i=0; i < strlen(str)-1; i++)
    {
        if (state == -1)
        {
            break;
        }
        
        switch (state)
        {
        case 0: // after start
            if (isdigit(str[i]))
            {
                state = 1;
            }
            else {
                state = -1;
            }
            break;
        case 1: // after digit
            if (isdigit(str[i]))
            {
                state = 1;
            }
            else if (str[i] == '.')
            {
                state = 2;
            }
            else if (str[i] == 'e')
            {
                state = 4;
            }
            else {
                state = -1;
            }
            break;
        case 2: // after .
            if (isdigit(str[i]))
            {
                state = 3;
            }
            else {
                state = -1;
            }
            break;
        case 3: // after digit
            if (isdigit(str[i]))
            {
                state = 3;
            }
            else if (str[i] == 'e')
            {
                state = 4;
            }
            else {
                state = -1;
            }
            break;
        case 4: // after e
            if (isdigit(str[i]))
            {
                state = 6;
            }
            else if (str[i] == '+' || str[i] == '-')
            {
                state = 5;
            }
            else {
                state = -1;
            }
            break;
        case 5: // after + or -
            if (isdigit(str[i]))
            {
                state = 6;
            }
            else {
                state = -1;
            }
            break;
        case 6: // after digit
            if (isdigit(str[i]))
            {
                state = 6;
            }
            else {
                state = -1;
            }
            break;
        
        case -1: // dead state
            state = -1;
            break;
        
        default:
            break;
        }
    }

    if (state != -1)
    {
        printf("\nNumber is valid.");
    }
    else
    {
        printf("\nInvalid number.");
    }

    return 0;
}

// https://cs.nyu.edu/~gottlieb/courses/2000s/2007-08-fall/compilers/lectures/diagrams/trans-dia-num.png



"""


# ******************************************************************************************
# $$$$$$$$$$$$$$$$ # program 05 Validation  $$$$$$$$$$$$$$$$$$

"""
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX_USERNAME_LEN 16
#define MAX_PASSWORD_LEN 16

int main()
{
    char username[MAX_USERNAME_LEN + 1];
    char password[MAX_PASSWORD_LEN + 1];

    printf("Enter username: ");
    scanf("%s", &username);

    printf("Enter password: ");
    scanf("%s", &password);

    int checku = 0, checkl = 0, checkn = 0, checks = 0;
    if (strlen(password) >= 8 && strlen(password) <= 16)
    {
        for (int i=0; i < strlen(password); i++)
        {
            if (isupper(password[i]))
            {
                checku = 1;
            }
            if (islower(password[i]))
            {
                checkl = 1;
            }
            if (isdigit(password[i]))
            {
                checkn = 1;
            }
            if (password[i] == '!' || password[i] == '%' || password[i] == '&' || password[i] == '@' || password[i] == '#'
            || password[i] == '$' || password[i] == '^' || password[i] == '*' || password[i] == '?' || password[i] == '_' || password[i] == '~')
            {
                checks = 1;
            }
        }
    }

    if (checkl == 1 && checku == 1 && checkn == 1 && checks == 1)
    {
        printf("\nPassword accepted.\n");
    }
    else
    {
        printf("\nPassword does not match all criterias.\n");
    }

    return 0;
}

"""


# ******************************************************************************************
# $$$$$$$$$$$$$$$$ # program 06 Lexical Analyzer  $$$$$$$$$$$$$$$$$$

"""
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    FILE *fp = fopen("code.txt", "r");
    char buffer[100]; int ind = 0;
    if (fp == NULL)
    {
        printf("Error opening file %s\n", argv[1]);
        return 1;
    }

    char ch;
    while (ch != EOF)
    {
        ch = fgetc(fp);
        if (ch != EOF)
        {
            buffer[ind++] = ch;
        }
    }

    int prev_char = 0, print_iden = 0, loop = 0;
    char iden[32];
    for (int ind = 0; buffer[ind] != '\0'; ind++)
    {
        if (print_iden == 1)
        {
            printf(" is an identifier.\n");
            loop = 0;
            print_iden = 0;
            prev_char = 0;
        }

        //keywords
        if (buffer[ind] == 'n' && buffer[ind+1] == 'u' && buffer[ind+2] == 'm' && buffer[ind+3] == ' ')
        {
            printf("num keyword encountered.\n");
        }

        //operators
        else if (buffer[ind] == '+' || buffer[ind] == '-' || buffer[ind] == '*' || (buffer[ind-1] != '/' && buffer[ind] == '/' && buffer[ind+1] != '/') || buffer[ind] == '=' || buffer[ind] == '%')
        {
            printf("%c operator encountered.\n", buffer[ind]);
        }

        //; = end of statement
        else if (buffer[ind] == ';')
        {
            printf("; encountered -> end of statement.\n\n");
        }

        //comment
        else if (buffer[ind] == '/' && buffer[ind+1] == '/')
        {
            char tbuff[100];
            int tind = 0;
            for (int j = ind; buffer[j] != '\n'; j++)
            {
                tbuff[tind] = buffer[j];
                tind++;
            }
            tbuff[strlen(tbuff)-1] = '\0';
            printf("'%s' is comment.\n", tbuff);
            int occur = 0;
            for (int j = ind; j < strlen(buffer); j++)
            {
                if (buffer[j] == '\n')
                {
                    occur++;
                }
                if (occur == 1)
                {
                    occur = j;
                    break;
                }
            }
            ind = occur;
            print_iden = 0;
            prev_char = 0;
        }
        
        //identifier
        else if (isalpha(buffer[ind]))
        {
            int temp = ind;
            if (temp > 1)
            {
                if (buffer[temp-1] == ' ' || buffer[temp-1] == '\n' || prev_char == 1)
                {
                    while (temp <= strlen(buffer) && (buffer[temp] != '\0' && buffer[temp] != ' ' && buffer[temp] != ';'))
                    {
                        printf("%c", buffer[temp]);
                        iden[loop] = buffer[temp];

                        if ((buffer[temp+1] == ' ' || buffer[temp+1] == ';') && buffer[temp+1] != '\0')
                        {
                            print_iden = 1;
                        }
                        
                        prev_char = 1;
                        temp++;
                    }
                }
            }
        }
    }

    return 0;
}

"""


# Answers to asked Questions to A division

"""

# Identify the number
state = 1
string = input("Enter any string:-")
for i in string:
    print(state)
    if(state == 1):
        if (i.isdigit() ):
            state = 2
        else: 
            state = 0
    elif (state == 2):
        if (i == '.'):
            state = 3
        elif(i.isdigit()):
            state = 2
        elif (i == 'E'):
            state = 5
        else :
            state = 0
    elif (state == 3):
        if (i.isdigit()):
            state = 4
        elif (i == 'E'):
            state = 5
        else:
            state = 0
    elif  (state == 4):
        if(i.isdigit()):
            state = 4
        elif( i == 'E'):
            state = 5
        else:
            state = 0
    elif (state == 5):
        if(i == '+' or i == '-'):
            state = 6
        elif(i.isdigit()):
            state = 7
        else:
            state = 0
    elif (state == 6):
        if (i.isdigit()):
            state = 7
        else:
            state = 0
    elif(state == 7):
        if (i.isdigit()):
            state = 7
        else:
            state = 0
print(f'\nFinal state is {state}')

if (state ==  2 or state == 4 or state == 7 ):
    print("Number is accepted")
    







# $1 + $2 = $3
state = 1
file = open("xyz.txt",'r')
content = file.readlines()
print(content)
for lines in content:
    for char in lines:
        if (state == 1):
            if(char == '$'):
                state = 2
            else:
                state = 10
        if (state == 2):
            if(char == '$'):
                state = 2
            elif(char.isdigit() or char.isalpha()):
                state = 3
            else:
                state = 1
        if(state == 3):
            if(char.isdigit() or char.isalpha()):
                state = 3
            else:
                state = 4
                print("identifier identified")
        if(state == 4):
            if(char == '$'):
                state = 2
            else:
                state = 1
        if(state == 10):
            state=1
            
            
            

# Identify keyword int
comment
number
identifier

# code to accept "INT"
state = 1
file = open('xyz.txt', 'r')
content = file.readlines()
print(content)
for words in content:
    for char in words:
        if (state == 1):
            if (char == 'i'):
                state = 2
            else:
                state = 10
        elif (state == 2):
            if (char == 'n'):
                state = 3
            else:
                state = 10
        elif (state == 3):
            if (char == 't'):
                state = 4
            else:
                state = 10
        elif (state == 4):
            if (char.isalpha() or char.isdigit()):
                state = 10
            else:
                state = 5
                print('INT identified')

        elif (state == 5):
            state = 1
        print(state)
        
"""
