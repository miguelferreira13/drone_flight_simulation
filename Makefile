app:
	uvicorn app:app --host 0.0.0.0 --port 8000

run: clear-logs
	python src/simulation.py

clear-logs:
	rm -f log.db 

setup: 
	./setup.sh