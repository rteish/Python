import math

sub=['math', 'science', 'data', 'analysis', 'statistics']
marks=[85, 90, 78, 92, 88]
for i in range(len(sub)):
    print(f"Subject: {sub[i]}, Marks: {marks[i]}")
total_marks = sum(marks)
average_marks = total_marks / len(marks)
print(f"Total Marks: {total_marks}")
print(f"Average Marks: {average_marks}")

