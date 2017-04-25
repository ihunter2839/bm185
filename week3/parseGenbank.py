from Bio import SeqIO
import sys
import gzip
import re

outfile = open("eColiInfo.txt", "w")

for seq_record in SeqIO.parse(sys.argv[1], "gb"):
    #get the features list for the current record
    feat = seq_record.features
    #f is a seqFeature object
    for f in feat:
        #if the current feature is a coding sequence
        if "CDS" in f.type:
            #string to hold formated information
            outstring = ""
            if "protein_id" in f.qualifiers:
                outstring += str(f.qualifiers["protein_id"])[2:-2] + '\t'
            else:
                outstring += "Sudo gene" + '\t'
            #snag the values. I know this code is horribly ugly
            #but it is a work-in-progress script
            outstring += str(f.location)[1:-4] + '\t'
            outstring += str(f.strand) + '\t'
            outstring += str(f.qualifiers["gene"])[2:-2] + '\t'
            outstring += str(f.qualifiers["locus_tag"])[2:-2] + '\t'
            outstring += str(f.qualifiers["gene_synonym"])[2:-2] + '\t'
            if "product" in f.qualifiers:
                outstring += str(f.qualifiers["product"])[2:-2] + '\t'
            else:
                outstring += "psuedo" + '\t'
            taxIDString = feat[0].qualifiers["db_xref"][0]
            taxIDMatch = re.search("[0-9]+", taxIDString)
            outstring += taxIDMatch.group(0) + '\t'
            if "EC_number" in f.qualifiers:
                ec = f.qualifiers["EC_number"]
                ecString = ""
                for e in ec:
                    ecString += e + ","
                outstring += ecString[:-1] + '\t'
            if "db_xref" in f.qualifiers:
                db = f.qualifiers["db_xref"]
                dbString = ""
                for d in db:
                    dbString += d + ","
                outstring += dbString[:-1] + '\t'
            outfile.write(outstring + '\n')










