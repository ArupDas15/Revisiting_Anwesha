import jnius_config

# Set the classpath
jnius_config.add_classpath('out')

# Import the Java class
from jnius import autoclass

Driver = autoclass("FConnection")

# Create an instance of the Java class
obj = Driver()

# Call a method on the Java object
while True:
	st = input("Enter the input word (Type 'Q' to Stop): ")
	if st == 'Q': break
	result = obj.task(st)
	print(result)