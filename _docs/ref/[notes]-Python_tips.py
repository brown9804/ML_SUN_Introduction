# To getting a small sample of n rows from a cvs to another one 
# if you want another extension just change it.
import pandas as pd

getting_sample = pd.read_csv("./file_.csv")
df = pd.DataFrame(getting_sample)
print(df.head(5).to_csv("./getting_sample.csv"))
