for ID in {1..40}   
do
    echo 'filtering' $ID
    python -m main/filter_matches $ID f1 f3 7 
    out=$?
    if [ $out -ne 0 ]; then
        exit
    fi
done
