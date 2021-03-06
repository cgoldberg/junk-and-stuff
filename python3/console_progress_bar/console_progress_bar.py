#!/usr/bin/env python3
#
#  console_progress_bar
#
#  Copyright (c) 2010-2011 Corey Goldberg (http://goldb.org)
#
#  License :: OSI Approved :: MIT License:
#      http://www.opensource.org/licenses/mit-license
# 
#      Permission is hereby granted, free of charge, to any person obtaining a copy
#      of this software and associated documentation files (the "Software"), to deal
#      in the Software without restriction, including without limitation the rights
#      to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#      copies of the Software, and to permit persons to whom the Software is
#      furnished to do so, subject to the following conditions:
#
#      The above copyright notice and this permission notice shall be included in
#      all copies or substantial portions of the Software.
#


"""
console_progress_bar.py - ascii command-line progress bar with percentage and elapsed time display


example usage:

        #!/usr/bin/env python3

        import console_progress_bar as pb

        # print a static progress bar:
        #  [##########       25%                  ]  15s/60s

        prog_bar = pb.ProgressBar(60)
        prog_bar.update_time(15)
        print(prog_bar)

        # print a dynamic updating progress bar on one line:
        #
        #  [################100%##################]  10s/10s
        #  done

        secs = 10
        prog_bar = pb.ProgressBar(secs)
        print('\nplease wait %d seconds...\n' % secs)

        # spawn asych (threads/processes/etc) code here that runs for secs.
        # the call to .animate() blocks the main thread.

        prog_bar.animate(secs)

        print('done')

""" 


import sys
import time



if sys.platform.lower().startswith('win'):
    on_windows = True
else:
    on_windows = False
    
    
    
class ProgressBar:
    def __init__(self, duration):
        self.duration = duration
        self.prog_bar = '[]'
        self.fill_char = '#'
        self.width = 40
        self.__update_amount(0)
    
    def animate(self, secs):
        for i in range(secs):
            if on_windows:
                print(self, end='\r')
            else:
                print(self, (chr(27) + '[A'))
            self.update_time(i + 1)
            time.sleep(1) 
        print(self)
        
    def update_time(self, elapsed_secs):
        self.__update_amount((elapsed_secs / float(self.duration)) * 100.0)
        self.prog_bar += '  %ds/%ss' % (elapsed_secs, self.duration)
        
    def __update_amount(self, new_amount):
        percent_done = int(round((new_amount / 100.0) * 100.0))
        all_full = self.width - 2
        num_hashes = int(round((percent_done / 100.0) * all_full))
        self.prog_bar = '[' + self.fill_char * num_hashes + ' ' * (all_full - num_hashes) + ']'
        pct_place = int((len(self.prog_bar) / 2) - len(str(percent_done)))
        pct_string = '%d%%' % percent_done
        self.prog_bar = self.prog_bar[0:pct_place] + \
            (pct_string + self.prog_bar[pct_place + len(pct_string):])

    def __str__(self):
        return str(self.prog_bar)
        
        
      

if __name__ == '__main__':
    
    # print a static progress bar
    #  [##########       25%                  ]  15s/60s

    p = ProgressBar(60)
    p.update_time(15)
    print('\nstatic progress bar:')
    print(p)
    
    
    # print a static progress bar
    #  [=================83%============      ]  25s/30s

    p = ProgressBar(30)
    p.fill_char = '='
    p.update_time(25)
    print('\nstatic progress bar:')
    print(p)
    
    
    # print a dynamic updating progress bar on one line:
    #
    #  [################100%##################]  10s/10s
    #  done
    
    secs = 10
    p = ProgressBar(secs)
    print('\n\ndynamic updating progress bar:')
    print('\nplease wait %d seconds...\n' % secs)
    
    # spawn asych (threads/processes/etc) code here that runs for secs.
    # the call to .animate() blocks the main thread.
    
    p.animate(secs)
    
    print('done')
    
    
    
"""
example output:


$ python3 console_progress_bar.py 

static progress bar:
[##########       25%                  ]  15s/60s

static progress bar:
[=================83%============      ]  25s/30s


dynamic updating progress bar:

please wait 10 seconds...

[################100%##################]  10s/10s
done

"""

    