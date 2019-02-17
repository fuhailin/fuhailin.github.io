#!/bin/bash

current_date_time=`date "+%Y-%m-%d %H:%M:%S"`
# Themes config backup
cd themes/next/

# Update needmoreshare2
cd source/lib/needsharebutton
git pull

# Update fancyBox3 
cd ../fancybox
git pull

# Update lazyload
cd ../jquery_lazyload
git pull

# Back to the NexT theme folder
cd ../..

# 
# git add .
# git commit -m "Theme updated: $current_date_time"
# git push 
cd ../..

# Generate blog
hexo clean
hexo generate
# Copy to repository
hexo deploy
# Deploy
git add .
git commit -m "Site updated: $current_date_time"
git push --recurse-submodules=check
