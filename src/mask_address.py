"""
コンフィグファイルをマスクする．
IP address -> #, MAC address -> *
"""
import re
import glob

raw_configs = glob.glob('../data/raw_config/*')

for raw_config in raw_configs:
    with open(raw_config, 'r') as f:
        config = f.read()

    # replace IP addresses with '#'
    config = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '#', config)

    # replace MAC addresses with '*'
    config = re.sub(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', '*', config)

    file_name = raw_config[19:-4]
    masked_file = '../data/config_masked/' + file_name + '_masked.cfg'
    with open(masked_file, 'w') as f:
        f.write(config)
