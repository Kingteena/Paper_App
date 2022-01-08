import PyPDF2


def readMarkingScheme(paper):
    pdf_reader = PyPDF2.PdfFileReader(paper)
    answer_dict = {}
    for page in range(1, pdf_reader.numPages):
        answer_list = pdf_reader.getPage(page).extractText().split('\n')[3].split()
        for i in range(3, len(answer_list), 3):
            answer_dict[answer_list[i]] = answer_list[i + 1]
    return answer_dict


def getPages(paper_code, static_folder):
    paper_path = f"{static_folder}/questions_predit/{paper_code}"
    with open(f"{paper_path}.pdf", 'rb') as paper:
        reader = PyPDF2.PdfFileReader(paper)
        for page in range(1, reader.numPages):
            writer = PyPDF2.PdfFileWriter()
            writer.addPage(reader.getPage(page))
            with open(f'{paper_path}_{page}.pdf', 'wb') as outfile:
                writer.write(outfile)
    return reader.numPages


def cropPage(start, end, page_number, question_number, paper_code, static_folder):
    with open(f"{static_folder}/questions_predit/{paper_code}.pdf", "rb") as in_f:
        reader = PyPDF2.PdfFileReader(in_f)
        writer = PyPDF2.PdfFileWriter()
        start_x, end_x = 1, 594
        y = 842
        page = reader.getPage(page_number)
        page.cropBox.lowerLeft = (start_x, y - start)
        page.cropBox.upperRight = (end_x, y - end)
        writer.addPage(page)
        with open(f"{static_folder}/questions/{paper_code}_{question_number}.pdf", "wb") as out_f:
            writer.write(out_f)



