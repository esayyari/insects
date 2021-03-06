#! /usr/bin/env python
 
import os
import sys
import re
import subprocess as sub

name_pt = re.compile("(?<=[>])(.+)")
 
if ("--help" in sys.argv) or ("-?" in sys.argv) or len(sys.argv) < 1:
    sys.stderr.write("usage: %s <alignment-file-path> <alignment-type> [<results-file-path>]\n"%sys.argv[0])
    sys.exit(1)
altype = sys.argv[2]
sourcepath = os.path.dirname(os.path.abspath(__file__)) 
src_fpath = os.path.expanduser(os.path.expandvars(sys.argv[1]))
if not os.path.exists(src_fpath):
    sys.stderr.write('Not found: "%s"' % src_fpath)
simplifyfst=sourcepath+'/simplifyfasta.sh'
p = sub.Popen([simplifyfst,src_fpath],stdout=sub.PIPE,stderr=sub.PIPE)
simpl, errors = p.communicate()
if errors is not None and errors != "":
    print errors    
dest_fpath=None
if len(sys.argv) > 3:
    dest_fpath=os.path.expanduser(os.path.expandvars(sys.argv[3]))
    dest = open(dest_fpath, "w")
else:
    dest = sys.stdout

def counts(l):
	if (altype == "FNA"):
		x=l.lower()
		return (x.count('a'),x.count('c'),x.count('g'),x.count('t'),x.count('n'),x.count('-'))
	else:
		x=l.lower()
		return (x.count('-'),  x.count('x'), len(x))
if (altype == "FNA"):
	print >>dest, "%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" %("SEQUENCE","TAXON","A_C","C_C","G_C","T_C","N_C","frag_C","A_R","C_R","G_R","T_R","c1_A_C","c1_C_C","c1_G_C","c1_T_C","c1_N_C","c1_frag_C","c1_A_R","c1_C_R","c1_G_R","c1_T_R","c2_A_C","c2_C_C","c2_G_C","c2_T_C","c2_N_C","c2_frag_C","c2_A_R","c2_C_R","c2_G_R","c2_T_R","c3_A_C","c3_C_C","c3_G_C","c3_T_C","c3_N_C","c3_frag_C","c3_A_R","c3_C_R","c3_G_R","c3_T_R")
#print mapping
	try:
		seq=""
		for l in simpl.split("\n"):    
			if l.startswith(">"):
				seq=l[1:]
				seq2=seq.split("_")[0]
			else:
				if not l:
					continue
				a= [0, 0, 0, 0]
				c= [0, 0, 0, 0]
				g= [0, 0, 0, 0]
				t= [0, 0, 0, 0]
				n= [0, 0, 0, 0]
				d= [0, 0, 0, 0]
				(a[0],c[0],g[0],t[0],n[0],d[0]) = counts(l)
           			s = len(l)+0.00000000000001
				sc = s/3
            
				(a[1],c[1],g[1],t[1],n[1],d[1]) = counts(l[0::3])
				(a[2],c[2],g[2],t[2],n[2],d[2]) = counts(l[1::3])
				(a[3],c[3],g[3],t[3],n[3],d[3]) = counts(l[2::3])
				try:
					print >>dest, "%s %s %d %d %d %d %d %d %f %f %f %f %d %d %d %d %d %d %f %f %f %f %d %d %d %d %d %d %f %f %f %f %d %d %d %d %d %d %f %f %f %f" %(
                        	  		seq,seq2,
                                	  		a[0],c[0],g[0],t[0],n[0],d[0],a[0]/s,c[0]/s,g[0]/s,t[0]/s,
                                        	                 a[1],c[1],g[1],t[1],n[1],d[1],a[1]/sc,c[1]/sc,g[1]/sc,t[1]/sc,
                                                	                                  a[2],c[2],g[2],t[2],n[2],d[2],a[2]/sc,c[2]/sc,g[2]/sc,t[2]/sc,
                                                    	                                                a[3],c[3],g[3],t[3],n[3],d[3],a[3]/sc,c[3]/sc,g[3]/sc,t[3]/sc)
				except ZeroDivisionError as e:
					print >>sys.stderr, "%s %s ERROR" %(seq,seq2)
					print >>sys.stderr, "L:%s*\n%d %s" %(l, s, a)
	except RuntimeError as e:
		dest.close()
		if dest_fpath is not None:
			os.remove(dest_fpath)
		raise e
else:
	print >> dest,  "%s %s %s %s %s %s %s" %("SEQUENCE","TAXON","SEQUENCE_LENGTH","X_C","frag_C","X_R","frag_R")
	try:
		seq=""
		for l in simpl.split("\n"):
			if l.startswith(">"):
				seq=l[1:]
				seq2=seq.split("_")[0]
			else:
				if not l:
					continue
				X = 0
				d = 0
				t = 0
				(d, X, t) = counts(l)
				t = t + 0.0
				try:
					print >> dest, "%s %s %d %d %d %f %f" %(seq, seq2, t, X, d, X/t, d/t)
				except ZeroDivisionError as e:
					print >> sys.stderr, "%s %s ERROR" %(seq,seq2)
					print >>sys.stderr, "L:%s*\n%d %s" %(l, t, X)
	except RuntimeError as e:
		dest.close()
		if dest_fpath is not None:
			os.remove(dest_fpath)
		raise e
        
dest.close()
