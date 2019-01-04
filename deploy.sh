#!/bin/bash

# Themes config backup
mkdir -p ./themes_bak/next
mkdir -p ./themes_bak/next/layout
mkdir -p ./themes_bak/next/layout/_macro
cp -f ./themes/next/_config.yml ./themes_bak/next/_config.yml
cp -f ./themes/next/layout/_layout.swig ./themes_bak/next/layout/_layout.swig
cp -f ./themes/next/layout/_macro/post.swig ./themes_bak/next/layout/_macro/post.swig


# Generate blog
hexo clean
hexo generate
# Copy to repository
hexo deploy
# Deploy
git add .
current_date_time=`date "+%Y-%m-%d %H:%M:%S"`
git commit -m "Site updated: $current_date_time"
git push
