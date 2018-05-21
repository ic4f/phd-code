for ID in {1..40}   
do
    python -m main/write_matches $ID f3 /home/sergey/_a/data/myphd/generated/html/f3/
    out=$?
    if [ $out -ne 0 ]; then
        exit
    fi
done
