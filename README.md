# vsd
HTML 5 Video Server using Python Django Framework

It is suitable for use with modern browsers that support HTML 5 video streaming.
If your player supports HTTP Live Streaming, you can use the Apple supplied mediafilesegmenter to create playlist (.m3u8) files.
Otherwise, you can use MPEG4 Video (.mp4, .m4v, etc.)

This project is based on Django 1.3.1 and Python 2.7.

It includes several management commands:

1. Use 'load_dl2' to import an XML file from [Delicious Library 2](http://www.delicious-monster.com/get/) containing all of the videos. I haven't tried it with Delicious Library 3 export files yet.
2. Use 'build_tags' to create searchable tags based on keywords.
3. Use 'fetch_covers' to look for cover art at Amazon.

Cover art (front, back, thumbnails) is displayed if available.

Every screening by every user (video, start time, stop time, etc.) is saved every time a movie is played.
