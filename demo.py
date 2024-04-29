import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Example data (replace this with your actual data retrieval code)
start_date = '2024-04-27 09:00:00'
end_date = '2024-05-27 16:00:00'
num_data_points = 1000

# Generate timestamps using pd.date_range()
timestamps = pd.date_range(start=start_date, end=end_date, periods=num_data_points)

# Generate example prices (replace this with your actual price data)
prices = np.random.randint(80, 120, size=num_data_points)  # Generate random prices between 80 and 120

# Create a DataFrame
df = pd.DataFrame({'Timestamp': timestamps, 'Price': prices})

# Set Timestamp column as index
df.set_index('Timestamp', inplace=True)

# Resample data to different time intervals (5 minutes, 1 hour, 1 day)
df_5min = df.resample('5T').mean()  # 5 minutes
df_1hour = df.resample('1H').mean()  # 1 hour
df_1day = df.resample('1D').mean()  # 1 day

# Plot the data
plt.figure(figsize=(10, 6))

# Plot 5-minute data
plt.plot(df_5min.index, df_5min['Price'], label='5 Minutes')

# Plot 1-hour data
plt.plot(df_1hour.index, df_1hour['Price'], label='1 Hour')

# Plot 1-day data
plt.plot(df_1day.index, df_1day['Price'], label='1 Day')

plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Stock Price Over Time')
plt.legend()
plt.grid(True)
plt.show()
