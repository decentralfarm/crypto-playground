import os
import time
import stake_axs

minutes=0
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

file_path = os.path.join(script_dir, 'counter.txt')

with open(file_path,'r+') as f:
    minutes = int(f.read())

    print(f'Sleeping for {minutes} minutes')
    time.sleep(minutes*60)
    output = stake_axs.main()
    minutes+=1
    if output!=0:
        print("Issues, sleeping 1 minute")
        time.sleep(60)
        output = stake_axs.main()
        minutes+=1
    f.seek(0)
    f.write(str(minutes))
    f.close()
