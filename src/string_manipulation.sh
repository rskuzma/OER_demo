#! /bin/bash
filename="$1"
thresh="$2"
name=${filename%.*}
extension=${filename##*.}
page1="_page1."
page2="_page2."
bin="_bin_"

filename_page_1=$name$page1$extension
filename_page_2=$name$page2$extension


filename_bin_page_1=$name$bin$thresh$page1$extension
filename_bin_page_2=$name$bin$thresh$page2$extension

echo "The filename: $filename"
echo "The thresh: $thresh"
echo "The name: $name"
echo "The extension: $extension"
echo "Put it together: $name.$extension"
echo "filename page 1: $filename_page_1"
echo "filename page 2 $filename_page_2"
echo "filename bin page 1: $filename_bin_page_1"
echo "filename bin page 2 $filename_bin_page_2"
echo "Converting OER: $filename, binarizing threshold: $thresh to json"
