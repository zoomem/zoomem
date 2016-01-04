while true; do
find ~/git_workplace/zoomem/zoomem_site/visualize/static/cpp_files* -type f -mmin +360 -delete
sleep 300
done
