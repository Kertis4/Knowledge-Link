import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from io import BytesIO

def plot_change_over_time_from_csv(data_string, statistic_name, graph_title):

    try:
        # Attempt to read the CSV file with common encodings and delimiters
        data = None
        csv_data = StringIO(data_string)
        try:
            data =  pd.read_csv(csv_data, encoding='utf-8')
        except UnicodeDecodeError:
            data =  pd.read_csv(csv_data, encoding="latin1")

        # If delimiter issues arise, try alternative delimiters
        if data is None or data.empty:
            raise ValueError("File could not be loaded. Please check its format.")

        # Display the first few rows to confirm structure (optional for debugging)

        # Ensure required columns are present
        if 'Year' not in data.columns or statistic_name not in data.columns:
            raise ValueError(f"The dataset must contain 'Year' and '{statistic_name}' columns.")

        # Group by year and calculate mean values for the statistic
        grouped_data = data.groupby('Year')[statistic_name].mean().reset_index()

        # Plotting with blue, grey, and orange color scheme
        plt.figure(figsize=(10, 6))
        plt.plot(grouped_data['Year'], grouped_data[statistic_name], marker='o', linestyle='-', color='blue', label=statistic_name)

        # Add gridlines and customize colors
        plt.grid(color='grey', linestyle='--', linewidth=0.5)

        plt.xticks(grouped_data['Year'], rotation=45)

        # Title and labels
        plt.title(f"Change Over Time: {statistic_name}", fontsize=14, color='orange')
        plt.xlabel("Year", fontsize=12)
        plt.ylabel(statistic_name, fontsize=12)

        # Show legend
        plt.legend(loc="best")

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        plt.close()

        img_buffer.seek(0)


        return img_buffer

    except Exception as e:
        print(f"An error occurred: {e}")
