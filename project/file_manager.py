# file = open('youtube.txt', 'w')

# try:
#     file.write("Welcome to project file")
# finally:
#     file.close()

with open('test.txt','w') as file:
    file.write("Hello new file open method")