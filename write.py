import xlwt

def excel_setup(subject_code):
	master = xlwt.Workbook()
	sheet = master.add_sheet(subject_code)
	return master, sheet

def writeline(sheet, fotoNumber, left_eye_x, left_eye_y, right_eye_x, right_eye_y):

