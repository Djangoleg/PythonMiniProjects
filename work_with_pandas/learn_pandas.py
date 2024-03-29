import pandas as pd

# pd.set_option('display.max_rows', 40)

movies = pd.read_csv("movies.csv", index_col='Title')

# pandas.core.frame.DataFrame
# print(movies)

# Print first 10 rows.
print(movies.head(10))

# Print last 10 rows.
# print(movies.tail(10))

print(f'DataFrame movies len = {len(movies)}')

print(f'DataFrame movies shape (row, columns): {movies.shape}')

print(f'DataFrame movies number of cells: {movies.size}')

print(f'DataFrame movies column types: \n{movies.dtypes}')

print(f'DataFrame movies get line[30] by index: \n{movies.iloc[29]}')

# 30 Buena Vista $1,056.10  2016
[print(x, end=' ') for x in movies.iloc[29]]

print()

print(f'DataFrame movies get line by name: \n{movies.loc["Gravity"]}')

# 106 Warner Brothers $723.20  2013
[print(x, end=' ') for x in movies.loc["Gravity"]]

print()

# sort_values.
movies_sort = movies.sort_values(by=['Year', 'Studio'], ascending=True).head(20)

# DataFrame to string.
print(movies_sort.to_string())

# DataFrame to numpy. Here you can take the values.
for rows in movies_sort.to_numpy():
    [print(row) for row in rows]
    print('=' * 20)

print()

# Sort by index column (index_col='Title').
print(movies.sort_index().head(10).to_string())

print()

# Extract a column 'Studio' and get count.
studio = movies["Studio"]
print(studio.value_counts().head(10).to_string())

