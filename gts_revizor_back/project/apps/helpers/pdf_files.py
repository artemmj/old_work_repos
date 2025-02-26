from typing import List

from PyPDF2 import PdfWriter


def merge_pdf_files(paths_to_generated_reports: List[str], output_dest: str):
    merger = PdfWriter()

    for path_to_generated_reports in paths_to_generated_reports:
        with open(path_to_generated_reports, 'rb') as file_obj:
            merger.append(fileobj=file_obj)

    merger.write(output_dest)
    merger.close()

    return output_dest
