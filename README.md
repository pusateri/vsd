# vsd
HTML 5 Video Server using Python Django Framework

It is suitable for use with modern browsers that support HTML 5 video streaming.
If your player supports HTTP Live Streaming, you can use the Apple supplied mediafilesegmenter to create playlist (.m3u8) files.
Otherwise, you can use MPEG4 Video (.mp4, .m4v, etc.)

This project is based on Django 1.3.1 and Python 2.7.

It includes several management commands:

1. Use 'load_dl2' to import an XML file from Delicious Library 2 containing all of the videos.
2. Use 'build_tags' to create searchable tags based on
3. Use 'fetch_covers' to look for cover art at Amazon.

Cover art (front, back, thumbnails) is displayed if available.

Tags are searchable.
