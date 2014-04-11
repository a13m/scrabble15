#!/usr/bin/env python
"""
Creates gifs showing every successive scrabble move in a game.

Moves are defined simply by words, their start position and their
direction.

Copyright (c) 2014, Al Grant.
License: MIT
"""
from PIL import Image, ImageDraw, ImageFont

class ScrabbleMove:
   def __init__(self, startPos, word, direction):
      self.word = word
      self.startPos = startPos
      self.direction = direction

class ScrabbleBoardGif:
   valuePerLetter = { 1:["E" , "A", "I", "O", "N", "R", "T", "L", "S", "U" ],
                      2:["D", "G"],
                      3:["B", "C", "M", "P"],
                      4:["F", "H", "V", "W", "Y"],
                      5:["K"],
                      8:["J","X"],
                      10:["Q","Z"] }

   letterValue = {}

   for val in valuePerLetter:
      for letter in valuePerLetter[val]:
         letterValue[letter] = val

   lightColour = (249,238,206)
   darkColour = (249,238,120)

   letterOffset = { "G":-1, "H": -1, "I":3, "M":-2,"N":-1,"Q":-5, "W":-2, "Y":1, "Z":-3}
   numOffset = {"Z":-4.5, "Q":-4.5}

   font = ImageFont.truetype("SourceSansPro-Regular.otf", 25)
   fontSmall = ImageFont.truetype("SourceSansPro-Regular.otf", 10)

   def __init__(self):
      # 15 by 15 board with empty strings
      self.board = [['']*15 for i in range(15)]
      # In case we want to keep track of these later...
      self.lettersAvailable = list("aaaaaaaaabbccddddeeeeeeeeeeeeffggghhiiiiiiiiijkllllmm" \
              "nnnnnnooooooooppqrrrrrrssssttttttuuuuvvwwxyyz??".upper())

      self.boardImage = Image.open("emptyBoard.png")
      self.boardDraw = ImageDraw.Draw(self.boardImage)
      self.lastMove = None

   def DrawLetter(self, pos, letter, colour, fontColour):
      top = pos[1]*30 + 5
      left = pos[0]*27 + 5
      borderColour = (215,151,0)
      self.boardDraw.rectangle([left,top,left+26,top+29],fill=colour, outline=borderColour)
      letterPos = [left + 6,top - 3]
      if letter in self.letterOffset:
         letterPos[0]+=self.letterOffset[letter]
      valuePos = [left + 20,top + 16]
      if letter in self.numOffset:
         valuePos[0] += self.numOffset[letter]

      self.boardDraw.text(letterPos, letter, fill=fontColour, font=self.font)
      if self.board[pos[0]][pos[1]] != '?':
         #Blanks have no value...
         self.boardDraw.text(valuePos, str(self.letterValue[letter]), fill=(0,0,0), font=self.fontSmall)

   def DrawMove(self, move):
      # Draw over the last move with the light colour
      if self.lastMove != None:
         # [:] to copy position, because we'll be modifying it.
         pos = self.lastMove.startPos[:]
         for letter in self.lastMove.word:
            if self.board[pos[0]][pos[1]] == letter:
               self.DrawLetter(pos, letter, self.lightColour, (0,0,0))
            else:
               self.DrawLetter(pos, letter, self.lightColour, (150,0,0))
            if self.lastMove.direction == "DOWN":
               pos[1]+=1
            else:
               pos[0]+=1   
      
      # Draw new tiles in dark colour
      # [:] to copy position, because we'll be modifying it.
      pos = move.startPos[:]
      for letter in move.word:
         # check that we haven't already placed in this
         # position
         if self.board[pos[0]][pos[1]] == '':
            if letter in self.lettersAvailable:
               self.board[pos[0]][pos[1]] = letter
               self.DrawLetter(pos, letter, self.darkColour, (0,0,0))
               self.lettersAvailable.remove(letter)
            elif '?' in self.lettersAvailable:
               self.board[pos[0]][pos[1]] = '?'  
               self.DrawLetter(pos, letter, self.darkColour, (150,0,0))
               self.lettersAvailable.remove('?')
            else:
               #uh oh...
               self.DrawLetter(pos, letter, self.darkColour, (0,150,0))
               self.lettersAvailable.remove(letter)
               print "missing a letter!"
                         
         if move.direction == "DOWN":
            pos[1]+=1
         else:
            pos[0]+=1   
      self.lastMove = move

   def Show(self):
      self.boardImage.show()
   
   def BoardCopy(self):
      return self.boardImage.copy()

if __name__ == '__main__':
   allBoards = [['circumambulated', 'cryptozoologies', 'mountaineerings', 'overidentifying', 'superabsorbents', 'dinoflagellates'],
             ['computerphobias', 'counterrallying', 'radiobiological', 'reinvigorations', 'glutaraldehydes', 'steadfastnesses'],
             ['dematerializing', 'disappointments', 'interbehavioral', 'interbehavioral', 'strongyloidoses', 'glutaraldehydes'],
             ['dematerializing', 'discontinuances', 'interbehavioral', 'interbehavioral', 'strongyloidoses', 'glutaraldehydes'],
             ['dematerializing', 'disappointments', 'interbehavioral', 'interbehavioral', 'strongyloidosis', 'glutaraldehydes'],
             ['dematerializing', 'discontinuances', 'interbehavioral', 'interbehavioral', 'strongyloidosis', 'glutaraldehydes'],
             ['dematerializing', 'disappointments', 'interbehavioral', 'interbehavioral', 'strongyloidoses', 'glyceraldehydes'],
             ['dematerializing', 'disappointments', 'interbehavioral', 'interbehavioral', 'strongyloidosis', 'glyceraldehydes'],
             ['hendecasyllabic', 'hyperaesthesias', 'straightforward', 'sedimentologist', 'superindividual', 'confrontational'],
             ['overextractions', 'overidentifying', 'radiobiological', 'nonmetropolitan', 'glutaraldehydes', 'subordinateness'],
             ['overextractions', 'overidentifying', 'recombinational', 'neocolonialisms', 'glutaraldehydes', 'superabsorbents'],
             ['overidentifying', 'overpersuasions', 'nonmetropolitan', 'sociobiological', 'subordinateness', 'glutaraldehydes'],
             ['overrepresented', 'overwithholding', 'recombinational', 'hyperfunctional', 'glutaraldehydes', 'disequilibrates'],
             ['paleobiologists', 'photoduplicated', 'overengineering', 'prepresidential', 'dehydrogenation', 'subvocalization'],
             ['parasitologists', 'photoduplicated', 'overengineering', 'prepresidential', 'dehydrogenation', 'subvocalization'],
             ['reactionaryisms', 'renationalizing', 'neurobiological', 'nonmetropolitan', 'glutaraldehydes', 'subordinateness'],
             ['republicanizing', 'revolutionaries', 'catheterization', 'interparoxysmal', 'subordinateness', 'glutaraldehydes'],
             ['republicanizing', 'revolutionaries', 'catheterization', 'interparoxysmal', 'subordinateness', 'glyceraldehydes']]

   #Draw the 8 letter words first!
   three = []
   fifteen_eight = {}

   for word in open("wordlists/scrabble15.words"):
       w = word.split()[0].strip()
       w8 = word.split()[1].strip()
       fifteen_eight[w.upper()] = w8.upper()

   for e,thisBoard in enumerate(allBoards):
      scrabbleGif = ScrabbleBoardGif()
      frames = []
      moves = [ScrabbleMove( [0,7],  thisBoard[3].upper(), "ACROSS"), 
               ScrabbleMove( [7,0],  thisBoard[2].upper(), "DOWN"), 
               ScrabbleMove( [0,0],  thisBoard[0].upper(), "ACROSS"), 
               ScrabbleMove( [0,0],  thisBoard[1].upper(), "DOWN"), 
               ScrabbleMove( [0,14], thisBoard[4].upper(), "ACROSS"), 
               ScrabbleMove( [14,0], thisBoard[5].upper(), "DOWN")]

      for move in moves:
         w8 = fifteen_eight[move.word]
         index = move.word.find(w8)
         w8Start = [i for i in move.startPos]
         if move.direction == "DOWN":
            w8Start[1] += index
         else:
            w8Start[0] += index

         scrabbleGif.DrawMove(ScrabbleMove(w8Start, w8, move.direction))
         frames.append(scrabbleGif.BoardCopy())
         scrabbleGif.DrawMove(move)
         frames.append(scrabbleGif.BoardCopy())
      scrabbleGif.DrawMove(moves[-1])     
      frames.append(scrabbleGif.BoardCopy())
      frames.append(scrabbleGif.BoardCopy())
      frames.append(scrabbleGif.BoardCopy())
      FRAME_DELAY = 1.25
      from images2gif import writeGif

      writeGif("gifs/board%02d.gif"%e,frames, duration=FRAME_DELAY, dither=0)