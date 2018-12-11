#!/bin/bash

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
