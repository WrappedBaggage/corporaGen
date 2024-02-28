#import libraries
import uuid
import os
import logging
import csv
import random
import time
from abc import ABC, abstractmethod
from pdf_AI import pdf_generator
from xlsx_AI import xlsx_generator
from txt_AI import txt_generator
from jpg_AI import jpg_generator
from mail_AI import mail_generator

#Each class object needs to use the create function in order to finish initialization of the object
class File(ABC):
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content
        
    @abstractmethod
    def create(self, directory):
        pass

class TxtFile(File):
    def create(self, directory):
        start_time = time.perf_counter()
        txt_generator(self.filename, directory)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        return elapsed_time

class JpgFile(File):
    def create(self, directory):
        start_time = time.perf_counter()
        jpg_generator(directory)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        return elapsed_time

class PdfFile(File):
    def create(self, directory):
        start_time = time.perf_counter()
        pdf_generator(directory)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        return elapsed_time
    
class XlsxFile(File):
    def create(self, directory):
        start_time = time.perf_counter()
        xlsx_generator(self.filename, directory)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        return elapsed_time

class EmlFile(File):
    def create(self, directory):
        start_time = time.perf_counter()
        mail_generator(self.filename, directory)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        return elapsed_time
    
def main():
    #choice of filetypes
    filetype_list = ["txt", "jpg", "pdf", "xlsx", "eml"]
    
    #initialize logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    start_time  = time.perf_counter()
    
    #User input
    num_files = int(input("How many files do you want to create? "))
    directory = str(input("Target directory "))
    
    #Checks if directory exists, if not, it is created
    log_dir = os.path.join(directory, 'log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    #Initializing log file
    log_file = os.path.join(log_dir, 'execution.log')
    handler = logging.FileHandler(log_file)
    logger.addHandler(handler)
    logger.info(f"File creation of {num_files} files has started in the {directory} directory.")
    
    
    tempdata_file = os.path.join(directory, 'tempdata.csv')
    generate_csv(num_files, filetype_list, tempdata_file)
    
    files_creation_times = []
    with open(tempdata_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filetype = row['filetype']
            filename = row['filename']
            content = row['content']
            file_instance = None
            
            if filetype == "txt":
                file_instance = TxtFile(filename, content)
            elif filetype == "jpg":
                file_instance = JpgFile(filename, content)
            elif filetype == "pdf":
                file_instance = PdfFile(filename, content)
            elif filetype == "xlsx":
                file_instance = XlsxFile(filename, content)
            elif filetype == "eml":
                file_instance = EmlFile(filename, content)
            
            if file_instance:
                time_spent = file_instance.create(directory)
                files_creation_times.append(time_spent)
    
    end_time = time.perf_counter()
    min_time = min(files_creation_times)
    max_time = max(files_creation_times)
    avg_time = sum(files_creation_times) / len(files_creation_times)
    logger.info(f"Minimum file creation time: {min_time:.2f} seconds")
    logger.info(f"Maximum file creation time: {max_time:.2f} seconds")
    logger.info(f"Average file creation time: {avg_time:.2f} seconds")
    elapsed_time = end_time - start_time
    logger.info(f"Finished after {elapsed_time:.2f} seconds")

def generate_filename(filetype):
    if filetype == "txt":
        return b"Txt filename is generated based on context within the txt_generator module"
    elif filetype == "jpg":
        return str(uuid.uuid4())[:8]
    elif filetype == "pdf":
        return b"Pdf filename is generated based on context within the pdf_generator module"
    elif filetype == "xlsx":
        return str(uuid.uuid4())[:8]
    elif filetype == "eml":
        return b"Eml filename is generated based on context within the eml_generator module"

def generate_content(filetype):
    if filetype == "txt":
        return b"Txt content is generated using txt_AI.py"
    elif filetype == "jpg":
        return b"Image content is generated using jpg_AI.py"
    elif filetype == "pdf":
        return b"Pdf content is generated using pdf_AI.py"
    elif filetype == "xlsx":
        return b"Xlsx content is generated using xlsx_AI.py"
    elif filetype == "eml":
        return b"Eml content is generated using mail_AI.py"

def generate_csv(num_files, filetype_list, tempdata_file):
    
    with open(tempdata_file, 'w', newline='') as csvfile:
        fieldnames = ['filename', 'filetype', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for _ in range(num_files):
            filetype = random.choice(filetype_list)
            filename = generate_filename(filetype)
            content  = generate_content(filetype)
            writer.writerow({'filename': filename, 'filetype': filetype, 'content': content})
            
        
if __name__ == '__main__':
    main()