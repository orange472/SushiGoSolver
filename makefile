SushiGo:
	echo "#!/bin/bash" > SushiGo
	echo "python3 test_sushi_go.py \"\$$@\"" >> SushiGo
	chmod u+x SushiGo