# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 18:03:28 2017

@author: asus


Get list of every file in folder
    Verify names match
        if names match, compare md5
    

"""

import hashlib
import os



path1 = "N:\\"
path2 = "M:\\"

f_out_path = 'N:\\matching_20170705'

to_ignore_ext = []#to_ignore = ['.jpg','.jpeg','.png']
to_ignore_name = '$RECYCLE.BIN'

def get_file_names(directory,to_ignore_ext,to_ignore_name):
    '''
    Get all the file names in a directory
    '''
    file_paths = []
    roots = []
    filenames = []
    counter = 0
    for root, directories, files in os.walk(directory):
        
        for filename in files:
            if counter % 10000 == 0:
                print('Getting info on file {}'.format(counter))
            f_ext = filename[filename.rfind('.'):]
            if f_ext in to_ignore_ext:
                continue
            elif to_ignore_name in root:
                continue
            else:
                counter += 1
                filepath = os.path.join(root,filename)
                file_paths.append(filepath)
                roots.append(root)
                filenames.append(filename)
                
    return (roots, filenames, file_paths)


def generate_file_md5(fname, blocksize=2**24):
    m = hashlib.md5()
    with open(fname, "rb" ) as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update( buf )
    return m.hexdigest()


def compare_file_names(p1,p2,f_out_path,compare_hash=False):
    p2_letter = p2[0][0]
    p1_num_vals = len(p1) - 1
    counter = 0
    for ii in xrange(p1_num_vals,-1,-1):
        counter += 1
        if counter % 100 == 0:
            print('{}/{}, {:.2f}% complete On file {}'.format(counter,p1_num_vals,float(counter)/float(p1_num_vals)*100.0,p1[ii]))
        
        test_name = p2_letter + p1[ii][1:]
        p2_num_vals = len(p2) -1
        
        found_match = False
        for jj in xrange(p2_num_vals,-1,-1):
            files_same = False
            if p2[jj] == test_name:
                files_same = compare_file_hash(p1[ii],p2[jj],f_out_path)
                if files_same:
                    p2.pop(jj)
                    p1.pop(ii)
                    found_match = True
                    break
                
        if not found_match:
            print('Missing file: {}'.format(p1[ii]))
    with open(f_out_path + '_remaining_path1.txt','a') as f:
        for filename in p1:
            f.write('{}\n'.format(filename))
    with open(f_out_path + '_remaining_path2.txt','a') as f:
        for filename in p2:
            f.write('{}\n'.format(filename))

def compare_file_hash(f1,f2,f_out):
    
    p1_hash = generate_file_md5(f1)    
    p2_hash = generate_file_md5(f2)
    
    if p1_hash == p2_hash:
        with open(f_out + '_hash_match.txt','a') as f:
            f.write('{},{},{}\n'.format(f1,f2,p1_hash))
        return True
    else:
        with open(f_out + '_hash_no_match.txt','a') as f:
            f.write('{},{},{},{}\n'.format(f1,f2,p1_hash,p2_hash))
        return False
    
    

roots_1, filenames_1, file_paths_1 = get_file_names(path1,to_ignore_ext,to_ignore_name)
roots_2, filenames_2, file_paths_2 = get_file_names(path2,to_ignore_ext,to_ignore_name)

file_paths_1 = sorted(file_paths_1)
file_paths_2 = sorted(file_paths_2)

print('Number of files in path1: {} in {} folders'.format(len(roots_1),len(set(roots_1))))
print('Number of files in path2: {} in {} folders'.format(len(roots_2),len(set(roots_2))))

compare_file_names(file_paths_1,file_paths_2,f_out_path)




