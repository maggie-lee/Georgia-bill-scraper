# Georgia-bill-scraper

Contents: 

billscrape.py scrapes bills in the Georgia legislature

sankeygabills.py sorts bills into separate spreadsheets by their final status: like vetoed, passed one committee, signed by governor, etc.

index.html and associated files draw a Sankey diagram, using D3.js.
The diagram shows what happens to bills in the Legislature.

Then that gets annotated and fixed up in Photoshop. <a href="https://raw.githubusercontent.com/greencracker/Georgia-bill-scraper/master/sankey16_export.png target="_blank">See it here.</a>
  
Footnotes:

In the 80 working days of the 2015-2016 term of the Georgia Legislature at the Gold Dome in Atlanta, lawmakers filed 4,834 bills and resolutions.

More than half of that was honors, like recognizing peach queens, rock stars and other good folks of Georgia.

The rest, well, most of the rest died when the term expired a half-hour late, at about 00:30 on March 25. This is the breakdown.

“All bills and resolutions filed” counts everything: bills, resolutions, prefiles, hoppers, duplicates. I got that count from a scraper

“All honorary resolutions” are the ones that just honor, recognize or send condolences to folk. They do dozens of these a day and pass them all in a block with one vote. Every year there are a few that are filed too late to get approved.

“All legislation that makes a policy point” is everything else. I chose to make that broad, including regular bills, constitutional amendments, study committees, urging resolutions, encouraging resolutions and, yes, road namings.

A Python script sorted and filtered all these bills into the different groups and spit out the numbers you see here.  

For example, if a bill got filed made a policy point, it got filtered to the orange box. Then if at any time its status was "passed," it got filtered to the light green box, "passed by at least one chamber." If it got one House passage and one Senate passage, it got "passed both chambers."  If it had been assigned to the local legislature committees, it got classified local. If it got vetoed, well, you get the picture.

AND, note, like Mark Twain said, there are lies, damned lies and statistics, so take any number out from under the Gold Dome with a grain of salt anyway. For example, legislators can cram many different things into one sausage casing. Say you file HB1 and HB2.  Then you cut all the language out of them and paste it at the bottom of HB3, which becomes law.  Well, the logic looks like two bills failed and one passed.  Whereas in actual reality, three things passed, just all crammed into one vehicle.  I don’t know how to correct for that, but I also know it’s done oh, maybe a few dozen times a year. Not constantly. Or for another example, say a local bill gets filed as a general bill even though in content it is clearly a local bill? Well I don’t know how I’d catch that.  There may be some!

