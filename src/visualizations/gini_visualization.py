import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./resources/results/giniSelection.csv")
ax = df.plot.barh(x='feature', y='gini_score', rot=0)
#To allow more margin for the x axis, use the subplot settings when the graph is displayed.
plt.show()