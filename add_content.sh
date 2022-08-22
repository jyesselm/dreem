echo "\n \n #################### \n     remove output/ \n ##################### \n \n "

rm -fr ~/src/dreem/output

echo "\n \n #################### \n     install DREEM \n ##################### \n \n "

pip3 install .

echo "\n \n #################### \n     run DREEM \n ##################### \n \n "
dreem -fq2 test/resources/case_1/r2.fastq -fq1 test/resources/case_1/r1.fastq -fa test/resources/case_1/ref.fasta \
--overwrite \
--RNAstructure_path /Users/ymdt/src/RNAstructure/exe \
--sample_info /Users/ymdt/src/dreem/test/resources/samples.csv \
--library_info /Users/ymdt/src/dreem/test/resources/case_1/library.csv \
#--temperature 
#--add_any_info

echo "\n \n #################### \n     test DREEM \n ##################### \n \n "

python3 my_test_zone.py
