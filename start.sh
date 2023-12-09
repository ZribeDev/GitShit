AMOUNT=${1:-1}

for (( i=1; i<=AMOUNT; i++ ))
do
  python3 main.py
done

rm -rf temp