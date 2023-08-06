from lib import Logger;
from lib import fn;
from lib import DateTime;
from io import StringIO;
from sylk_parser import SylkParser;
import xlrd;
import pandas as pd;
import numpy as np;
import os;
import csv;
import sys;
import time;
import shutil;
import re;
import datetime;
import zipfile;

def readToDF(file, use_special_txt=False, skiprows=None, dtype=str):
	extension = file.split('.')[-1];
	# print('extension', extension, file)
	data = pd.DataFrame();
	ext_read_function = {
		# 'txt': readTxtToDFTest,
		'txt': readTxtToDF,
		'special_txt': readTxtToDFTest,
		'xls': readXlsToDF,
		'xlsx': readExcelToDF,
		'slk': readSlkToDF,
		'csv': readCSVToDF,
	};
	if skiprows is not None and extension in ['csv', 'xlsx']:
		data = ext_read_function[extension](file, skiprows=skiprows, dtype=dtype);
	else:
		data = ext_read_function[extension](file);
	if extension == 'txt':
		data.info();
		total_lines = countTxtTotalLine(file);
		if data.empty or len(data) != total_lines:
			Logger.v('## None run txt test', data.empty, len(data), total_lines);
			data = readTxtToDFTest(file);
			data.info();
		if use_special_txt:
			Logger.v('## None run txt test special')
			data = readTxtToDFTest(file);
			data.info();

	return data;

def readCSVToDF(file, sep=',', encoding='unicode_escape', dtype=str, skiprows=None):
	try:
		df = pd.read_csv(file, sep=sep, encoding=encoding, dtype=dtype, skiprows=skiprows);
	except Exception as e:
		try:
			df = pd.read_csv(file, sep=';', encoding=encoding, dtype=dtype, skiprows=skiprows);
		except Exception as e:
			Logger.e('File.readCSVToDF', e);
			print('file:', file);
			df = pd.DataFrame();

	if not df.empty:
		if ';' in df.columns[0]:
			df = pd.read_csv(file, sep=';', encoding=encoding, dtype=dtype, skiprows=skiprows);
		columns = df.columns;
		to_rename = {};
		for col in columns:
			string_encode = col.encode("ascii", "ignore");
			string_decode = string_encode.decode();
			to_rename[col] = string_decode;
		df = fn.renameDFColumn(column_keymap=to_rename, data=df);
		df = df.dropna(axis=0, how='all');

	
	if 'sep=' in [c.replace(' ', '') for c in list(df.columns)]:
		data_list = []
		with open(file, newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
			fieldnames = [];
			for idx, row in enumerate(spamreader):
				if idx == 1:
					fieldnames = row;
				elif idx == 0:
					pass;
				else:
					qwe = dict(zip(fieldnames, [c.replace('"', '') for c in row]));
					data_list.append(qwe);
		df = pd.DataFrame(data_list)
		writeToCsv(file, df);

	# if df.empty:
	# 	try:
	# 		df = pd.read_csv(file, sep='\t', encoding=encoding, dtype=dtype);
	# 	except Exception as e:
	# 		Logger.e('File.readCSVToDF', e);
	# 		df = pd.DataFrame();
	return df;

def replace_str_index(text,index=0,replacement=''):
	return '%s%s%s'%(text[:index],replacement,text[index+1:])

def countTxtTotalLine(file):
	counter = 0;
	try:
		with open(file, 'r', encoding='unicode_escape') as in_file:
			for lines in in_file:
				counter += 1;
			counter -= 1; # remove header line
	except Exception as e:
		# Logger.e('File.readTxtToDFTest', e);
		# print('file:', file);
		pass;
	return counter;

def readTxtToDFTest(file, sep=None, encoding='unicode_escape'):
	result = [];
	try:
		with open(file, 'r', encoding='unicode_escape') as in_file:
			columns = [];
			first_line = '';
			counter = 0;

			for lines in in_file:
				counter += 1;
				# if counter == 2:
				# 	break;
				
				if lines.strip() != '':
					striped_lines = lines;
					striped_lines = striped_lines.replace('\n', ' ');
					# striped_lines = striped_lines.replace('\t', ' ');
					sentence = '';
					continuous_bar = 0;
					sentence_list = [];
					column_width = {

					}
					# print('striped_lines', striped_lines)
					if counter == 1:
						first_line = striped_lines;
						char_list = list(striped_lines);
						for idx, line in enumerate(char_list):
							if char_list[idx - 1] != ' ' and char_list[idx] == ' ':
								char = '%20';
							elif (char_list[idx - 1] == ' ' and char_list[idx - 2] == ' ' and char_list[idx] == ' ') or (char_list[idx - 1] == ' ' and char_list[idx] == ' '):
								char = '%7C';
							else:
								char = char_list[idx];
							
							sentence += char;
							sentence_list.append(char);
							# print(line);
						# print('b4', sentence, type(sentence))
						if sentence != '':
							sentence = sentence.replace('%20%7C', '%7C');
							sentence = sentence.replace('%7C', ' ');
							sentence = re.sub(' +', ' ', sentence);
							sentence = sentence.replace(' ', '|');
							sentence = sentence.replace('%20', ' ');
							# sentence = sentence.replace('%2C', '|');
							sentence = sentence.lstrip('|');

							# print('sentence', sentence)

							columns = [c.strip() for c in sentence.split('|')];
					else:
						pass;
						if striped_lines:
							for header_idx, header in enumerate(columns):
								# print('header', header, header_idx);
								header = header.strip();
								found_index = first_line.find(header);
								header_char_count = len(header.strip());
								if header_idx == len(columns) - 1:
									search_index = found_index + header_char_count - 2;
									if search_index >= len(striped_lines):
										search_string = 'null';
									else:
										search_string = striped_lines[search_index];
								else:
									search_index = found_index + header_char_count - 1;
									if search_index >= len(striped_lines):
										search_string = 'null';
									else:
										search_string = striped_lines[search_index];

								if header_idx == 0:
									column_width[header] = range(found_index, search_index + 1);
								elif header_idx == len(columns) - 1:
									prev_header = columns[header_idx - 1];
									start_index = column_width[prev_header];
									column_width[header] = range(start_index[-1] + 1, search_index + 2);
								else:
									prev_header = columns[header_idx - 1];
									start_index = column_width[prev_header];
									column_width[header] = range(start_index[-1] + 1, search_index + 1);
								
								# add '!' for those column is empty to prevent skipping column
								if search_string.strip() == '':
									striped_lines = replace_str_index(striped_lines, search_index, '!');

							append_obj = {};
							for col in column_width:
								col_width = column_width[col];
								combine_string = '';
								if col_width[-1] >= len(striped_lines):
									combine_string = 'null';
								else:
									for i in col_width:
										combine_string += striped_lines[i];
								combine_string = ' '.join(combine_string.split('  '));
								if combine_string.strip() == '!':
									combine_string = 'null';
								append_obj[col] = combine_string.strip();
							result.append(append_obj);
	except Exception as e:
		Logger.e('File.readTxtToDFTest', e);
		print('file:', file);

	df = pd.DataFrame(result, dtype=str);
	df = df.dropna(axis=0, how='all');
	return df;

def readTxtToDF(file, sep=None, encoding='unicode_escape'):
	# try:
	# 	# df = pd.read_csv(file, sep=sep, encoding=encoding, dtype=str);
	# 	df = pd.read_fwf(file) # read txt with fix width
	# except Exception as e:
	# 	Logger.e('File.readTxtToDF', e);
	# 	df = pd.DataFrame();

	# print(df.columns)
	# drop_columns = [];
	# for col in df.columns:
	# 	if 'unnamed:' in col.lower():
	# 		drop_columns.append(col);
	# print(drop_columns);
	# df = df.drop(columns=drop_columns);

	result = [];
	try:
		headers = [];
		with open(file, 'r') as read_obj:
			# pass the file object to reader() to get the reader object
			csv_reader = csv.reader(read_obj, delimiter=' ')
			# Iterate over each row in the csv using reader object
			for idx, row in enumerate(csv_reader):
				temp_res = {};
				# row variable is a list that represents a row in csv
				if idx == 0:
					# print(row);
					for r in row:
						# print(r, type(r), r.replace(' ', '|').replace('\t', '|').split('|'));
						for col in r.replace(' ', '|').replace('\t', '|').split('|'):
							if col:
								# print(col);
								headers.append(col);
					print('headers', headers);
				else:
					col_idx = 0;
					for r in row:
						for col in r.replace(' ', '|').replace('\t', '|').split('|'):
							if col:
								key = headers[col_idx];
								temp_res[key] = col;
								col_idx += 1;
				result.append(temp_res);
	except Exception as e:
		Logger.e('File.readTxtToDF', e);
		print('file:', file);

	df = pd.DataFrame(result, dtype=str);
	df = df.dropna(axis=0, how='all');
	return df;

def readXlsToDF(file):
	result = [];
	df = pd.DataFrame();
	converted_file = file.replace('.xls', '.xlsx');
	# print('converted_file', converted_file, os.path.exists(converted_file) )
	if os.path.exists(converted_file):
		df = readExcelToDF(converted_file);
	else:
		try:
			book = xlrd.open_workbook(file,encoding_override="cp1251")  
		except Exception as e:
			print('ex', e)
			try:
				book = xlrd.open_workbook(file)
			except Exception as e:
				print('nested', e);
				book = None;
		if book:
			# print("The number of worksheets is {0}".format(book.nsheets))
			# print("Worksheet name(s): {0}".format(book.sheet_names()))
			sh = book.sheet_by_index(0)
			# print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
			# print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
			headers = [];
			for rx in range(sh.nrows):
				# print(sh.row(rx))
				if rx == 0:
					# print('0 type', type(sh.row(rx)));	
					for header in sh.row(rx):
						headers.append(header.value);
				else:
					obj_ = {};
					for idx, row_data in enumerate(sh.row(rx)):
						# handle datetime column change to timestamp
						if row_data.ctype == 3:
							try:
								dt = datetime.datetime(*xlrd.xldate_as_tuple(row_data.value,
													  book.datemode));
								row_data_value = int((dt - datetime.datetime(1970, 1, 1)) / datetime.timedelta(seconds=1))
								row_data_value = DateTime.toString(DateTime.convertDateTimeFromTimestamp(row_data_value));
							except Exception as e:
								Logger.e('Error converting date', e);
								row_data_value = row_data.value;
						else:
							row_data_value = row_data.value;
						obj_.update({
							headers[idx]: row_data_value,	
						});
					result.append(obj_);
		else:
			print('\n\nfile manually convert', file)

		if result:
			df = pd.DataFrame(result, dtype=str);
			df = df.dropna(axis=0, how='all');
	return df;

def readExcelToDF(file, engine=None, skiprows=None, sheet_name=0, nrows=None, dtype=str, usecols=None, header=0):
	try:
		if sheet_name != 0 and sheet_name is not None and type(sheet_name) == str:
			df = pd.DataFrame();
			df_dict = pd.read_excel(file, engine=engine, dtype=dtype, skiprows=skiprows, sheet_name=None, nrows=nrows, usecols=usecols, header=header);
			for tabname in df_dict.keys():
				if sheet_name == tabname.strip():
					df = df_dict[tabname];
					break;
		else:
			df = pd.read_excel(file, engine=engine, dtype=dtype, skiprows=skiprows, sheet_name=sheet_name, nrows=nrows, usecols=usecols, header=header);
		if type(df) == dict:
			for sheet in df.keys():
				df[sheet] = df[sheet].dropna(axis=0, how='all');
	except Exception as e:
		Logger.e('File.readExcelToDF', e);
		print('file:', file);
		df = pd.DataFrame();
	return df;

def readSlkToDF(file):
	try:
		parser = SylkParser(file);

		fbuf = StringIO();
		parser.to_csv(fbuf);

		test_results = fbuf.getvalue();
		TESTDATA = StringIO(test_results);
		df = pd.read_csv(TESTDATA, sep=",", dtype=str);
		df = df.dropna(axis=0, how='all');
	except Exception as e:
		Logger.e('File.readSlkToDF', e);
		print('file:', file);
		df = pd.DataFrame();
	return df;

def readMacroToDF(file, engine=None, skiprows=None, sheet_name=0):
	# try:
	# 	workbook = xlrd.open_workbook(file)
	# 	for sheet in workbook.sheets():
	#         with open('{}.csv'.format(sheet.name), 'wb') as f:
	#             writer = csv.writer(f)
	#             for row in range(sheet.nrows):
	#                 out = []
	#                 for cell in sheet.row_values(row):
	#                     try:
	#                         out.append(cell.encode('utf8'))
	#                     except:
	#                         out.append(cell)
	#                 writer.writerow(out)
	# except Exception as e:
	# 	Logger.e('File.readMacroToDF', e);
	# 	df = pd.DataFrame();

	try:
		df = pd.read_excel(file, engine=engine, dtype=str, skiprows=skiprows, sheet_name=sheet_name);
		df = df.dropna(axis=0, how='all');
	except Exception as e:
		Logger.e('File.readMacroToDF', e);
		print('file:', file);
		df = pd.DataFrame();

	return df;

def readParquetToDF(file, columns=None):
	try:
		df = pd.read_parquet(file, columns=columns);
		df = df.dropna(axis=0, how='all');
	except Exception as e:
		Logger.e('File.readParquetToDF', e);
		print('file:', file);
		df = pd.DataFrame();

	return df;

def writeToTxt(filename, data):
	fn.ensureDirectory('/'.join(filename.split('/')[:-1]), is_absolute=True);
	with open(filename, 'w') as f:
		f.write(data);
	f.close;

def writeToExcel(filename, data, sheets=None, index=False, startrow=0):
	fn.ensureDirectory('/'.join(filename.split('/')[:-1]), is_absolute=True);
	while True:
		try:
			writer = pd.ExcelWriter(filename, engine='xlsxwriter');
			if sheets:
				for sheet in sheets:
					df = data[sheet];
					df.to_excel(writer, sheet_name=sheet, index=index, startrow=startrow);
				writer.save();
			else:
				data.to_excel(writer, sheet_name='sheet1', index=index, startrow=startrow);
				writer.save();
			break;
		except Exception as ex:
			Logger.e(ex);
			Logger.v('Unable to write file. Please close file ({0}) to allow rewrite.'.format(filename));
			time.sleep(5);
		except (KeyboardInterrupt, SystemExit):
			return False;
	return True;

def extractMacro(macro_file, writer):
	os.system("vba_extract.py '{0}'".format(container_master_file));
	workbook  = writer.book;
	workbook.filename = macro_file;
	workbook.add_vba_project('./vbaProject.bin');
	return workbook;

def writeToMacro(filename, macro_file, temp_file, data, sheets=None, index=False):
	fn.ensureDirectory('/'.join(filename.split('/')[:-1]), is_absolute=True);
	while True:
		try:
			writer = pd.ExcelWriter(temp_file, engine='xlsxwriter');

			if sheets:
				for sheet in sheets:
					df = data[sheet];
					df.to_excel(writer, sheet_name=sheet, index=index);

				os.system("vba_extract.py '{0}'".format(macro_file));
				workbook  = writer.book;
				workbook.filename = filename;
				workbook.add_vba_project('./vbaProject.bin');
				writer.save();
			else:
				data.to_excel(writer, sheet_name='sheet1', index=index);
				os.system("vba_extract.py '{0}'".format(macro_file));
				workbook  = writer.book;
				workbook.filename = filename;
				workbook.add_vba_project('./vbaProject.bin');
				writer.save();
			writer.close();
			removeDirectory(temp_file, mode='file');
			break;
		except Exception as ex:
			Logger.e(ex);
			Logger.v('Unable to write file. Please close file ({0}) to allow rewrite.'.format(filename));
			time.sleep(5);
		except (KeyboardInterrupt, SystemExit):
			return False;
	return True;

def writeToParquet(filename, data, use_dictionary=False, engine='pyarrow', compression='snappy'):
	fn.ensureDirectory('/'.join(filename.split('/')[:-1]), is_absolute=True);
	while True:
		try:
			data.to_parquet(filename, use_dictionary=use_dictionary, engine=engine, compression=compression)
			break;
		except Exception as ex:
			Logger.v('Unable to write file. Please close file ({0}) to allow rewrite.'.format(filename));
			Logger.e(ex);
			time.sleep(5);
		except (KeyboardInterrupt, SystemExit):
			return False;

def writeToCsv(filename, data, sep=',', index=False, chunksize=None, row_per_file=1000000, auto_split=False):
	fn.ensureDirectory('/'.join(filename.split('/')[:-1]), is_absolute=True);

	if auto_split == True:
		### auto split data when more than 1 million row
		list_of_dfs = [data.iloc[i:i+row_per_file-1,:] for i in range(0, len(data), row_per_file)]
		file_data = [];
		if len(list_of_dfs) == 1:
			file_data.append({
				'filename': filename,
				'data': data,	
			});
		else:
			folder = '/'.join(filename.split('/')[:-1]);
			filename_only = filename.split('/')[-1].split('.')[0];
			for idx, df in enumerate(list_of_dfs):
				part_name = 'part_{0}'.format(idx + 1);
				new_filename = '{0}/{1}_{2}.csv'.format(folder, filename_only, part_name);

				file_data.append({
					'filename': new_filename,
					'data': df,	
				});
		# print('file_data', file_data)
		# exit()
		for row in file_data:
			filename = row['filename'];
			data = row['data'];
			print('saving', filename)
			while True:
				try:
					data.to_csv(filename, sep=sep, index=index, chunksize=chunksize);
					break;
				except Exception as ex:
					Logger.v('Unable to write file. Please close file ({0}) to allow rewrite.'.format(filename));
					Logger.e(ex);
					time.sleep(5);
				except (KeyboardInterrupt, SystemExit):
					return False;
	else:
		while True:
			try:
				data.to_csv(filename, sep=sep, index=index, chunksize=chunksize);
				break;
			except Exception as ex:
				Logger.v('Unable to write file. Please close file ({0}) to allow rewrite.'.format(filename));
				Logger.e(ex);
				time.sleep(5);
			except (KeyboardInterrupt, SystemExit):
				return False;
	return True;

def convertCSVDelimter(file, from_delimiter=';', to_delimiter=',', replace=False):
	df = readCSVToDF(file, sep=from_delimiter);
	folder = '/'.join(file.split('/')[:-1]);
	filename = file.split('/')[-1].split('.')[0];
	if replace:
		output_filepath = file;
	else:
		output_filepath = '{0}/{1}_comma.csv'.format(folder, filename);
	writeToCsv(output_filepath, df, sep=to_delimiter);

def convertSingleFileToCSV(input_file, output_file):
	df = readToDF(input_file);
	if not df.empty:
		writeToCsv(output_file, df);
		df = pd.DataFrame();
		print('converted', output_file);

def convertToCSV(files, limit_count=None, sep=','):
	for row in files[:limit_count]:
		file = fn.getNestedElement(row, 'input_file');
		output_filepath = fn.getNestedElement(row, 'output_file');
		extension = file.split('.')[-1];
		if os.path.exists(output_filepath):
			pass;
		else:
			df = pd.DataFrame();
			if extension == 'csv':
				fn.ensureDirectory('/'.join(output_filepath.split('/')[:-1]).rstrip('/'), is_absolute=True);
				shutil.copy(file, output_filepath);
			elif extension == 'txt':
				df = readTxtToDF(file);
				pass;
			elif extension == 'xls':
				df = readXlsToDF(file);
				pass;
			elif extension == 'xlsx':
				df = readExcelToDF(file);
				pass;
			elif extension == 'slk':
				df = readSlkToDF(file);
			# elif extension == 'xlsm':
			# 	df = readMacroToDF(file);
			else:
				print('####################\n####################\n####################\nnew file extension', file, '\n####################\n####################\n####################\n')

			if not df.empty:
				fn.ensureDirectory(path='/'.join(output_filepath.split('/')[:-1]).rstrip('/'), is_absolute=True);
				print('saving', output_filepath);
				df.to_csv(output_filepath, index=False, sep=sep);

def getFilesFromDir(directory, include_subdir=True, folder_only=False):
	files = [];
	if include_subdir == True:
		for dirname, dirnames, filenames in os.walk(directory):
			for filename in filenames:
				if not filename.startswith('~') and not filename.startswith('.') and filename not in ['Thumbs.db', 'desktop.ini'] and not filename.endswith('.tmp'):
					full_filepath = os.path.join(dirname, filename);
					full_filepath = full_filepath.replace('\\', '/');
					files.append(full_filepath);
	else:
		if os.path.exists(directory):
			for filename in os.listdir(directory):
				if os.path.isfile(os.path.join(directory, filename)) and not filename.startswith('~') and not filename.startswith('.') and filename not in ['Thumbs.db', 'desktop.ini'] and not filename.endswith('.tmp'):
					full_filepath = os.path.join(directory, filename);
					full_filepath = full_filepath.replace('\\', '/');
					files.append(full_filepath);
				elif folder_only == True:
					full_filepath = os.path.join(directory, filename);
					full_filepath = full_filepath.replace('\\', '/');
					files.append(full_filepath);
	return files;

def removeDirectory(path, mode='directory'):
	if mode == 'file':
		try:
			os.remove(path)
		except OSError as e:  ## if failed, report it back to the user ##
			print ("Error: %s - %s." % (e.filename, e.strerror))
	elif mode == 'directory':
		try:
			# shutil.rmtree(path)
			for dirname, dirnames, filenames in os.walk(path):
				for filename in filenames:
					# print('delete', filename)
					full_filepath = os.path.join(dirname, filename);
					if os.path.isfile(full_filepath):
						# print('delete', full_filepath)
						os.remove(full_filepath);
		except OSError as e:
			print(path, e)
			print ("Dir Error: %s - %s." % (e.filename, e.strerror))
	else:
		try:
			os.remove(path)
		except OSError as e:  ## if failed, report it back to the user ##
			print ("Error: %s - %s." % (e.filename, e.strerror))

def getFileDateTime(file, mode='created_at'):
	if mode == 'updated_at':
		timestamp = os.path.getmtime(file);
	else:
		timestamp = os.path.getctime(file);
	result = DateTime.toString(DateTime.getDateTime(timestamp), date_format='%Y-%m-%d %H:%M:%S');
	return result;

def getCache(file):
	data = readCSVToDF(file);
	return data;

def setCache(file, data):
	writeToCsv(file, data);
	return getCache(file);

def organiseFiles(files, mode='product_master', month_mapping_required=True):
	result = [];
	mode_mapping = {
		'product_master': 'product_master',
		'itemized': 'itemize',
	};
	month_mapping = DateTime.monthMapping(mode='name_digit', name_length=3);
	for file in files:
		mode_name = mode_mapping[mode];
		split_file = file.lower().split('/');
		filename = split_file[-1];
		file_year = split_file[-3];
		if month_mapping_required:
			file_month = split_file[-2][:3];
			month_digit = str(month_mapping[file_month]).zfill(2);
		else:
			month_digit = split_file[-2];
		if mode_name in filename:
			# print(file_year, month_digit, file);
			result.append({
				'year_month': '{0}-{1}'.format(file_year, month_digit),
				'filepath': file,
			});
	return result;

def unzip(filepath, save_path=None):
	# root_path = fn.getRootPath();
	with zipfile.ZipFile(filepath, mode='r', compression=zipfile.ZIP_DEFLATED) as zip_ref:
		if save_path:
			directory_to_extract_to = save_path;
		else:
			directory_to_extract_to = '/'.join(filepath.split('/')[:-1]);
		# print('filepath', filepath, 'root_path', root_path)
		# zip_ref.extractall();
		zip_ref.extractall(directory_to_extract_to);
	# print('done unzip', filepath, directory_to_extract_to)
	return directory_to_extract_to;

def zipFiles(zip_path, file_list):
	zipObj = zipfile.ZipFile(zip_path, compression=zipfile.ZIP_DEFLATED, mode='w');
	for file in file_list:
		filename = file.split('/')[-1];
		zipObj.write(file, arcname=filename);
	zipObj.close();
	return zip_path;

def saveToWorkSheet(save_ws, output_file):
	fn.ensureDirectory('/'.join(output_file.split('/')[:-1]), is_absolute=True);
	while True:
		try:
			if save_ws:
				save_ws.save(output_file)
			else:
				sys.exit('Workbook not found.')
			break
		except Exception as ex:
			Logger.e(ex)
			Logger.v('Unable to write file. Please close testing file.')
			time.sleep(5)

def copyFile(source, destination):
	try:
		shutil.copy(source, destination)
		# Logger.v("File copied successfully.")
	
	# If source and destination are same
	except shutil.SameFileError:
		Logger.e("Source and destination represents the same file.")
	
	# If there is any permission issue
	except PermissionError:
		Logger.e("Permission denied.")
	
	# For other errors
	except:
		Logger.e("Error occurred while copying file.")

def closeAndSaveOpenpyxl(filepath, workbook):
	while True:
		try:
			workbook.save(filepath);

			break;
		except Exception as ex:
			Logger.v('Unable to write file. Please close file ({0}) to allow rewrite.'.format(filepath));
			Logger.e(ex);
			time.sleep(5);
		except (KeyboardInterrupt, SystemExit):
			return False;