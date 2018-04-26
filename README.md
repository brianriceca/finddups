# finddups

Wade recursively through a directory hierarchy looking for identical files. 

The algorithm is to find all the files with exactly the same size in bytes (except for zero length files, which are 
boring) and then, for all those files, checksum them and report the ones that have identical checksums.
