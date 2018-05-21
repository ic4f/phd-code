#Tokenizes news and releases for all companies
for n in {1..40}
do
    echo "PROCESSING COMPANY $n" 
    python -m main.write_tokens $n   
    out=$?
    if [ $out -ne 0 ]; then
        echo 'Exiting process due to raised exception'
        exit
    fi
done

