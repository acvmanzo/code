import os

vid1 = 'cs_20130619_ag_A_l_1.avi'
vid2 = 'cs_20130619_ag_A_l_2.avi'
outvid = 'cs_20130619_ag_A_l.avi'

#cmd = 'ffmpeg -i cs_20130619_ag_A_l_1.MTS -i cs_20130619_ag_A_l_2.MTS -filter_complex "[0:0] [0:1] [0:2] [1:0] [1:1] [1:2] [2:0] [2:1] [2:2]   concat=n=3:v=1:a=2 [v] [a1] [a2]" -map "[v]" -map "[a1]" -map "[a2]" output.MTS'
  
#cmd = 
  #movie=part1.mp4, scale=512:288 [v1] ; amovie=part1.mp4 [a1] ;
#movie=part2.mp4, scale=512:288 [v2] ; amovie=part2.mp4 [a2] ;
#[v1] [v2] concat [outv] ; [a1] [a2] concat=v=0:a=1 [outa]


#ffmpeg -i vid1 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate1.ts
#ffmpeg -i input2.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate2.ts
#ffmpeg -i "concat:intermediate1.ts|intermediate2.ts" -c copy -bsf:a aac_adtstoasc output.mp4


cmd = 'ffmpeg -i concat:"{0}|{1}" -c copy {2}'.format(vid1, vid2, outvid)
print(cmd)
exitcode = os.system(cmd)
