import numpy as np

# Import the guessable words list
egl = open("eligible_guesses_list.txt", "r")
esl = open("eligible_solutions_list.txt", "r")
eligible_guesses = egl.readlines()
potential_solutions = esl.readlines()

practice = potential_solutions[0:10]
practice.append('tiger')
n = 0
i = 1
depth = np.zeros(10)
initial_guess = 'lager'
    
for target in practice:
    
    # Loop through for up to 6 guesses
    for attempt in range(6):
    	target = target.strip()
    	print(target)
        
        # Set initial worst case remaining words
    	remaining_words_wc = len(potential_solutions)
    	srmat = {}
        
        # Set a list of eligible guesses
    	candidate_guesses = eligible_guesses[:100]
        
        # Choose 'snare' as first guess
    	if attempt == 0:
    		candidate_guesses = [initial_guess]
    
        # Cycle through eligible guesses
    	for candidate_guess in candidate_guesses:
             # List of patterns and solutions that would yield
             # that pattern for a candidate guess
    		pattern_dict = {}
            
    		for potential_solution in potential_solutions:
    			temp_ps = potential_solution
    			match_code = [0] * 5
                
    			for char_idx in range(5):
                    
                # Check if letter is in the right place
    				if candidate_guess[char_idx] == temp_ps[char_idx]:
    					match_code[char_idx] = 2
    					temp_ps = temp_ps[:char_idx] + "*" + temp_ps[char_idx+1:]
                        
                # Check if letter is in the word at all
    				if candidate_guess[char_idx] in temp_ps and match_code[char_idx] == 0:
    					match_code[char_idx] = 1
    					ind_app = temp_ps.find(candidate_guess[char_idx])
    					temp_ps = temp_ps[:ind_app] + "*" + temp_ps[ind_app+1:]
                        
                # Add pattern to the matrix of possible patterns
                # This happens if that pattern is absent
    			if tuple(match_code) not in pattern_dict:
    				pattern_dict[tuple(match_code)] = [potential_solution]
                    
                # This happens if that pattern is already present
    			else:
    				pattern_dict[tuple(match_code)].append(potential_solution)
    
            # Find the most popular pattern for that word
    		N = max([len(val) for val in pattern_dict.values()])
            
            # If the worst case scenario for a given word is less than the worst
            # case scenario for the current word, change the word.        
    		if N < remaining_words_wc:            
                # Update the proposed guess
    			chosen_word = candidate_guess  
                # Save the pattern dictonary for the proposed guess
    			chosen_pattern_dict = pattern_dict
                          
                # Update the worst case scenario we are trying to beat
    			remaining_words_wc = N        
        
        # Find the pattern for the target word 
    	for pattern, words in chosen_pattern_dict.items():
    		if target in list(map(str.strip, words)):
    			feedback = pattern
    			break
        
        # Trim the list of potential solutions by selecting the appropriate
        # list from the pattern dictionary
    	potential_solutions = chosen_pattern_dict[feedback]
        
        # If only one word remains, it's the solution
    	if len(potential_solutions) == 1:
    		print(f'Words solved: {n+1}')
    		depth[n] = i
    		n += 1
    		break
         
    	i += 1