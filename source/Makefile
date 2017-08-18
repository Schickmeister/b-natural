default:
	@echo "Coping files to /usr/local/b_natural"
	@mkdir /usr/local/b_natural
	@cp Interpreter.py /usr/local/b_natural
	@cp Parser.py /usr/local/b_natural
	@cp johann.py /usr/local/b_natural
	@echo "Making johann executable"
	@mv /usr/local/b_natural/johann.py /usr/local/b_natural/johann
	@chmod +x /usr/local/b_natural/johann
	@echo "Linking johann to /usr/local/bin"
	@ln -s /usr/local/b_natural/johann /usr/local/bin/johann
	@echo "Done!"

clean:
	@echo "Removing link at /usr/local/bin/johann"
	@rm /usr/local/bin/johann
	@echo "Removing directory /usr/local/b_natural"
	@rm -r /usr/local/b_natural