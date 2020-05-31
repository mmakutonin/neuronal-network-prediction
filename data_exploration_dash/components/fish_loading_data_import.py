import os
import pandas as pd
from util.util_functions import load_file

model_list = load_file('data_synthesized_pickled/geo_plotting_data.pickle')

print(type(model_list[0]))
print(type(model_list[0]["x"]))

model_dict = {f"{row['subject']}:{row['stimulus']}": row["x"].join(
    row["y"], how="inner"
).join(
    row["z"], how="inner"
).join(
    row["loadings"], how="inner"
) for row in model_list}

print(model_dict["subject_1:None"].head())
print(model_dict["subject_1:None"].shape)



