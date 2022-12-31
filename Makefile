
clean: 
	rm -r output/*

_init: requirements.txt
	# 仮想環境を作成
	python -m venv myvenv
	conda deactivate
	source ~/.myvenv/bin/activate
	make install

install: requirements.txt
	pip install -r requirements.txt
