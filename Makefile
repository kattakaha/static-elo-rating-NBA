
clean: 
	rm -r output/*

install: requirements.txt
	pip install -r requirements.txt
