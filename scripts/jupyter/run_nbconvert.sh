#!/bin/bash -x
set -ex

jupyter nbconvert  --to markdown "$1" --config jekyll_config.py --template=jekyll.tpl --Application.log_level='DEBUG'

outputpath=${1%.ipynb}

mv "$outputpath.md" $2
# postname=$(date +"%Y-%m-%d-")$(echo $outputname | tr " " -)
# mv "$outputpath.md" "../../_posts/$postname.md"

postname=$(basename "$1" .ipynb)
files_dir="$postname"_files
rm -rf "../../posts_assets/$files_dir"
mv  "$outputpath"_files ../../posts_assets/
