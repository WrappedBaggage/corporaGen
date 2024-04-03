from openai import OpenAI
from dotenv import load_dotenv
import os
import csv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Gets the api key from the local environment loaded above. The OS environment variable doesn't work for me for some reason.
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def xlsx_generator(filename, directory, prompt):
    # Set the role of the AI and the user request
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a excel content creation program. Your only purpose is to generate generic excel data in csv format with appropriate headers. Your goal is to generate as many lines of data as possible."},
            {"role": "user", "content": "Create a csv for an excel spreadsheet that could be found on the laptop of an employee of a big tech company. You decide on an appropriate context. It is very important that you only provide the csv output (no additional text), and that you provide as many lines as possible!"}
        ]
    )

    # Just a cleaner variable for the output of the AI
    data = chat_completion.choices[0].message
    # The list that will contain the formatted data before outputting into a CSV file
    CSVlist = []

    # Filters out the trash that comes with the AI's return and appends the output we want into our CSV list
    count =  0
    for i in data:
        if count ==  0:
            CSVlist.append(i[1])
            count +=  1
        else:
            pass

    # Formats the data appropriately for CSV export
    lines = CSVlist[0].split("\n")

    #Adds the data to excel.csv file
    with open("excel.csv", "w", newline="") as AIdata:
        writer = csv.writer(AIdata)
        for line in lines:
            if line:
                values = line.split(',')
                writer.writerow(values)

    #Converts csv to xlsx
    def csv_to_xlsx(csv_path, xlsx_path):
        df = pd.read_csv(csv_path)
        df.to_excel(xlsx_path, index = False)

    xlsx_path = os.path.join(directory, f"{filename}.xlsx")
    csv_to_xlsx("excel.csv", xlsx_path)
    return xlsx_path

if __name__ == "__main__":
    xlsx_generator("filename", "directory")