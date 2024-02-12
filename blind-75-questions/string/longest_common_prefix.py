def longest_common_prefix(texts):
    pref = ""
    smallest_text_length = min(len(text) for text in texts)
    for i in range(smallest_text_length):
        curr_char = texts[0][i]
        for text in texts[1:]:
            if text[i] != curr_char:
                return pref
        pref += curr_char
    return pref


x = ["flower","flow","flight"]

print(longest_common_prefix(x))

