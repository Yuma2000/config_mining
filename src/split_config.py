"""
Split config into blocks and replace each word with a number.
"""
import glob

data_directory = "/home/takeda/config/data/"


def split_file(config_file_name) -> list:
    """
    Split config into blocks.
    """
    blocklist = []
    with open(config_file_name, 'r') as f:
        lineslist = f.readlines()

    nextBlock = False  # 次のブロックであるかの判定
    for data in lineslist:
        if data == '\n':  # 空行はとばす
            continue
        if '!' in data:  # ！でブロック分け
            nextBlock = True
            continue
        # !がdataに入ってなかったら
        if nextBlock:
            blocklist.append(data)
        else:
            blocklist[len(blocklist)-1] += data
        nextBlock = False

    return blocklist


def word2num(block_num, block, word_dict, word_count, file_name, file_count):
    words = block.split()
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
    output_file = data_directory + 'block_onlyNum/' + str(file_count) + '-' + file_name + '-' + str(block_num) + '.txt'
    with open(output_file, 'w') as f:
        f.write(config)
    print(words)
    print(block)
    return word_count


def main():
    config_files = glob.glob(data_directory + 'config_masked/*')
    word_dict = {}  # dictionary to store word-number mapping
    word_count = 1
    file_count = 1
    for config_file_name in config_files:
        blocklist = split_file(config_file_name)

        file_name = config_file_name[39:-11]
        for block_num, block in enumerate(blocklist):
            word_count = word2num(block_num, block, word_dict, word_count, file_name, file_count)
            file_count += 1


if __name__ == '__main__':
    main()
