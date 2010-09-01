#!/usr/bin/env python

import os
import getopt
import sys
import subprocess

# Function that goes through the folders and then calls itself
def explore_folder(folder_name, indentation):
  try:
    for entry in os.listdir(folder_name):
      print ('\t' * indentation) + entry

      # Formulating the parent folder name
      if folder_name == '.': parent = ''
      else: parent = folder_name + '/'
      
      # Calling the function that decompresses the files and deletes the others that are not .avi or .mkv
      decompress_and_delete(parent, entry, indentation)
      
      # Calling the function again
      explore_folder(parent+entry, indentation+1)
  except:
    pass
    
def decompress_and_delete(directory, file_name, indentation):
  if (directory <> '.DS_Store'):
      if 'part01' in file_name or '.r00' in file_name:
        
        # Decompressing the part**.rar or .r00 files
        print ('\t' * indentation) + "Decompressing file: " + file_name
        
        if directory == '':
          directory = '.'
          
        # Finding out which files are to be extracted
        files = os.popen('unrar l %s | cut -d " " -f 2' % file_name).readlines()
        files = [x.replace('\n', '') for x in files[7:-3]] # Da linha 7 até a ante penultima
        
        proc = subprocess.Popen(["unrar", "x", directory + '/' + file_name, directory], stdout=file(os.devnull, "w"))
        retcode = proc.wait()
        print ('\t' * indentation) + "Finished decompressing file: " + file_name
        
        # Deleting the files
        answer = raw_input("Delete all other files? [Y]es / [N]o: ")
        if answer.upper() == 'Y':
          for entry in os.listdir(directory):
            if (entry not in files):
                print "Deleting: %s" % entry
                os.system('rm ' + (directory + '/' + entry))
        

def main():
  # Interpreting the parameters
  o, a = getopt.getopt(sys.argv[1:], 'd:')
  opts = {}
  for k, v in o:
  	opts[k] = v

  # If the '-d' argument is defined, use the one passed as parameter
  if opts.has_key('-d'):
  	explore_folder(opts['-d'], 0)
  else:
    explore_folder('.', 0)

if __name__=="__main__":
  main()