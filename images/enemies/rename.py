import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Current working directory:", os.getcwd())

for n in range(20):
    file_num = '00' + str(n)
    file_num = file_num[-3:]
    os.rename(f'3_enemies_1_walk_{file_num}.png', f'{n}.png')


