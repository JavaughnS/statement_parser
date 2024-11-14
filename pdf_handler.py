import pdfplumber
import fitz
import pandas
import camelot

# class PDFHandler(self):
def extract_pdf_annots(pdf_path):
    def make_text(words):
        line_dict = {} 

        words.sort(key=lambda w: w[0])

        for w in words:  

            y1 = round(w[3], 1)  

            word = w[4] 

            line = line_dict.get(y1, [])  

            line.append(word)  

            line_dict[y1] = line  

        lines = sorted(line_dict.items())

        return "n".join([" ".join(line[1]) for line in lines])
    
    try:
        pdf = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error extracting annots: {e}")

    page1 = pdf[0]
    words = page1.get_text("words")

    all_annots = []

    for annot in page1.annots():
        if annot != None:
            rec=annot.rect

            rec

            mywords = [w for w in words if fitz.Rect(w[:4]) in rec]
            ann = make_text(mywords)
            all_annots.append(ann)

    try:
        with open("extracted_annot.txt", "w") as text_file:
            text_file.write("n".join(all_annots))
    except Exception as e:
        print(f"Error writing file: {e}")

    print(f"Extracted annot from page 1:")
    print("n".join(all_annots))


def extract_pdf_table(pdf_path):
    # try:
        # tables = camelot.read_pdf(pdf_path, pages="all", flavor='lattice', line_scale=40)
        # # camelot.plot(tables[0],kind='contour').show()
        # with open("output/extracted_tables.txt", "w", encoding="utf-8") as output_file:
        #     print(tables.n)
        #     for i, table in enumerate(tables):
        #         print(table.df)
        #         output_file.write(f"Table {i + 1}:\n")
        #         output_file.write(table.df.to_string(index=False, header=False))
        #         output_file.write("\n\n")
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]  # Access a specific page
            im = page.to_image()  # Convert the page to an image
            im.show()

            # Extract tables
            tables = page.extract_tables({"vertical_strategy": "text", "join_x_tolerance": 30})

            # Draw rectangles around detected tables
            for table in tables:
                if table:
                    for row in table:
                        if row and all(row):
                            rect = page.bbox  # Replace with your bounding box coordinates if needed
                            im.draw_rect(rect)  # Draw the rectangle

            # Show the image with highlighted rectangles
            # im.show()

            # Open a new text file to write the extracted text
            with open("output/extracted_tables.txt", "w", encoding="utf-8") as output_file:
                tables = []
                # simplii:
                # simplii_table_settings = {"horizontal_strategy": "text"}

                # td:
                # td_table_settings = {"vertical_strategy": "text"}
                # cropped_page = page.within_bbox((0, 0, 347, 616)).extract_table(...)

                for page in pdf.pages:
                    
                    tables.append(page.extract_table({"vertical_strategy": "text"}))
                if tables:
                    for table in tables:
                        # print(f"Tables from page {page_num + 1}:")
                        if table:
                            for row in table:
                                print(row)
                                row_string = "\t".join(str(cell) if cell not in [None, ""] else "" for cell in row)
                                output_file.write(row_string + "\n")
                    # output_file.write(f"Page {page_num + 1}:\n")
                    # output_file.write(table)
                    output_file.write("\n\n")  # Add a blank line after each page's text
                # else:
                #     output_file.write(f"Page {page_num + 1}: No table found\n\n")
        
        print("Table extraction complete. Check the extracted_table.txt file.")

    # except Exception as e:
    #     print(f"Error extracting table from PDF: {e}")

def extract_pdf_text(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Open a new text file to write the extracted text
            with open("output/extracted_text.txt", "w", encoding="utf-8") as output_file:
                # Iterate through all pages in the PDF
                for page_number, page in enumerate(pdf.pages):
                    # Extract text from the current page
                    page_text = page.extract_text()
                    
                    if page_text:
                        # Write the extracted text of this page to the file
                        output_file.write(f"Page {page_number + 1}:\n")
                        output_file.write(page_text)
                        output_file.write("\n\n")  # Add a blank line after each page's text
                    else:
                        output_file.write(f"Page {page_number + 1}: No text found\n\n")
        
        print("Text extraction complete. Check the extracted_text.txt file.")
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")