import requests
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from reportlab.lib.units import inch

# URL for data extraction
url = "https://financialmodelingprep.com/api/v4/earning-calendar-confirmed?from=2023-04-10&to=2023-08-19&apikey=a5980d75f7be916e2d25fb9aa625bef1"

# Fetch the raw data
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    data = []

# Process the data into a DataFrame
df = pd.DataFrame(data)

# Function to split long text into multiple lines
def split_text(text, max_length=15):
    return '\n'.join([text[i:i+max_length] for i in range(0, len(text), max_length)])

# Shorten long text entries in the dataframe
for col in df.columns:
    df[col] = df[col].apply(lambda x: split_text(str(x)) if isinstance(x, str) else x)

# Create a PDF using ReportLab
def create_pdf_reportlab(dataframe, pdf_filename):
    # Set up the PDF file with multi-page support
    pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Prepare table data (headers + rows)
    table_data = [list(dataframe.columns)]  # Headers
    for row in dataframe.itertuples(index=False):
        table_data.append(list(row))

    # Create a table
    table = Table(table_data)

    # Table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8)
    ]))

    # Set the column width to prevent overflow
    col_widths = [1.0 * inch for _ in dataframe.columns]
    
    # Table wrapping to avoid overflow
    table._argW = col_widths

    # Build the PDF
    pdf.build([table])

# Generate the PDF
pdf_filename = "Earning_calendar.pdf"
create_pdf_reportlab(df, pdf_filename)
print(f"PDF created successfully: {pdf_filename}")
