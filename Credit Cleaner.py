#Credit Cleaner
try:
    import re
    import os
    import csv
    import xlsxwriter
    import argparse
except ImportError:
    print("One or more dependencies missing, run 'pip install -r requirements.txt'")
    exit()
def extant_file(x):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("File does not exist")
    return x
parser = argparse.ArgumentParser(description= "A parser for credit card skimmers with the 'T1' 'T2' formating")
parser.add_argument("file_path", type=extant_file, help= "Path of plaintext file for parsing")
args = parser.parse_args()
path = os.path.dirname(os.path.abspath(args.file_path))
test = re.compile("(?<!\d)\d{16}(?!\d)")
test2 = re.compile("(?<!\d)\d{14}(?!\d)")
test3 = re.compile("(?<!\d)\d{11}(?!\d)")
mName = []
mCredit = []
mMisc = []
t2Credit = []
t2Misc = []
err = []
header = ["Name", "Credit Card #"]
def fileParse(filename):
    x = []
    with open(filename, 'r') as f:
        for index, line in enumerate(f):
            if 'T1' in line:
                if "^" in line:
                    try:
                        var = line.split("^")
                        mCredit.append(var[0])
                        mName.append(var[1])
                        mMisc.append(var[2])
                    except IndexError:
                        err.append(line)
                else:
                    var = line.split("/")
                    mCredit.append(var[0] + " CORRUPTED")
                    mName.append("Corrupted")
                    mMisc.append("Corrupted")
            if 'T2' in line:
                if "=" in line:
                    try:
                        var = line.split("=")
                        t2Credit.append(var[0])
                        t2Misc.append(var[1])
                    except IndexError:
                        err.append(line)
                else:
                    t2Credit.append("Corrupted")
                    t2Misc.append("Corrupted")
                    
    return x
def csvWriter():
    with open(os.path.join(os.path.expanduser('~'),'Desktop',"CardNumANDName"), "w") as f:
        fieldnames = ["Name", "Credit Card #", "Misc", "T2Credit", "T2Misc"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for x in range(0,len(mCredit)):
            try:
                mName[x] = mName[x].replace(",","")
            except IndexError:
                pass
            try:
                mCredit[x] = mCredit[x].replace(",","")
            except IndexError:
                pass
            try:
                mMisc[x] = mMisc[x].replace(",","")
            except IndexError:
                pass
            try:
                t2Credit[x] = t2Credit[x].replace(",","")
            except IndexError:
                pass
            try:
                t2Misc[x] = t2Misc[x].replace(",","")
            except IndexError:
                pass
            try:
                var1 = mCredit[x].split("B")
                mCredit[x] = var1[1]
            except IndexError:
                pass
            try:
                var2 = t2Credit[x].split(";")
                t2Credit[x] = var2[1]
            except IndexError:
                pass
            try:
                writer.writerow({'Name': mName[x], 'Credit Card #': mCredit[x], 'Misc': mMisc[x], 'T2Credit': t2Credit[x], "T2Misc": t2Misc[x]})
            except IndexError:
                break
def excel_write():
    workbook = xlsxwriter.Workbook(path+'/'+ filename+'.xlsx')
    worksheet = workbook.add_worksheet()
    row = 1
    col = 0
    y = 0
    headers = ["Name", "CREDIT_CARD","MISC","T2_CREDIT","T2_MISC"]
    worksheet.write(0,0,"NAME")
    worksheet.write(0,1,"CREDIT_CARD")
    worksheet.write(0,2,"MISC")
    worksheet.write(0,3,"T2_CREDIT")
    worksheet.write(0,4,"T2_MISC")
    for x in range(0, len(mCredit)):
        try:
            mName[x] = mName[x].replace(",","")
        except IndexError:
            mName[x].append("")
        try:
            mCredit[x] = mCredit[x].replace(",","")
        except IndexError:
            mCredit[x].append("")
        try:
            mMisc[x] = mMisc[x].replace(",","")
        except IndexError:
            mMisc[x].append("")
        try:
            t2Credit[x] = t2Credit[x].replace(",","")
        except IndexError:
            t2Credit[x].append("")
        try:
            t2Misc[x] = t2Misc[x].replace(",","")
        except IndexError:
            t2Misc[x].append("")
        try:
            var1 = mCredit[x].split("B")
            mCredit[x] = var1[1]
        except IndexError:
            pass
        try:
            var2 = t2Credit[x].split(";")
            t2Credit[x] = var2[1]
        except IndexError:
            pass
        worksheet.write(row,col,mName[x])
        worksheet.write(row,col+1,mCredit[x])
        worksheet.write(row,col+2,mMisc[x])
        worksheet.write(row,col+3,t2Credit[x])
        worksheet.write(row,col+4,t2Misc[x])
        row += 1
    workbook.close()
filename = os.path.basename(args.file_path).split(".")[0]
fileParse(filename)
excel_write()
##csvWriter()
for x in range(0, len(err)):
    print("Error in Line: "+ err[x])
            
