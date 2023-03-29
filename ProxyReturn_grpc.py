import redis

# Create a Redis client
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Get the value of all keys
print(r.hgetall('1'))

# Extract airwellness values
airwellness_values = r.hvals('1')

print(airwellness_values)

parsed_values = []
for value in airwellness_values:
    parsed_value = float(value.decode().split(': ')[1].strip())
    parsed_values.append(parsed_value)

print(parsed_values)

# Close the connection
r.close()

