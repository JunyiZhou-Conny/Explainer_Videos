# keep only the text between Project Gutenberg's START and END marker lines (books without markers unchanged)
        start = input_text.find("*** START OF")
        if start != -1:
            input_text = input_text[input_text.index("\n", start) + 1:]
        end = input_text.find("*** END OF")
        if end != -1:
            input_text = input_text[:end]
