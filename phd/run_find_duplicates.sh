for ID in {1..40}   
do
    python -m main/find_duplicates $ID 
    out=$?
    if [ $out -ne 0 ]; then
        exit
    fi
done
