all:
	make 2021
	make 2020
	make 2019
	make 2018


2021: main.py
	python main.py 2021 10

2020: main.py
	python main.py 2020 10

2019: main.py
	python main.py 2019 10

2018: main.py
	python main.py 2018 10

clean: 
	rm -r output/*

install: requirements.txt
	pip install -r requirements.txt
