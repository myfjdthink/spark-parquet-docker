import pandas as pd

pd.set_option('display.max_columns', None)
df = pd.read_parquet('./data/20231220_085518_13207_seu4n_6dfa4a96-aec1-4f72-ab1d-851cf2fc04fc')

print(df.count())
print(df.head())
