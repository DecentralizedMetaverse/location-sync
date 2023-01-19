start_time=`date +%s`
python3 main.py 1000 $1 $1 1000 1000 400.0 0 0 1000 | python3 main.py 1000 $1 $1 1000 1000 40.0 0 0 1000 | python3 main.py 1000 $1 $1 1000 1000 20.0 0 0 1000 | python3 main.py 1000 $1 $1 1000 1000 13.333333333333332 0 0 1000 | python3 main.py 1000 $1 $1 1000 1000 10.0 0 0 1000 | python3 main.py 1000 $1 $1 1000 1000 8.0 0 0 1000 | python3 main.py 1000 $1 $1 1000 1000 6.666666666666666 0 0 1000 | python3 main.py 1000 $1 $1 1000 1000 5.7142857142857135 0 0 1000 | python3 main.py 1000 $1 $1 1000 1000 5.0 0 0 1000 | python3 main.py 1000 $1 $1 1000 1000 4.444444444444445 0 0 1000 end_time=`date +%s`
run_time=$((end_time - start_time))
echo $run_time

