'''
Find duplicate files in a directory
Run in windows 7 with python 2.7

Get the name of every file
Take the has of every file
    - Add it to the dict of hashes
Check if the hash has already been seen (is in dict already)
    - If it has, add it to the list of duplicates
Go over list of duplicates
    - Ask user what file to keep, other files are moved to duplicates folder
    - Enter number corresponding to the file to keep
    - If the file is an image, enter 's' to open it in the default viewer


'''

import hashlib
from time import time
import os
from PIL import Image

# Directories to work in
directory = "M:\\Images"
duplicate_dir = "M:\\Image_Duplicates"
decide_later_dir = duplicate_dir + '\\Review'



def get_file_names(directory):
    '''
    Get all the file names in a directory
    '''
    file_paths = []
    
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root,filename)
            file_paths.append(filepath)
            
    return file_paths

def find_duplicates(directory):
    '''
    Take the hash of every file
    If a hash is duplicated, the file exists somewhere else. Add it to the list of duplicates
    To avoid needing to feed in data piece by piece, only files under 500 MB are hashed.
    '''    
    
    hashes = {}
    duplicates = []
    large_files = []


    files = get_file_names(directory)
    num_files_total = len(files)
    num_dups = 0
    
    print('Total number of files to compute: {}'.format(num_files_total))
    
    start_time = time()
    file_counter = -1
    for f in files:
        file_counter += 1
        with open(f,'rb') as file_to_check:
            if os.stat(f).st_size < 5e8: # 500MB limit
                # if the file is too big, will get memory error
                # there are not too many of these files, so just note it
                data = file_to_check.read()
                f_hash = hashlib.sha256(data).hexdigest()
                #print('File: {}\t Hash: {}'.format(f,f_hash))
                
                if f_hash in hashes:
                    duplicates.append(f_hash)
                    hashes[f_hash].append(f)
                    num_dups +=1
                    print('Found duplicate f_hash: {}'.format(hashes[f_hash]))
                else:
                    hashes[f_hash] = [f]
            else:
                print('File too large to hash: {}'.format(f))
                large_files.append(f)
                
        if file_counter % 100 == 1:
            complete = float(file_counter)/float(num_files_total)*100.
            remaining = (time()-(start_time))/file_counter * (num_files_total-file_counter)
            print('{}/{}: {:.2f}% complete, {:.0f} seconds remaining'.format(file_counter,
                                                                              num_files_total,
                                                                              complete,
                                                                              remaining))

    print('\n\nFinished finding duplicate')
    print('Time Elapsed: {:.1f} seconds'.format(time()-start_time))
    print('Total number of duplicate files found: {}'.format(num_dups))
    
    return (hashes,duplicates,num_dups)
    
def choose_files(hashes,duplicates,duplicate_dir):
    '''
    List out the directories the duplicates are in
    If it is an image, show the image
    '''
    
    img_ext = ['.png','.jpeg','.jpg']
    #get list of duplicate hashes, unique only
    duplicates_unique = list(set(duplicates))
    #print('Duplicates_unique:{}'.format(duplicates_unique))
    
    for dup in duplicates_unique:
        f_counter = 0
           
        print('0:  Move files to review folder')
        for f in hashes[dup]:
            f_counter += 1
            print('{}: {}'.format(f_counter, f))
        
        
        # ask for the file to keep, make sure they enter a valid number
        valid_input = False
        while not valid_input:
            user_input = raw_input('Enter file to keep: ')
            if user_input.isdigit():
                id_to_keep = int(user_input)
                if id_to_keep <= len(hashes[dup]) and id_to_keep > 0:
                    f_keep = hashes[dup][int(user_input)-1]
                    move_duplicates(hashes[dup],f_keep,duplicate_dir)
                    valid_input = True
                    break
                    #print f_keep
                elif id_to_keep == 0:
                    move_all(hashes[dup],decide_later_dir)
                    f_keep = 'None'
                    valid_input = True
                else:
                    valid_input = False
            elif user_input.isalpha():
                if user_input == 's':
                    # get extension, if image, open it
                    ext = hashes[dup][0][hashes[dup][0].rfind('.'):].lower()
                    print('Extension: {}'.format(ext))
                    if ext in img_ext:
                        img = Image.open(hashes[dup][0])
                        img.show()
            else:
                valid_input = False
        
        
def move_all(fname_all,directory):
    '''
    Move all the files in fname_all to the specified directory
    '''
    f_counter = -1
    #print('fname_all: {}'.format(fname_all))
    for f in fname_all:
        #print('f: {}'.format(f))
        f_counter += 1
        fname = f[f.rfind('\\')+1:]
        period_loc = fname.rfind('.')
        fname = fname[:period_loc] + '_{}'.format(f_counter) + fname[period_loc:]
        new_name = directory + '\\' + fname
        os.rename(f,new_name)
    
def move_duplicates(fname_all,fname_keep,duplicate_dir):
    '''
     Move all files in fname_all except the specified file, fname_keep, to the duplicate directory
    '''
    f_counter = -1
    for f in fname_all:
        #print('fname_all: {}'.format(fname_all))
        #print('fname_keep: {}'.format(fname_keep))
        #print('f: {}'.format(f))
        if f != fname_keep:
            f_counter += 1
            fname = f[f.rfind('\\')+1:]
            period_loc = fname.rfind('.')
            fname = fname[:period_loc] + '_{}'.format(f_counter) + fname[period_loc:]
            new_name = duplicate_dir + '\\' + fname
            #print('Moving to: {}'.format(new_name))
            os.rename(f,new_name)
            
hashes,duplicates,num_dups = find_duplicates(directory)
choose_files(hashes,duplicates,duplicate_dir)
