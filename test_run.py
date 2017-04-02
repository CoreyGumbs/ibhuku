import string


url_name = ''.join('!~@#$%^&*()_Testmy-1977'.split())


def strip_url_name_punctuation(url_name):
    '''
    Strips any unauthorized punctuation from user input in the following steps:
    1. Makes unauthorized punctuation list of string.punctuation
    2. Removes any allowed punctuation from  unauthorized punctuation list.
    3. Creates translation map for removing any unauthorized punctuation.
    4. Returns translated string with removed unauthorized punctuation.
    '''
    punc_key = [punctuation for punctuation in string.punctuation]
    allowed_punc = [punc_key.remove(
        punc)for punc in punc_key if punc == '_' or punc == '-']
    translator = str.maketrans('', '', str(punc_key))
    return url_name.translate(translator)

new_url = strip_url_name_punctuation(url_name)


print(new_url)
