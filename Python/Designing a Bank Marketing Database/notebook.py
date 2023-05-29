# Start coding...
import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv("datasets/bank_marketing.csv")


# Split the data
client = df[["client_id", "age", "job", "marital", "education", "credit_default", "housing", "loan"]]

campaign = df[["client_id", "campaign", "month", "day_of_week", "duration", "pdays", "previous", "poutcome", "y"]]

economics = df[["client_id", "emp_var_rate", "cons_price_idx", "euribor3m", "nr_employed"]]

# Rename, clean, create, and delete columns
# Renaming columns
client.rename(columns={"client_id": "id"}, inplace=True)

campaign.rename(columns={"duration": "contact_duration",
                         "previous": "previous_campaign_contacts",
                         "y": "campaign_outcome",
                         "campaign": "number_contacts",
                         "poutcome": "previous_outcome"},
                inplace=True)

economics.rename(columns={"euribor3m": "euribor_three_months", "nr_employed": "number_employed"}, inplace=True)

# Cleaning columns
client["education"] = client["education"].str.replace(".", "_")
client["education"] = client["education"].replace("unknown", np.NaN)
client["job"] = client["job"].str.replace(".", "")

campaign["campaign_outcome"] = campaign["campaign_outcome"].replace({"yes": 1, "no": 0})
campaign["previous_outcome"] = campaign["previous_outcome"].replace("non_existent", np.NaN)\
    .replace({"failure": 0, "success": 1})

# Creating new columns
campaign["month"] = campaign["month"].str.capitalize()
campaign["day_of_week"] = campaign["day_of_week"].str.capitalize()
campaign["year"] = "2022"
campaign["last_contact_date"] = campaign["year"] + "-" + campaign["month"] + "-" + campaign["day_of_week"]
campaign["last_contact_date"] = pd.to_datetime(campaign["last_contact_date"], format="%Y-%b-%a")
campaign["campaign_id"] = 1

# Deleting columns
campaign.drop(columns=["month", "year", "day_of_week"], inplace=True)

# Saving the data
# Store the DataFrames
client.to_csv("datasets/client.csv", index=False)
campaign.to_csv("datasets/campaign.csv", index=False)
economics.to_csv("datasets/economics.csv", index=False)

# Structuring the dictionary
database_design = {"client": client, "campaign": campaign, "economics": economics}

print(database_design)
