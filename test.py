import pandas as pd
import plotly.express as px
from PIL import Image
from io import BytesIO

# Create a sample DataFrame
data = {'Category': ['A', 'B', 'C', 'D'],
        'Value': [10, 15, 7, 20]}

df = pd.DataFrame(data)

# Plot a bar chart using Plotly Express
fig = px.bar(df, x='Category', y='Value', title='Bar Chart Example')

# Save the figure as an image with higher quality (adjust the scale as needed)
image_bytes = fig.to_image(format="png", scale=2.0)  # Increase scale for higher quality

# Display the image using PIL
image = Image.open(BytesIO(image_bytes))
image.show()
