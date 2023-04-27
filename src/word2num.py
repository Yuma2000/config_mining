# read the configuration file
with open('../data/as1border1_replaced.cfg', 'r') as f:
    config = f.read()

# split the configuration file into words
words = config.split()

# create a dictionary to store word-number mapping
word_dict = {}

# initialize the word counter to 1
word_count = 1

# loop through the words and replace them with numbers
for i, word in enumerate(words):
    # check if the word has already been assigned a number
    if word in word_dict:
        # if so, replace the word with the corresponding number
        words[i] = str(word_dict[word])
    else:
        # if not, assign a new number to the word and update the dictionary
        words[i] = str(word_count)
        word_dict[word] = word_count
        word_count += 1

# join the words back into a string
config = ' '.join(words)

# write the updated configuration file
with open('../data/config_updated.txt', 'w') as f:
    f.write(config)

# print the word-number mapping dictionary
print(word_dict)
