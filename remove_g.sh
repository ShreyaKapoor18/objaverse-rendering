for folder in combined_*.txt; do
  echo $folder
  python3 remove_second_line.py $folder
done

