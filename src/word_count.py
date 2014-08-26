#!/usr/bin/env python
from __future__ import division
"""Word Cloud

Builds a cloud of words and outputs them as a png image

visit http://gitorious.org/projects/word-cloud to check out the latest repos

"""

__version__ = "0.1"
__license__ = "GNU Affero General Public License (AGPLv3)"

""" Visit http://www.gnu.org/licenses/agpl.txt for more information about
the Affero (Gnu3) license.  It's hot stuff
"""

__author__ = "Billy McClure <http://www.novembercamel.com>"
__contributors__ = ["David Arthur <>",]

# ------- system modules   ------------
import re, sys, os, random, math, time

# ------- required modules ------------
import Image, ImageFont, ImageDraw
import numpy

# ----- recommended modules -----------
try:
  import psyco
  psyco.full()
except:
  print "Install psycho...this is going to be painfully slow"


class WordCloud:    
    """
    This isn't a real word cloud as it only calculates a volume frequency and
    and not actual relative frequency (which I believe is a logrithmic function
    of time).  David can probably help with all the math for that as soon
    as we get data that is associated with time
    """
    def __init__(self):
      """
      Basic class properties.  We should move these into arguments instead, or
      at least allow an override through args
      """
      self.words = re.findall('[\w\'\-]+', open('../libs/mainline/words.txt', 'r').read())
      self.stopwords = re.findall('[\w\'\-]+', open('../libs/mainline/stop_words.txt', 'r').read())
      
      self.im_size = (800,800) #size of png output...for more words to fit
                               # you'll want to adjust this variable
                               
      self.build_matrix()      #see method for details...
      self.word_count_min = 3  #minimum frequency of word in word set
      self.word_length_min = 2 #minimum length of word (characters)
      self.start_font_size = 80
      self.stop_font_size = 10

    def fill_empty_space(self, spot, word_size):
      """
      A word has found a spot to sit, so fill in the binary matrix with
      flags where the word is.  The problem is that this is a square, and
      not all words fill in all the space, so large words look like they
      have padding
      """
      for i in range(spot[1], spot[1]+word_size[1]):
        for j in range(spot[0], spot[0]+word_size[0]):
          self.im_matrix[i,j] = 1
      """
      ********************************************************
      this section prints out a binary matrix of where the images
      are being placed.  it's pretty cool to see
      sorry for the double comments, vim hates me
      *********************************************************
      """
      #str = ""
      #for i in range(0, self.im_size[0]-1):
      #  print str
      #  str = ""
      #  for j in range(0, self.im_size[1]-1):
      #    str += "%d"%self.im_matrix[i,j]
      

    def find_empty_space(self, word_size, has_words=0, rand_row=True):
      """
      A few techniques implemented here:
      First, a random row (r) is chosen, image size of w,h
        If you want the image to be more condensed and flow
        from top to bottom, large to small, then set rand_row
        to False
      Second, look ahead w cols for 1(ones), starting at r,0,
        iterating through h rows.  If no 1(ones), store point,
        increment column position, and do again.  If there is a one,
        set the column position to right most one in the subset
        and do again
      If all rows are exhausted, send the word back to this
        function and avoid random row start position, instead,
        start at 0,0 and look again.
      STOP GATHERING POINTS ONCE YOU HAVE 100.  IF YOU DO NOT DO THIS
        THEN THE ALGORITHM TAKES F-ING FOREVER
      """
      # if there are no words in the picture yet, then place the
      #  first one in some random place
      if has_words == 0:
        spot= (random.randint(0, self.im_size[0]-word_size[0]-1),
               random.randint(0, self.im_size[1]-word_size[1]-1))
        self.fill_empty_space(spot, word_size)
        return spot

      clear_pts = [] # collection of points word fits in
      i = 0
      # reset the starting row to a random position to make the cloud
      #  seem much...cloudier?
      if rand_row is True:
        i = random.randint(0, int(self.im_size[1]-word_size[1]-1))
      while i <= self.im_size[1]-word_size[1]-1: # go through all rows
        j = 0
        if(len(clear_pts) > 100): break
        # now iterate through the column in steps of one, unless
        #  a 1(one) is found, then skip to it and keep searching
        while j+word_size[0]-1 <= self.im_size[0]-word_size[0]-1:
          clear_bound = True
          # iterate through each row of this column for the height
          #  of the image
          for k in range(i, i+word_size[1]-1):
            # if the sum of this bound is 0, then we're good
            row = self.im_matrix[k,j:j+word_size[0]-1]
            if(numpy.sum(row) > 0):
              t = numpy.transpose(numpy.nonzero(row))
              j = t[len(t)-1][0][1]+j
              #i = k
              clear_bound = False
              break
          if clear_bound is True:
            clear_pts.append((j,i))
          j += 1
        i += 1
      if len(clear_pts) is 0 and rand_row is False: 
        return None
      # the word failed to fit, so start from the beginning of
      #  the image, skipping random placement, and find a spot
      elif len(clear_pts) is 0 and rand_row is True:
        print "...random failed, trying to find a spot manually"
        return self.find_empty_space(word_size, 1, False)
      spot = clear_pts[random.randint(0, len(clear_pts)-1)]
      self.fill_empty_space(spot, word_size)
      return spot
        
    def make_image(self):
      """
      Create an image by placing words one at a time, starting with
      the "largest" into the area provided, if there is space available.

      Font is customizable - be sure to find the TTF or PIL for it, though
      a PIL will require a different ImageFont method to load it.

      If someone wants to mess around with the colors please do, though
      I really like the black on white
      """
      image = Image.new("RGB", self.im_size)
      draw = ImageDraw.Draw(image)
      # this should be made dynamic based on self.im_size
      font_size = self.start_font_size  
      
      l_cnt = 0       # last count, temp storage for comparison
      #alteration count - count of unique frequencies in the normalized
      #  word list.  so if "the" appears 3 times, "i" appears 3 times,
      #  and "he" appears 2 times, then alt_cnt = 2 i.e. (3,2)
      alt_cnt = len(set([y for x,y in self.norm_words]))
      d_alt_cnt = alt_cnt-1 # decrementer for exponential function
      for word,w_cnt in self.norm_words:
        # change the font here
        font = ImageFont.truetype("../libs/mainline/ARIAL.TTF", font_size)
        # this is just how big an area the box the word fits in takes up,
        #  it's a two v tuple.  Will probably be replaced when we figure
        #  out how to determine if the space is used by an actual white pixel
        #  instead
        word_size = font.getsize(word)
        print "placing %s %s"%(word, word_size)
        spot = self.find_empty_space(word_size, l_cnt)
        if spot is not None:
          draw.text(spot, word, font=font)
        else:
          # couldn't find an empty space after 500 attempts (fail)
          print "couldn't fit %s"%word
        
        # determine font size.  it's an exponential function that
        # degrades quickly (or is supposed to be).  This way the 
        # big words have large presence, while the insignificant
        # words fall out quickly, but are all relatively the same size
        if l_cnt is not w_cnt: 
          # this equation given to me by David Arthur
          font_size = int(math.ceil(self.stop_font_size* \
            (self.start_font_size/self.stop_font_size)**(d_alt_cnt/(alt_cnt-1))))
          d_alt_cnt = d_alt_cnt - 1
          l_cnt = w_cnt
          #print font_size
      fname  = "word_clouds/" + sys.argv[1] + "_word_cloud.png"
      image.save(fname, "PNG")

    def get_words(self):
      """
      Words are pulled in __init__...simply...if someone wants to wrap that 
      in a method and make it a more verbose action, please feel free.  we'll
      have to anyways when we move to an api reader.

      Words here filtered, counted, then reverse sorted.
      Filtered means that small words are removed, and words with a frequency
        of self.word_count_min are kicked out
      """
      counts = {}
      for w in self.words:
        w = w.lower()
        if w in self.stopwords: continue
        if len(w) <= self.word_length_min: continue
        if w not in counts: counts[w] = 0
        counts[w] = counts[w] + 1
      counts = sorted(counts.iteritems(), key=lambda(k,v):(v,k), reverse=True)
      self.norm_words = filter(lambda x: x[1] > self.word_count_min, counts)
      print self.norm_words
      self.norm_words = self.norm_words
      print "%d words to fit"%len(self.norm_words)

    def build_matrix(self):
      """
      My best shot at finding/recording space usage.  If someone can
      do this better please do.  I'm curious what kind of cool algorithms
      exist that are more efficient/successful than random guessing

      It's a binary matrix the size of the image.  If text gets put in, then
      the area a size of a box that contains the text, in the position it is
      placed, is then flagged so that no other words can then go there
      """
      self.im_matrix = numpy.asmatrix(numpy.zeros(self.im_size, numpy.int8))

usage = \
"""

"""
if __name__ == "__main__":
  st = time.time()
  wc = WordCloud()
  wc.get_words()
  wc.make_image()
  print time.time()-st," seconds"
