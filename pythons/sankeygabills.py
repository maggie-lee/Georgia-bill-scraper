####
# This takes a .csv of bills in the Georiga General Assembly
# And returns several .csvs 
# Each of the .csvs contains a list of bills that match
# a certain status
# For example, a spreadsheet of all the bills that were vetoed
# Or a spreadsheet of all the bills that made it through
# one committee.
#
# The the result is published here: 
#
# http://maggielee.net/?p=2321
###


from tidylib import tidy_document
import mechanize
from bs4 import BeautifulSoup
import re
import html5lib
import pycurl
import csv
import pandas
import numpy
print "ok imports"


df = pandas.read_csv('merged16.csv')
#print df.dtypes

A = df # A = all legislation
#print A #4935 items FYI

A.to_csv("A.csv")

############ SPLIT A into B and C: honorary/admin res & debatable legislation
#
# B includes anything honorary or administrative, ie:
# - honoring, recognizing, congradulating, condoling resolutions
# - scheduling, inviting in the governor, etc. 
# (some of these are house & senate versions of the same honor, like "Surgons' Day")
#
# C is everything else, everything policy-related including:
# - study committees including those that only have to pass one chamber
# - substantive chamber rule changes
# - urging resolutions
# - encouraging resolutions
# - constitutional amendments
# - road dedications. Why road dedications? They are a "policy"-related thing inasmuch as if
# one passes, somebody, maybe the legislator, has to pony up for the sign. The state won't
# pay. The result is very many are filed, but few pass. 
#
###################

######## 2016 changes in method
#
# added "encouraging" resolutions to debatable legislation
#
# and note, some duplicates from like prefiled ones were also filed under other bill number.  and empty approps for some reason
############

B = A[
	(A.type == 'SR') | (A.type == 'HR') # choose all resolutions
	]

B = B[
	(B.hc == "HC: ") & (B.sc == "SC: ") |  # choose those with no committee
	(B.hc == "HC: Rules") & (B.sc == "SC: ") & (B.title.str.contains("invite") == True) # or invite resolutions, which go to Rules* 
	]


# * There is no counterpart to this rule in the Senate. The Senate assigned 9 things to Rules this year.
# 8 were study committees or constitutional amendments
# 1 was a resolution apologizing for slavery
# Because they assigned it to Rules, I've treated the resoultion just like the other 8. 
# and put it in the policy-related bucket

### exclude the ones that are other resolutions which are policy-related

study_committee_mask = (B.title.str.contains("study committee") == True)
B = B[~study_committee_mask]
#exclude study committees from B

study_committee_mask = (B.title.str.contains("Study Committee") == True)
B = B[~study_committee_mask]
#exclude Study Committees from B

rule_amendments_mask = (B.title.str.contains("amend") == True)
B = B[~rule_amendments_mask]
#exclude amendments to Senate rules from B

CA_mask = (B.title.str.contains("-CA") == True)
B = B[~CA_mask]
#exclude constitutional amendments from B

CA_mask_2 = (B.title.str.contains("- CA") == True)
B = B[~CA_mask_2]
#be really sure to exclude constitutional amendments from B

urge_mask = (B.title.str.contains(" urge") == True)
B = B[~urge_mask]

encourage_mask = (B.title.str.contains(" encourage") == True)
B = B[~encourage_mask]

#print B #2989

B['found'] = 1 #create a dummy column with marker 'found' 

C = A.merge(B, how='left') #do a left merge of A & B, which by default
#merges on common columns

C = C[pandas.isnull(C['found'])].drop('found', axis=1)
#filter C to just those items not found in B and kill the marker

#print C #1946
C.to_csv("C.csv")

B = B.drop('found', axis=1)
#kill the marker in B too

B.to_csv("B.csv")

############ SPLIT B into K & P -- successes and fails
# K = successful honorary/admin resolutions
# P = failed honorary/admin resolutions
##############

P = B # leave B alone and create P

P = P[
	(P.status.str.contains("Adopted") == False)
	] #get rid of all where adopted = false

P = P[
	(P.title.str.contains("invite") == False)
	] #get rid of all invite resolutions; their status will usually be "Read and Referred," which equals success

P = P[
	(P.status.str.contains("Transmit") == False)
	] #get rid of all "Senate transmits House" -- these are administrative & successful

# SR 704 condolences to Mr. John David was a duplicate of SR 522



P['found'] = 1

K = B.merge(P, how='left')
K = K[pandas.isnull(K['found'])].drop('found', axis=1)

P = P.drop('found', axis=1)

K.to_csv("K.csv")
P.to_csv("P.csv")

#print K #2982

########## SPLIT C into D & L  --  passed at least one chamber vs. dead
# D = debatable legislation that passed at least one chamber; including study 
# committees that need to pass only one chamber
# L = debatable legislation that died
############

D = C #create D and leave C alone


D = D[
	((D.type.str.contains("H") == True) & (D.sc != "SC: ")) |  # grab house legislation that has a senate committee
	((D.type.str.contains("S") == True) & (D.hc != "HC: ")) | # or grab senate legislation that has a house committee
	(D.type.str.contains("H") == True) & (D.status.str.contains("Adopted") == True) | #the things House or Senate adopted, which includes study committees, urging res
	(D.type.str.contains("S") == True) & (D.status.str.contains("Adopted") == True)
	]



# print D #863

D['found'] = 1

L = C.merge(D, how='left')
L = L[pandas.isnull(L['found'])].drop('found', axis=1)

#print L #1083

D = D.drop('found', axis=1)

D.to_csv("D.csv")
L.to_csv("L.csv")



########### SPLIT D into M & EF -- deads, locals and generals
# M: passed one chamber then died, including joint study committees
# E: locals that passed both chambers
# F: generals that passed both chambers * includes study committees that only needed to pass one chamber
#########

EF = D #let's keep E and F together for a minute before splitting them into locals and generals


EF = EF[
	(EF.status.str.contains("Act") == True) | #grab the ones that are enacted
	(EF.status.str.contains("Veto") == True)| #and the vetos; we'll filter them out later.
	(EF.status.str.contains("Effective") == True) | #and the ones that are in effect
	(EF.status.str.contains("Adopted") == True) | # and the ones that are adopted, like one-chamber study committees
	(EF.status.str.contains("Agreed") == True)  # and the back-and-forth ones they agreed to
	]


#print EF

EF['found'] = 1

M = D.merge(EF, how='left')

M = M[pandas.isnull(M['found'])].drop('found', axis=1)

EF = EF.drop('found', axis=1)

EF.to_csv("EF.csv")

M.to_csv("M.csv")

#print M

########## SPLIT EF into E & F -- bills that passed two chambers, split into locals & generals
# E: locals - in IGC & SLGO; if there's a mismatch, like IGC & Rules, it's in generals
# F: generals - all other combinations of committees
##########

E = EF

E = E[
	(E.hc.str.contains("Intragovernmental Coordination") == True) & #grab everything in IGC
	(E.sc.str.contains("State and Local Governmental Operations") == True) #and SLGO
]

E['found'] = 1

F = EF.merge(E, how='left')
F = F[pandas.isnull(F['found'])].drop('found', axis=1)
E = E.drop('found', axis=1)
#print F

E.to_csv("E.csv")


###### SPLIT H from E -- take out local vetoes
# H - local vetoes
######

H = E

H = H[
	(H.status.str.contains("Veto") == True) #grab the vetoes
	]

E.to_csv("E.csv")
F.to_csv("F.csv")
H.to_csv("H.csv")

#print H

######### SPLIT N from F -- take out general vetoes
# N - general vetoes
########

N = F

N = N[
	(N.status.str.contains("Veto") == True) #grab the vetoes
	]
#print N

N.to_csv("N.csv")

######### CREATE J -- all dead bills
# J - All dead bills 
# merge the following:
# P - dead honorary resolutions
# L - died, passed no chambers
# M - died after passing one chamber
# H - local vetoes
# N - general vetoes
###########

deads = [P, L, M, H, N] #list of deads
#print type(deads)

J = pandas.concat(deads)
J.to_csv("J.csv")

#print J

#### CREATE G - all new local & state laws
# G - all new local & state laws
# merge the following:
# E - successful locals 
# F - successful generals
# THEN SUBTRACT H & N -- the vetoes
#########

successfuls = [E, F]

G = pandas.concat(successfuls)
#print G

G = G[
	(G.status.str.contains("Veto") == False)
	]

#print G

G.to_csv("G.csv")

sankey_list = [         #stick em all in a list
	("A", len(A.index)),
	("B", len(B.index)),
	("C", len(C.index)),
	("D", len(D.index)),
	("E", len(E.index)),
	("F", len(F.index)),
	("G", len(G.index)),
	("H", len(H.index)),
	("J", len(J.index)),
	("K", len(K.index)),
	("L", len(L.index)),
	("M", len(M.index)),
	("N", len(N.index)),
	("P", len(P.index))
	]

print (sankey_list)


with open("sankey_table.csv", "wb") as fi: #and export it so D3 can pick it up!!
	writer = csv.writer(fi)
	writer.writerows(sankey_list)
