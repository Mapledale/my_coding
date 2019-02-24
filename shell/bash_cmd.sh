# to find all files with a specific string
# -r: recursive, -n: line#, -w: match the whole word, -l: return file names only
# --include --exclude: for files, --include-dir --exclude-dir: for directories
grep -rnw '/home/user/host/rfw_code/mROADM/tcli/' -e "txt"
grep --include=\*.{c,h} --exclude=*.o -rnw '/path/to/somewhere/' -e "pattern"
grep --exclude-dir={dir1,dir2,*.dst} -rnw '/path/to/somewhere/' -e "pattern"

# to replace 'bar' with 'bar' in all files 
sed -i -- 's/bar/bar/g' *baz*
sed -i -- 's/bar/bar/g' *.baz
find . -type f -exec sed -i 's/bar/bar/g' {} +
find . -type f -name "*baz*" -exec sed -i 's/bar/bar/g' {} +

# to rename all *.bar files to *.bar 
# (To check what the command would do without actually doing it, add "echo" before "mv")
# refer to http://mywiki.wooledge.org/BashFAQ/030
for f in ./*.bar; do mv "$f" "${f%.bar}.bar"; done
