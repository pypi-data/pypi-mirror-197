rm data/huge.jsonl
pip install jsonschema-inference
for i in {1..100}; do cat data/big.jsonl >> data/huge.jsonl; done
echo "start comparison..."
for i in 1 2 4 8;
    do 
        echo "nworkers=$i";
        time jsonschema-inference --jsonl data/huge.jsonl --verbose 0 --out result/huge.schema --nworkers $i;
        time jskiner --jsonl data/huge.jsonl --verbose 0 --out result/huge.schema --nworkers $i;
done
rm data/huge.jsonl