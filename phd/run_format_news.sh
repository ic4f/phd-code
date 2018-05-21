# Formats news for all companies and writes to temp
t="/home/sergey/_a/data/myphd/original/formatted-news/"

for f in ~/_a/data/myphd/original/downloaded-news/*
do
    n=$(basename $f)
    echo "Processing $n" 
    python -m main.format_news $n $t  
    out=$?
    if [ $out -ne 0 ]; then
        echo 'Exiting process due to raised exception'
        exit
    fi
done
