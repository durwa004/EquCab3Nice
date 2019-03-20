#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 19:11:48 2019

@author: jonahcullen
"""
#Get list of contig IDs from MSI vcf
#import gzip

#Read in contig IDs from MSI horses
contig_list = list()
#with gzip.open("/home/mccuem/shared/Projects/HorseGenomeProject/Data/EquCab3/interval_bio_comparison/MSI_run_files/interval_bio_10_cases.vcf.gz", "rt") as input_file:
with open("/home/mccuem/shared/Projects/HorseGenomeProject/Data/EquCab3/interval_bio_comparison/MSI_run_files/interval_bio_10_cases.vcf", "r") as input_file:
    for line in input_file:
        if "#" in line:
            if "##contig" in line:
                contig,*_ = line.rstrip("\n").split(",")
                a = contig.split("=")
                contig_list.append(a[2])
        else:
            break

#Need to read in IDs from NCBI file and then create a dictionary of chr:NC_
id_map = {}
with open("GCF_002863925.1_EquCab3.0_assembly_report.txt", "r") as input_file:
    for line in input_file:
        if "#" in line:
            next
        else:
            nice,a,b,c,d,e,NCBI,*_ = line.rstrip("\n").split()
            if "chr" in nice:
                id_map[nice] = NCBI
            else:
                for i in range(len(contig_list)):
                    if NCBI in contig_list[i]:
                        id_map[contig_list[i]] = NCBI

#Now want to read in vcf and change from id_map[key] to id_map[value]
with open("/home/mccuem/shared/Projects/HorseGenomeProject/Data/EquCab3/interval_bio_comparison/MSI_run_files/interval_bio_10_cases.vcf", "r") as input_file:
    with open("/home/mccuem/shared/Projects/HorseGenomeProject/Data/EquCab3/interval_bio_comparison/MSI_run_files/interval_bio_10_cases_copy.vcf", "w") as output_file:
        for line in input_file:
            if "##contig" in line:
                contig,ID,chrom,*_ = line.rstrip("\n").split("=")
                chrom = chrom.split(",")
                chrom = chrom[0]
                swap = id_map[chrom]
                output_file.write(line.replace(chrom,swap))
            elif "#" in line:
                output_file.write(line)
            elif "chr" in line:
                chrom,*_ = line.rstrip("\n").split()
                swap = id_map[chrom]
                output_file.write(line.replace(chrom,swap)) 
            else:
                output_file.write(line)

