import os
import pandas as pd
from util.util_functions import load_file

model_list = load_file('data_synthesized_pickled/geo_plotting_data.pickle')

subject_stimulus_df = pd.DataFrame(model_list).loc[:, ["subject", "stimulus"]].drop_duplicates()

model_dict = {f"{row['subject']}:{row['stimulus']}": row["x"].join(
    row["y"], how="inner"
).join(
    row["z"], how="inner"
).join(
    row["loadings"], how="inner"
) for row in model_list}

component_functions = {f"{row['subject']}:{row['stimulus']}": row['component_fxns'] for row in model_list}