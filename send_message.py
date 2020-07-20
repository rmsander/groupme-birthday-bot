import pandas as pd
from datetime import datetime
import requests
from ID import BOT_ID  # Don't push this file to GitHub

def main():

    # Destination URL
    URL = "https://api.groupme.com/v3/bots/post/"

    # CSV where birthdays are read from
    sheet_path = "birthdays.csv"

    # Read CSV and check if "posted" needs to be added as a column
    df = pd.read_csv(sheet_path)  # Read birthday CSV
    if "posted" not in list(df.keys()):
        df["posted"] = 0  # Default to False

    # Get current day
    current_day = datetime.strptime(str(datetime.today().month)+"-"+str(datetime.today().day), "%m-%d")

    # Get indices of birthdays today
    birthday_rows = pd.to_datetime(df.Birthday, format="%m-%d") == current_day

    # Using indices, get names and whether or not posts have already been made
    birthday_names = df[birthday_rows].Name.values.tolist()
    posted = df[birthday_rows].posted.values.tolist()

    # Iterate through birthdays, if there are multiple
    for i, (name, done) in enumerate(zip(birthday_names, posted)):
        if not done:
            print("POSTING FOR PERSON: {}".format(name))
            MYOBJ = {"bot_id": "c98b9a598a7a1ffdcbc9637bc4",
                     "text": "Happy birthday {}! :)".format(name)}

            x = requests.post(URL, data = MYOBJ)
            print("REQUEST: {}".format(x))

            # Set to done for that person
            df["posted"][i] = 1
            df.to_csv(sheet_path)  # Save updated CSV to reflect postings

if __name__ == "__main__":
    main()