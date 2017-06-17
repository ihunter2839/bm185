import sys
import re
import json

metadata_data = open(sys.argv[1])
metadata_clin = open(sys.argv[2])
epi_genes_list = open(sys.argv[3]).read().split()
epi_genes = {}
#stick it in a dictioinary to speed up runtime 
for gene in epi_genes_list:
    epi_genes[gene] = True

meta_data = json.load(metadata_data)
meta_clin = json.load(metadata_clin)
    
case_2_exp = {}

#associate expression data to clinical information
for exp in meta_data:
    if "data_category" in exp and exp["data_category"] == "Transcriptome Profiling":
        file_id = exp["file_id"]
        l = exp["cases"][0]
        case_id = l["case_id"]
        case_2_exp[case_id] = file_id

case_2_clin = {}

for clin in meta_clin:
    file_id = clin["file_name"]
    l = clin["associated_entities"][0]
    case_id = l["case_id"]
    case_2_clin[case_id] = file_id

#generate expression matrix/ time to death vector for all patients
mat_string = raw_input("Save matrix to: ") 
mat_head = "header_" + mat_string
vec_string = raw_input("Save vector to: ")
vec_head = "header_" + vec_string
matrix_out = open(mat_string, "w")
matrix_head = open(mat_head, "w")
vector_out = open(vec_string, "w")
vector_head = open(vec_head, "w")
#flag to write the order of genes to header file 
write_matrix_header = True
#only iterate through cases with FPKM expression data
for case in case_2_exp.keys():
    #flag to check that necessary info was found
    skip = False

    clin_file_name = "clinic/" + case_2_clin[case]
    exp_file_name = "data/" + case_2_exp[case] + "/exp.txt"

    #time of life information
    clin_file = open(str(clin_file_name))
    clin_data = clin_file.read()
    #lf = "<clin_shared:days_to_last_followup[\s\w\d\.\=\"]+>([0-9]+)<\/"
    d = "<clin_shared:days_to_death[\s\w\d\.\=\"]+>([0-9]+)<\/"
    #d2lf = re.search(lf, clin_data)

    d2d = re.search(d, clin_data)
    if d2d == None:
        skip = True
    else:
        vector_head.write(case + '\n')
        vector_out.write(d2d.group(1) + '\n')

    #expression information
    if skip == False:
        exp_file = open(str(exp_file_name))

        curLine = exp_file.readline()[:-1]
        while curLine != "":
            #infile should be tab deliminted
            split = curLine.split('\t')
            #0 - gene id
            #1 - expression in FPKM
            gene_id_full = split[0]
            gene_id = gene_id_full.split(".")[0]
            exp_level = split[1]

            #only examine genes with known epigenetic function
            if gene_id in epi_genes:
                matrix_out.write(split[1] + '\t')
                if write_matrix_header == True:
                    matrix_head.write(split[0] + '\t')
            curLine = exp_file.readline()[:-1]

        #switch flag, only write the header once
        if write_matrix_header == True:
            matrix_head.write('\n')
            write_matrix_header = False

        matrix_out.write('\n')
