for ID in {1..40}   
do
    echo 'printing' $ID
    python -m main/find_blocks $ID 'r7m2' 7 | sort > /home/sergey/_a/data/myphd/generated/blocks/nd_min7/$ID
    out=$?
    if [ $out -ne 0 ]; then
        exit
    fi
done
