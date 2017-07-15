'''
USE CRONTAB TO MAKE THIS PIECE OF CODE RUN PERIODICALLY/WHENEVER YOU WANT
Steps:
1. Open terminal,
    crontab -e
    to add a line to file:
    */5 * * * * /usr/bin/python /Users/guess/Desktop/test.py
    this is to make it run every 5 min.

    For usage of crontab, check http://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html

2. Re-check if it's set correctly
    crontab -l
'''

#!/usr/bin/python
import requests
import os
from send_twitter import send_simple_twitter
from datetime import datetime

url = 'http://www.adidas.com/us/nmd_r1-shoes/BY9952.html'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

wanted_size = 6.5

'''
helping functions
'''
def check_size():
    result = requests.get(url, headers=headers)

    # save result to raw_data.txt
    f = open('/Users/guess/Desktop/raw_data.txt', 'w')
    print >> f, result.content

    # open raw_data.txt and search for special line that includes
    # size information, save the line to a list fisrt
    line_l = []
    f = open('/Users/guess/Desktop/raw_data.txt', 'r')
    for line in f:
        if "<ispagecontextset name=\"product_variations\"" in line:
             # print line
             line_l.append(line)
    f.close()
    os.remove('/Users/guess/Desktop/raw_data.txt')

    # process line_l, extract sizes out of list of strings
    available_sizes = []
    for i in line_l:
        for t in i.split("\""):
            try:
                available_sizes.append(float(t))
            except ValueError:
                pass

    # print available sizes
    print_avail_sizes = 'available sizes: ' + str(available_sizes)
    print(print_avail_sizes)

    return available_sizes


'''
main function
'''
def main():
    log = open('/Users/guess/Desktop/log.txt','a')
    log.write("\n-------------------------------------\n")
    log.write(str(datetime.now()))
    all_available_sizes = check_size()
    log.write(str(all_available_sizes))
    for i in all_available_sizes:
        if i == wanted_size:
            print("!!!!!!! WE GOT IT !!!!!!!")
            log.write("!!!!!!!")
            send_simple_twitter()
            break
    log.close()

if __name__ == "__main__":
  main()






