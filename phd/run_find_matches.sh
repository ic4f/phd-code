#REQUIRED ARGS:
#1. company_id
#2. minimum match length
for ID in {1..40}   

do
    python -m main/find_matches $ID f1 m 7 7 f2 nd_min7
    out=$?
    if [ $out -ne 0 ]; then
        exit
    fi
done
