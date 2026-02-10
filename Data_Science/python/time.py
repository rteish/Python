import time
#start_time = time.time()
#duration = 5
#while time.time() - start_time < duration:
#    print("Running...")
#    time.sleep(1)
#print("Finished!")
#end_time = time.time()
#print(f"Total time taken: {end_time - start_time} seconds")

from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
current_date = now.strftime("%Y-%m-%d")
print("Current Date =", current_date)
current_year = now.strftime("%Y")
print("Current Year =", current_year)

