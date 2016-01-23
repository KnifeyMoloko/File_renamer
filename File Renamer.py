# file renamer by Maciej Cisowski

"""
# OVERVIEW
This is a very basic program that's designed around the need to rename and index files of a given format with recurring strings in folder names, e.g. "string quartet" in large quantities, cleaning up folders etc. It can be easily modified to do the same with files only, or to lookup files in folders instead of folders. It uses discrete functions called in sequence, creates an output folder with indexed files and offers the option of deleting the input folders to complete the cleanup. The program is designed to work after being dropped in the root catalogue containing the folders with the renamed files, so it requires an already somewhat stuctured folder enviroment, e.g. /root/.../Pictures/...; use caution when using this, as it does remove input catalogues completely!

# PROGRAM LOGIC
The Main Loop of the program waits for a raw input of a lookup name and then sequentially calls the discrete functions:
--> checker: checks for the inputed name (and it's lowercase and uppercase versions) in the folders in the catalogue in which the program was executed, provides a list of the folders with that name
--> maker: creates an output folder named /[raw_input name]Output
--> filer: uses os.walk to list the files in the folders provided by checker
--> copier: copies the files one-by-one from the input folders to the output folder, giving a counter printout in the console
--> renamer: first, it removes the files that don't conform to the .jpg format (change if needed!) from the output folder; then it renames the remaining files with the provided [raw_input name] + index; runs a checksum function to check if it didn't delete something by mistake - it's pretty accurate, but still, use at your own risk

# USE

This is utility program I needed, so it's basic as fuck. The functions are discrete enough to be used on their own in other programs though and the whole thing can be modified easily to suit custom purposes. The defualt use is to bring a catalogue containing many folders of jpgs to some order.

# RUNNING TIME

Large files and extra large quantities of files may prove to be very time consuming for this program, as it does not use any multithreading or disk-use optimization techniques. It does it's thing one-by-one, but with file counts < 500 it's pretty fast (few minutes at most).""" 


import os, shutil, sys

#GLOBALS

lookup_name = raw_input()
folder_list = os.listdir(".")
lookup_folders = []
print lookup_name
dir_name = lookup_name + "Output"
directory = os.getcwd()
output_directory = directory + "/" + dir_name
input_filelist = []
checksum_flag = False

#FUNCS

def checker():
    for folder in folder_list:
        # cycle through folders in the working directory
        if lookup_name in folder or str.lower(lookup_name) in folder or str.upper(lookup_name) in folder:
            # when lookup_name is found, append the list of dirs for file moving
            lookup_folders.append(directory + "/" + folder + "/")
    return lookup_folders

def maker():
    # make a directory for the output files
    try:
        os.mkdir(dir_name)
    except OSError:
        pass
    return dir_name

def filer():
    for lookup in lookup_folders:
        for root, dirs, filenames in os.walk(lookup):
            for name in filenames:
                input_filelist.append(os.path.join(root, name))
    return input_filelist

def copier():
    count = 1
    print len(input_filelist)
    for f in input_filelist:
        src = f
        dst = output_directory
        shutil.copy2(src, dst)
        print str(count) + "/" + str(len(input_filelist))
        count += 1

def checksum(remove, rename):
    #run checksum to check if the number of input/output len is the same
    if len(rename) == len(os.listdir(output_directory)):
        print "Files copied successfully (len is equal)"
    else:
        print "File copy failed (len is not equal)"

def renamer():
    counter = 1
    working_folder = os.listdir(output_directory)
    total_files_to_rename = len(working_folder)
    files_to_rename = []
    files_to_remove = []
    renamed_files = []
    for p in working_folder:
        root, ext = os.path.splitext(p)
        if ext != ".jpg":
            files_to_remove.append(p)
        elif ext == ".jpg":
            files_to_rename.append(p)
    print "Files to rename: " + str(len(files_to_rename)), "/", "Files to remove: " + str(len(files_to_remove))

    for f in files_to_remove:
        os.remove(output_directory + "/" + f)
    for f in files_to_rename:
        try:
            sauce = output_directory + "/" + f
            renamed_files.append(f)
            destino = output_directory + "/" + lookup_name + " " + str(counter)
            os.rename(sauce, destino)
            counter += 1
        except IOError:
            pass
    # mini-checksum
    if len(renamed_files) == len(files_to_rename):
        print
        print "Files renamed:" + " " + str(len(renamed_files)), "/", "Files to rename: " + str(len(files_to_rename))
        print "RENAMING PATTERN APPLIED. FILES RENAMED. SKYNET ONLINE"
    checksum(files_to_remove, files_to_rename)
    folder_remover()
    return files_to_rename, files_to_remove, total_files_to_rename

def folder_remover():
    if checksum_flag == False:
        for folder in lookup_folders:
            print folder
            print
        print "Do you want the delete the above folders? (input: Y/N)"
        delete = raw_input()
        if delete == "Y":
            for folder in lookup_folders:
                shutil.rmtree(folder)
            print "Folder cleanup complete."
        else:
            print "Suit yourself"
            sys.exit()


#MAIN LOGIC
if __name__ == '__main__':
    checker()
    maker()
    filer()
    copier()
    renamer()
