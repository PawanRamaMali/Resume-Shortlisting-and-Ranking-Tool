import glob
import operator
import os
import warnings
import PyPDF2
import textract
from gensim.summarization import summarize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import docx2txt

from core.functions import *

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')


class ResultElement:
    def __init__(self, rank, filename, candidate_name="Loading", mobile=123456789):
        self.rank = rank
        self.filename = filename
        self.candidate_name = re.sub("[^A-Za-z]", "", filename.split(".")[0])
        self.mobile = mobile


def getfilepath(loc):
    temp = str(loc)
    temp = temp.replace('\\', '/')
    return temp


def res(jobfile):
    Resume_Vector = []
    Ordered_list_Resume = []
    Ordered_list_Resume_Score = []
    LIST_OF_FILES = []
    LIST_OF_FILES_PDF = []
    LIST_OF_FILES_DOC = []
    LIST_OF_FILES_DOCX = []
    Resumes = []
    Temp_pdf = []
    os.chdir('./data/Uploaded_Resumes')
    for file in glob.glob('**/*.pdf', recursive=True):
        LIST_OF_FILES_PDF.append(file)
    for file in glob.glob('**/*.doc', recursive=True):
        LIST_OF_FILES_DOC.append(file)
    for file in glob.glob('**/*.docx', recursive=True):
        LIST_OF_FILES_DOCX.append(file)

    LIST_OF_FILES = LIST_OF_FILES_DOC + LIST_OF_FILES_DOCX + LIST_OF_FILES_PDF
    # LIST_OF_FILES.remove("antiword.exe")
    print("This is LIST OF FILES")
    print(LIST_OF_FILES)

    # print("Total Files to Parse\t" , len(LIST_OF_PDF_FILES))
    print("####### PARSING ########")
    for nooo, i in enumerate(LIST_OF_FILES):
        Ordered_list_Resume.append(i)
        Temp = i.split(".")
        if Temp[1] == "pdf" or Temp[1] == "Pdf" or Temp[1] == "PDF":
            try:
                print("This is PDF", nooo)
                with open(i, 'rb') as pdf_file:
                    read_pdf = PyPDF2.PdfFileReader(pdf_file)

                    number_of_pages = read_pdf.getNumPages()
                    for page_number in range(number_of_pages):
                        page = read_pdf.getPage(page_number)
                        page_content = page.extractText()
                        page_content = page_content.replace('\n', ' ')
                        Temp_pdf = str(Temp_pdf) + str(page_content)

                    Resumes.extend([Temp_pdf])
                    Temp_pdf = ''

            except Exception as e:
                print(e)

        if Temp[1] == "doc" or Temp[1] == "Doc" or Temp[1] == "DOC":
            print("This is DOC", i)
            try:
                a = textract.process(i)
                a = a.replace(b'\n', b' ')
                a = a.replace(b'\r', b' ')
                b = str(a)
                c = [b]
                Resumes.extend(c)

            except Exception as e:
                print(e)

        if Temp[1] == "docx" or Temp[1] == "Docx" or Temp[1] == "DOCX":
            print("This is DOCX", i)
            try:
                a = textract.process(i)
                a = a.replace(b'\n', b' ')
                a = a.replace(b'\r', b' ')
                b = str(a)
                c = [b]
                Resumes.extend(c)

            except Exception as e:
                print(e)

        if Temp[1] == "ex" or Temp[1] == "Exe" or Temp[1] == "EXE":
            print("This is EXE", i)
            pass

    print("Done Parsing.")

    Job_Desc = 0
    LIST_OF_TXT_FILES = []
    print(os.getcwd())
    os.chdir('../job_descriptions')
    f = open(jobfile, 'r')
    text = f.read()
    text = text.replace('\n', ' ')
    # print(text)
    job_description_summary = text
    try:
        tttt = str(text)
        tttt = summarize(tttt, word_count=100)
        text = [tttt]
    except:
        text = 'None'
    f.close()

    # Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    # print(text)
    vectorizer.fit(text)
    vector = vectorizer.transform(text)
    Job_Desc = vector.toarray()
    # print(Job_Desc)

    os.chdir('../')
    resume_summary = []
    for i in Resumes:
        text = i
        tttt = str(text)
        text = text.replace('\n', ' ')
        resume_summary.append(text)
        try:
            tttt = summarize(tttt, word_count=100)
            text = [tttt]
            vector = vectorizer.transform(text)
            vector.toarray()
            Resume_Vector.append(vector.toarray())
        except:
            pass
    # print(Resume_Vector)

    for i in Resume_Vector:
        samples = i
        neigh = NearestNeighbors(n_neighbors=1)
        neigh.fit(samples)
        NearestNeighbors(algorithm='auto', leaf_size=30)
        Ordered_list_Resume_Score.extend(neigh.kneighbors(Job_Desc)[0][0].tolist())

    Z = [x for _, x in sorted(zip(Ordered_list_Resume_Score, Ordered_list_Resume))]
    print("Test")
    print(Ordered_list_Resume)

    print(Ordered_list_Resume_Score)
    flask_return = []

    for n, i in enumerate(Z):
        name = getfilepath(i)
        rank = n + 1
        res = ResultElement(rank, name)
        if rank <= 10:
            flask_return.append(res)
        else:
            break
        print(f"Rank {res.rank + 1} :\t {res.filename}")
    return flask_return


if __name__ == '__main__':
    inputStr = input("")
