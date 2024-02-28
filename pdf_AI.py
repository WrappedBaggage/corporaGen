from openai import OpenAI
from dotenv import load_dotenv
import re
import os
import uuid
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def sanitize_filname(title):
      invalid_characters = r"[%<>:\"/\\|?*]"
      sanitized_title = re.sub(invalid_characters, "", title).replace(" ", "_")
      return sanitized_title

def pdf_generator(directory):
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a PDF content creation program. Your only purpose is to generate generic PDF data. "},
            {"role": "user", "content": """Create data for a PDF that could be found on the laptop of an employee of a big tech company.
                You decide on an appropriate context and names of people, companies or places.
                The following conditions are very important! At the start of a line that is a title you need
                to place a '%' symbol and at the start line that contains a heading you need to place a '&' symbol.
                Other text does not need symbol at the start of the line. Nothing else should be placed before the '%' or '&' symbols,
                can only contain one title, headings need to be numbered, and empty lines should not contain any symbols.
                It needs to be at least  100 lines.
            """}
        ]
    )

    data = chat_completion.choices[0].message
    # The list that will contain the formatted data before outputting into a CSV file
    datalist = []

    # Filters out the trash that comes with the AI's return and appends the output we want into our CSV list
    count =  0
    for i in data:
        if count ==  0:
            datalist.append(i[1])
            count +=  1
        else:
            pass

    # Formats the data appropriately for CSV export
    datalist = datalist[0].split("\n")

    first_title = None
    for text in datalist:
        if text.startswith("%"):
            first_title = text[1:]
            break

    # Makes a filename based on the first title and if if can't find that it makes a uuid name
    if first_title:
        filename = sanitize_filname(first_title) + ".pdf"
    else:
        filename = str(uuid.uuid4()) + ".pdf"
    doc = SimpleDocTemplate(os.path.join(directory, filename), pagesize=letter)

    # Define the styles for the title, headings, and regular text
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    regular_style = styles["Normal"]

    # Create a list of paragraphs for the headings and texts
    elements = []

    for text in datalist:
        if text == "":
            # This is an empty string, add a new line
            elements.append(Spacer(1,  12))
        elif text.startswith("%"):
            # This is a title
            elements.append(Paragraph(text[1:], title_style))
        elif text.startswith("&"):
            # This is a heading
            elements.append(Paragraph(text[1:], heading_style))
        else:
            # This is regular text
            elements.append(Paragraph(text, regular_style))

    # Build the document
    doc.build(elements)

if __name__ == "__main__":
    pdf_generator()