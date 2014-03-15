"""
Commands to open up the python interpreter and run the script:

start>type cmd in the search area, press enter

cmd.exe will open up

You will likely be starting from C:\Users\Arthrod

You need to navigate to where your python executable is*

cd ..  # this command will take you up a folder in the directory.
cd ../.. # this will take you up two folders, and if you start in your user folder will take you all the way up to C:

dir # this will list out all the files and folders inside your current working directory

cd python27 # this will take you into the python folder, which lives in your C:/ path.  
You will want to store your programs and such in here for ease of use.

to run your script, just type in python [name of script] into the command line


* technically, no you don't, but doing this will save you from having to type in the full path later.  So just do this.

"""

#generic importing modules
import os, re, csv, collections
#os used to find file names
# re used for file name regex
# csv used to write csv file
# collections used for Counter()

# this section processes the search terms
mainpath = '/Users/Elizabeth/GoogleDrive/textfiles/' # main path to folder where the text files are


vocab = []#empty list to contain vocab

with open(mainpath + 'searchterms.txt','rt') as searchterms:
	searchterms = searchterms.readlines() #read the file and make a list containing each line as an element


for each in searchterms: #loop through the list work search terms
	if each == '\n' or each == '': 
		continue #skip lines that are only newlines or empty strings
	else:
		vocab.append(each.strip().lower()) #lowercase and strip the string, and append to vocab list

vocabcount = dict(collections.Counter(vocab))  # run the vocab list through the counter

for key, value in vocabcount.iteritems():
	# loop through the vocab counter dictionary
	if value >1: # if the value of the count is more than 1
		print key,"is a dupe" # report that it is a dupe

uniquevocab = list(set(vocab))  # make the vocab list a set, then conver that to a list, this effectively removes dupes
diff = len(vocab) - len(uniquevocab)  # calculates the diff lengths between vocab and uniques, this should give you how many
										# items were duplciates
if diff > 0:  # if the diff amount is more than 0, report that there were dupes
	print "WARNING!", diff, "items excluded for being dupes"
vocab = uniquevocab # just make vocab the unique list because I don't want to change the rest of the code



# this section collects the file names to process
paths = [] # declaring list to contain file paths
files = os.listdir(mainpath)

try:
	for each in files:
		# this loops through the list of file names and constructs your full file path list
		# tests to see if the file path ends in .txt.  File name is excluded if it does not
		# end in .txt.  This means you can safely add other files to this directory.
		# This also converts the file name to lowercase, so .txt and .TXT will work the same
		# should you need to have this work with something else, such as rtf, or what have you
		# you will need to change the if line to this:
		# if each.lower().endswith('txt','rtf')
		# basically, you will just add the additional file extensions in as strings

		if each.lower().endswith("txt"): # only open .txt files, add others after comma
			if each.lower() <> 'searchterms.txt': # don't open the searchterms.txt file
				paths.append(mainpath + each) #make the full path
except:
	print "something failed in pulling in the file names" #generic error to report if a file couldn't be opened


headers = ['File']  # making headers for printing, adding 'file' because that should be the first item displayed
for word in vocab:  #loop through the vocab list
	headers.append(word)  # add the vocab words to the headers



#loops through the files and counts the instances of each in each file

resultdict = {} # empty dictionary to throw results into.  This is the main result dict for the counts

for path in paths: #loop through the file paths
	filenamesearch = re.compile(r'.+/(.+\.[a-z]+)')  #compiling file name regex
	filename = re.findall(filenamesearch,path)[0]  #snag the file name using regex
	with open(path,'rt') as mytext: 
		mytext = mytext.read() #open and read the file into mytext
	results = {} # create empty dict to receive values
	for word in vocab: #loop through the vocab list
		results[word] = mytext.count(word) #count the instances of the vocab work, and add that value to the vocab word as key
	resultdict[filename] = results # add the completed dictionary to the main results dict, using file name as key

# this is the main printing code block for resultdict
 
numresults=[]  # container for result matrix, this will hold what will be the rows
				# one list per row

for obj in resultdict.iteritems(): # this will spit out the individual dictionaries out of the main dict as tuples
	# stuff at this level is working on the main result dictionary
	# first arg is string of path, second arg is a dictionary of results
	mydict = obj[1] # the individual result diciontary is the second arg, takes that dict object out and names it
					# naming it allows us to do stuff to it, else I'd have to keep calling obj[1] which is awful
	nums = [] #list to hold result values per file
	nums.append(obj[0]) # add the file name being looped through to the list, this will be the first element in the row
	# now we can start throwing values in
	for word in vocab: #iterate through words in vocab
		nums.append(mydict[word]) #use those words as a key (which they are) for the value lookup, add value to nums
	numresults.append(nums) # add the completed list to the result matrix



#write the whole mess to a csv
with open('searchresults.csv','wb') as f:
    f_csv = csv.writer(f) # make it a writer object
    f_csv.writerow(headers) #write the headers
    f_csv.writerows(numresults) # write the row values
#file will automatically close because of with