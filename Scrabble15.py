#!/usr/bin/env python
"""
Finds sets of six fifteen letter words which can fit on a 
scrabble board, using the scrabble letter distribution and based on eight 
letter words.

Copyright (c) 2011, Al Grant. (modified 2014)
License: MIT
"""

import sys

# Scrabble letter distribution
scrabbleLetters = "aaaaaaaaabbccddddeeeeeeeeeeeeffggghhiiiiiiiiijkllllmm" \
              "nnnnnnooooooooppqrrrrrrssssttttttuuuuvvwwxyyz??"
scrabbleList = [i for i in scrabbleLetters]

def makeScrabblableList(dictionary="wordlists/enable1.txt"):
   """
   Determines all fifteen letter words which have an eight
   letter word embedded in in it, and stores them in a text file
   called "scrabble15.txt".
   """
   eightletter = []
   fifteenletter = []   
   
   for word in open(dictionary):
      w = word.strip()
      if len(w) == 8:
         eightletter.append(w)
      elif len(w) == 15:
         fifteenletter.append(w)
  
   scrabble15 = open("wordlists/scrabble15.words", "w")
   
   for word15 in fifteenletter:
      for word8 in eightletter:
         if word8 in word15:
            scrabble15.write("%s %s \n"%(word15,word8))

def RemoveWordFromList(word, availableLetters):
   """
   Tries to remove each character in string word from the list of available 
   letters and returns the new list of letters or False if impossible.
   """
   # letters[:] creates a copy of the list
   lett = availableLetters[:]
   for char in word:
      if char in lett:
         # First try removing the actual character
         lett.remove(char)
      elif '?' in lett:
         # Otherwise try removing the wildcards "?".
         lett.remove('?')
      else:
         return False
   return lett

def scrabblable(sixWordLists, availableLetters):
   """
   Determines whether sets of six words which can actually be constructed 
   using the list of availableLetters.

   The sixWordLists input contains six lists which have all the 15 letter
   words which have the same first, middle and last letters. 
   [['snippersnappers','steadfastness', ... ], [ ... ], ... ]

   The algorithm iterates through the word lists, and creating a new set of
   potential solutions by checking every word to see if it can be added 
   using the available letters.
   """
   potentialSolutions = [[availableLetters,[]]]
   
   for wordList in sixWordLists:
      newPotentialSolutions = []
      for word in wordList:
         for sol in potentialSolutions:
            potentialSolution = RemoveWordFromList(word,sol[0])
            if potentialSolution != False:
               newPotentialSolutions.append(
                  [potentialSolution,sol[1] + [word]])
      potentialSolutions = newPotentialSolutions
   
   if potentialSolutions:
      return [i[1] for i in potentialSolutions]
   else:
      return None
      
def printable_board(words):
   """
   Given a list of words, (format specific to this program), 
   returns a board which can be output in a file or on the
   command line.
   """
   w = words

   bigString = " ".join(w[0]) + "\n"
   for i in range(1,7):
      bigString += "%s             %s             %s\n"%(w[1][i],
                                                         w[2][i],w[5][i])
   bigString +=  " ".join(w[3]) + "\n"
   for i in range(8,14):
      bigString += "%s             %s             %s\n"%(w[1][i],
                                                         w[2][i],w[5][i])
   bigString +=  " ".join(w[4])

   return bigString
            

if __name__ == '__main__':


   try:
      fifteenLetterWordList = open("wordlists/scrabble15.words")
   except:
      # If the scrabble15.words doesn't exist yet, try 
      # making a new one!
      makeScrabblableList()
      fifteenLetterWordList = open("wordlists/scrabble15.words")


   # Create the following dictionaries for easy lookup later.
   # Corresponds the fifteen letter word, to the eight letter word substring
   fifteen_eight = {}

   # All three letter combinations 'start,middle,end', no repeats i.e. 
   # ['sss','sls','sln', ...] for
   # *s*nipper*s*napper*s* = sss
   # *s*uperab*s*orbent*s* = sss
   # *s*trongy*l*oidose*s* = sls
   # *s*ubvoca*l*izatio*n* = sln
   three = []

   # dic_1 connects single character to all three letter combinations, i.e.
   # 's':['sss', 'sls', 'sln', ...]
   dic_1 = {}

   # dic_2 connects two characters to all three letter combinations, i.e.
   # 'ss':['sss', ...]
   # 'sl':['sls', 'sln', ...]
   dic_2 = {}

   # dic_3 connects all three characters sets to all fifteen letter words 
   # which it represents, i.e.
   # "sss": ['snippersnappers','superabsorbents', ...]
   dic_3 = {}

   for word in fifteenLetterWordList:
      w = word.split()[0].strip()
      w8 = word.split()[1].strip()
      
      fifteen_eight[w] = w8
      
      # Three letter combination
      tlc = w[0]+w[7]+w[14]
      
      if tlc[0] not in dic_1:
         dic_1[tlc[0]] = [tlc]
      else:
         if tlc not in dic_1[tlc[0]]:
            dic_1[tlc[0]].append(tlc)
         
      if tlc[0:2] not in dic_2:
         dic_2[tlc[0:2] ] = [tlc]
      else:
         if tlc not in dic_2[tlc[0:2]]:
            dic_2[tlc[0:2]].append(tlc)
         
      if tlc not in dic_3:
         dic_3[tlc] = [w]
      else:
         if w not in dic_3[tlc]:
            dic_3[tlc].append(w)
         
      if tlc not in three:
         three.append(tlc)
   
   
   maxCombinations = len(three)
   
   #nl are the nine intersecting letters
   #0...1...2
   #.       .
   #3...4...5
   #.   .   .
   #6...7...8
   nl = [None]*9 #nine letters
   
   
   
   goodcombos = []
   
   # General idea is to loop through every possible three letter combo, 
   # then use the dictionaries quickly confirm or deny other word 
   # combinations.
   
   # w1 through w6 are the six three letter combinations (recall multiple words 
   # have same three letter combo).
   #
   #    w2  w3  w6
   # w1 .........
   #    .   .   .
   # w4 .........
   #    .   .   .
   # w5 .........
   
   # Not particularly cleverly written, but gets the job done!
   # Starting at w1, tries to fill in w2, w3, w4, w5, w6 until it runs into
   # an issue.  If there's no issues it checks whether or not the words can
   # be built using the scrabble letter distribution.
   for e,w1 in enumerate(three):
      #Going through each three letter combination
      print "%s/%s"%(e,maxCombinations)
      
      nl[0:3] = w1
      
      if nl[0] in dic_1 and nl[1] in dic_1 and nl[2] in dic_1:
         # makes sure potential w2 and w3 exist, then try all combinations of 
         # w2 and w3 (using pre calculated dictionaries)
         for w2 in dic_1[nl[0]]:
            nl[3] = w2[1]
            nl[6] = w2[2]
            for w3 in dic_1[nl[1]]:
               nl[4] = w3[1]
               nl[7] = w3[2]
               if nl[3]+nl[4] in dic_2 and nl[6]+nl[7] in dic_2:
                  # make sure w4 and w5 can exist, 
                  # then try all combinations.
                  for w4 in dic_2[nl[3]+nl[4]]:
                     nl[5] = w4[2]
                     for w5 in dic_2[nl[6]+nl[7]]:
                        nl[8] = w5[2]
                        if nl[2]+nl[5]+nl[8] in dic_3:
                           # Finally check if w6 exists, if so try and 
                           # find combinations of words which can be
                           # made from the scrabble letter distribution.
                           combos = [  dic_3[w1], dic_3[w2], 
                                       dic_3[w3], dic_3[w4], 
                                       dic_3[w5], dic_3[nl[2]+nl[5]+nl[8]]]
                           good = scrabblable(combos, scrabbleList + nl)
                           if good:
                              for g in good:
                                 # g2 is diagonal inverse of g, trying not 
                                 # to duplicate patterns.
                                 g2 = [g[i] for i in (1,0,3,2,5,4)]
                                 if (g  not in goodcombos and 
                                     g2 not in goodcombos):
                                    goodcombos.append(g)
   
   # Saves good combinations to file, even displays texty scrabble board.
   solutionFile = open("wordlists/6scrabble15.words","w")
   for e,g in enumerate(goodcombos):
      # creates a list of strings showing the eight letter word within
      # the fifteen letter word, i.e.  de(material)izing
      m = ["%s(%s)%s"%(w[:w.index(fifteen_eight[w])],fifteen_eight[w] , 
            w[w.index(fifteen_eight[w]) + 8:]) for w in g]

      solutionFile.write("\n\n%d\n\n"%(e+1))
      solutionFile.write("%s\n %s\n %s\n\n %s\n %s\n %s\n\n"%(m[0],m[3],m[4],
                                                              m[1],m[2],m[5]))
      solutionFile.write(printable_board(g))
   