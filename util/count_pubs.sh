for f in ~/_a/data/myphd/original/formatted-news/*
do
#    echo $f
    grep LOTW-PUB $f | wc -l
done        

