def find_word_replace_sentence(list1, list2, sentence,prompt):

    # Find the index of the first word in list1 that matches the given prompt
    for i, word in enumerate(list1):
        if word in prompt:
            index = i
            break
    else:
        # If no word in list1 matches the given prompt, return the original sentence
        return sentence

    # Use the index to get the word from list2
    word_to_replace = list2[index]

    # Replace any instance of "[mask]" in the sentence with the word from list2
    new_sentence = sentence.replace("[mask]", word_to_replace)

    # Return the modified sentence
    return new_sentence

list1 = ["are", "am", "were" , "was","were"]
list2 = ["are", "are", "was","were","were"]
sentence = "You [mask] doing nothing"
prompt = "What were i doing"
new_sentence = find_word_replace_sentence(list1, list2, sentence,prompt)

print(new_sentence)
