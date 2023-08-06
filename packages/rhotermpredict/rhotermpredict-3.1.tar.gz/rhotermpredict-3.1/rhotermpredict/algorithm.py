import re
import csv
import sys
import os
import argparse
import numpy as np
from copy import copy
from dataclasses import dataclass
from Bio import SeqIO
from Bio.Seq import Seq
from pathlib import Path


@dataclass
class RhoTermPredictResult:
    strand: str
    c_over_g: float
    start_rut: int  # x1
    end_rut: int    # x2
    term_seq: str
    downstream_seq: str
    palindromes: list
    pause_concensus: list
    scores: list

    def score_sum(self):
        return sum(self.scores)

def palindrome_finder(sequence, gc_genome=None, strand=None, score=None, calc="no"):
    n_rut = 0
    list_scores = []
    palindromes = []
    sequence = Seq(sequence)
    sequence_r = str(sequence.reverse_complement())
    _pattern_pause_site1 = r"GG\D{8}[C,T]G"
    _pattern_pause_site2 = r"C[G,A]\D{8}CC"
    for k in range(4, 8):
        for i in range(150):
            _x1 = i
            _y1 = i + k
            if _y1 > len(sequence):
                break
            else:
                window = sequence[_x1:_y1]
                window = str(window)
                gc_content = 100*(window.count("C")+window.count("G"))/len(window)
                score_p = score
                sub_sequence_r = sequence_r
                _start = 0
                while True:
                    if re.search(window, sub_sequence_r):
                        _research = re.search(window, sub_sequence_r)
                        _positions = _research.span()
                        _x2 = _positions[0]
                        _y2 = _positions[1]
                        sub_sequence_r = sub_sequence_r[_y2:]
                        _x2 += _start
                        _y2 += _start
                        _start += _y2
                        conseq = False
                        if 4 <= len(sequence)-_y2-_y1+1 <= 8:
                            if calc == "yes":
                                loop = len(sequence)-_y2-_y1
                                upstr = [_x1, _y1-1]
                                downstr = [len(sequence)-_y2, len(sequence)-_x2-1]
                                term_seq = window
                                score_p += 3
                                if gc_content > gc_genome + 20:
                                    score_p += 2
                                elif gc_content > gc_genome + 10:
                                    score_p += 1
                                if len(window) > 4:
                                    score_p += 1
                                if loop < 6:
                                    score_p += 1
                                if strand == 1:
                                    a = _x1-5
                                    b = len(sequence)-_x2+5
                                    seq_pause = str(sequence[a:b])
                                    if re.search(_pattern_pause_site1, seq_pause):
                                        score_p += 3
                                        conseq=True
                                elif strand == -1:
                                    a = _x1-5
                                    b = len(sequence)-_x2+5
                                    seq_pause = str(sequence[a:b])
                                    if re.search(_pattern_pause_site2, seq_pause):
                                        score_p += 3
                                        conseq=True
                                list_scores.append(score_p)
                                palindromes.append([upstr, downstr, term_seq, score_p, conseq])
                            else:
                                n_rut += 1
                    else:
                        break
    if calc == "yes":
        if len(list_scores) > 0:
            return np.max(list_scores), palindromes
        else:
            return 0, palindromes
    elif calc == "no":
        return n_rut, palindromes

def rho_term_predict(inseq = None, csv_out = None, text_out = None, quiet = True):
    """
    RhoTermPredict is a genome-wide predictor of transcription Rho-dependent terminators
    in bacterial genomes. It analyzes both the strands.

    :param inseq:
        List of sequences to analzye in string format
    :param csv_out:
        Path to the output - a xlsx file containing Rho-dependent terminators coordinates
    :csv_out:
        Path to the output - txt file containing informations about them
    """

    sequences_to_analyze = {}

    valid_string_check = re.compile('[ATGCU.-]', re.IGNORECASE)

    for i, sequence in enumerate(inseq):
        if not valid_string_check.match(sequence):
            raise ValueError(f'Sequence {i} is not a valid string of nucleotides')
        sequences_to_analyze[i] = sequence

    num_sequences = len(sequences_to_analyze)

    if not quiet:
        print(f"Sequences to analyze: {num_sequences}\n\n"
            f" RhoTermPredict is working, please wait...")
    final_list = []

    for _, genome in sequences_to_analyze.items():
        genome = genome.upper()
        gc_whole_genome = 100*(genome.count("G")+genome.count("C"))/len(genome)
        pattern1 = r"C\D{11,13}C\D{11,13}C\D{11,13}C\D{11,13}C\D{11,13}C"
        pattern2 = r"G\D{11,13}G\D{11,13}G\D{11,13}G\D{11,13}G\D{11,13}G"
        pattern_pause_site1 = r"GG\D{8}[C,T]G"
        pattern_pause_site2 = r"C[G,A]\D{8}CC"
        predictions = 0
        cg_value = []
        scores = []
        num = 1
        cod = 1

        # positive strand

        scale = 0
        for j in range(len(genome)):
            x1 = scale + j
            x2 = scale + j + 78
            if x2 > len(genome):
                break
            else:
                w = genome[x1:x2]
                if w.count("G") > 0:
                    numG = w.count("G")
                    c_over_g = w.count("C")/numG
                else:
                    numG = 1
                    c_over_g = (w.count("C")+1)/numG
                if c_over_g > 1:
                    if re.search(pattern1, w):
                        data = []
                        for g in range(50):
                            if x2+g <= len(genome):
                                w = genome[x1+g:x2+g]
                                if w.count("G") > 0:
                                    numG = w.count("G")
                                    c_over_g = w.count("C")/numG
                                else:
                                    numG = 1
                                    c_over_g = (w.count("C")+1)/numG
                                if c_over_g > 1:
                                    if re.search(pattern1, w):
                                        data.append(c_over_g)
                                    else:
                                        data.append(0)
                                else:
                                    data.append(0)
                            else:
                                break
                        maxP = np.argmax(data)
                        c_over_g = np.max(data)
                        x1 = x1 + maxP
                        x2 = x2 + maxP
                        pos1 = copy(x1)
                        pos2 = copy(x2)
                        scale = x2 - j - 1
                        s = genome[x2:x2+150]
                        w = genome[x1:x2]
                        score = 3
                        ctrl, _= palindrome_finder(s)
                        if ctrl > 0 or re.search(pattern_pause_site1, s):
                            num += 1
                            predictions += 1
                            scale = x2 + 150 - j - 1
                            cg_value.append(c_over_g)
                            if c_over_g > 2:
                                score += 3
                            elif c_over_g > 1.50:
                                score += 2
                            elif c_over_g > 1.25:
                                score += 1
                            cod += 1
                            final_score, palindromes = palindrome_finder(s, gc_whole_genome, 1, score, calc="yes")
                            final_score = float(final_score)
                            pause_consensus = []
                            while True:
                                if re.search(pattern_pause_site1, s):
                                    research = re.search(pattern_pause_site1, s)
                                    positions = research.span()
                                    x2 = positions[0]
                                    y2 = positions[1]
                                    found_PC = [x2, y2]
                                    s = s[y2:]
                                    pause_consensus.append(found_PC)
                                else:
                                    break
                            if final_score == 0:
                                final_score = score + 3
                            scores.append(final_score)
                            prediction = RhoTermPredictResult(strand = "+",
                                                                c_over_g = c_over_g,
                                                                start_rut=int(pos1),
                                                                end_rut=int(pos2),
                                                                term_seq = w,
                                                                downstream_seq=s,
                                                                palindromes=palindromes,
                                                                pause_concensus=pause_consensus,
                                                                scores = [float(palindrome[3]) for palindrome in palindromes])
                            final_list.append(prediction)

        # negative strand
        
        scale = 0
        for j in range(len(genome)):
            x1 = scale + j
            x2 = scale + j + 78
            if x2 > len(genome):
                break
            else:
                w = genome[x1:x2]
                if w.count("C") > 0:
                    numC = w.count("C")
                    c_over_g = w.count("G")/numC
                else:
                    numC = 1
                    c_over_g = (w.count("G")+1)/numC
                if c_over_g > 1:
                    if re.search(pattern2, w):
                        data = []
                        for g in range(50):
                            if x2+g <= len(genome):
                                w = genome[x1+g:x2+g]
                                if w.count("C") > 0:
                                    numC = w.count("C")
                                    c_over_g = w.count("G")/numC
                                else:
                                    numC = 1
                                    c_over_g = (w.count("G")+1)/numC
                                if c_over_g > 1:
                                    if re.search(pattern2, w):
                                        data.append(c_over_g)
                                    else:
                                        data.append(0)
                                else:
                                    data.append(0)
                            else:
                                break
                        maxP = np.argmax(data)
                        c_over_g = np.max(data)
                        x1 = x1 + maxP
                        x2 = x2 + maxP
                        pos1 = copy(x1)
                        pos2 = copy(x2)
                        scale = x2 - j - 1
                        s = genome[x1-150:x1]
                        w = genome[x1:x2]
                        score = 3
                        ctrl, _ = palindrome_finder(s)
                        if ctrl > 0 or re.search(pattern_pause_site2, s):
                            num += 1
                            predictions += 1
                            scale = x2 + 150 - j - 1
                            cg_value.append(c_over_g)
                            if c_over_g > 2:
                                score += 3
                            elif c_over_g > 1.50:
                                score += 2
                            elif c_over_g > 1.25:
                                score += 1
                            cod += 1
                            final_score, palindromes = palindrome_finder(s, gc_whole_genome, -1, score, calc="yes")
                            final_score = float(final_score)
                            start = 0
                            pause_consensus = []
                            while True:
                                if re.search(pattern_pause_site2, s):
                                    research = re.search(pattern_pause_site2, s)
                                    positions = research.span()
                                    x2 = positions[0]
                                    y2 = positions[1]
                                    s = s[y2:]
                                    x2 += start
                                    y2 += start
                                    pause_consensus.append(found_PC)
                                else:
                                    break
                            if final_score == 0:
                                final_score = score + 3
                            prediction = RhoTermPredictResult(strand = "-",
                                                                c_over_g = c_over_g,
                                                                start_rut=int(pos1),
                                                                end_rut=int(pos2),
                                                                term_seq=w,
                                                                downstream_seq=s,
                                                                palindromes=palindromes,
                                                                pause_concensus=pause_consensus,
                                                                scores = [float(palindrome[3]) for palindrome in palindromes])
                            final_list.append(prediction)
                            scores.append(final_score)
        if csv_out or text_out:
            _write_output(final_list, csv_out, text_out)
        elif not quiet:
            _print_results(final_list)

    if not quiet:
        print("RhoTermPredict has finished")
    return final_list

def _write_output(final_list, csv_file = None, text_file = None):
    if not csv_file and not text_file:
        raise ValueError("At least one of csv_file or text_file must be specified")

    cg_value = []

    class DummyWriter():
        """Dummy writer to avoid writing to file"""
        def write(self, *args):
            pass
        def writerow(self, *args):
            pass

    def _writer_handeler(csv_filestream, text_filestream):
        csv_filestream.writerow(['region', 'start_rut', 'end_rut', 'cg_ratio', 'strand', 'score_sum'])
        text_filestream.write("Sequences of predicted Rho-dependent terminators\n")
        predictions=0
        for i, terminator in enumerate(final_list):
            x1 = terminator.start_rut
            x2 = terminator.end_rut
            w = terminator.term_seq
            s = terminator.downstream_seq
            c_over_g = terminator.c_over_g
            scores = terminator.scores
            strand = terminator.strand

            text_filestream.write(f"\n\n\nPREDICTED REGION NUMBER T{i} (STRAND {strand})")
            text_filestream.write(f"\nGenomic sequence of putative RUT site (Coordinates:  {x1}-{x2}, g/c = {c_over_g})   {w}")
            text_filestream.write(f"\nThe 150 nt long genomic region immediately downstream is {s}")
            text_filestream.write("\n")
            for palindrome in terminator.palindromes:
                upstr = palindrome[0]
                downstr = palindrome[1]
                term_seq = palindrome[2]
                score = palindrome[3]
                conseq = palindrome[4]
                writestring = f"\nPalindromic sequences found at coordinates {upstr[0]}-{upstr[1]} e {downstr[0]}-{downstr[1]} (Sequence:   {term_seq})"
                if conseq:
                    writestring += " (PAUSE-CONSENSUS PRESENT)"
                writestring += f" (SCORE: {score})"
                text_filestream.write(writestring)
            for pause_concensus in terminator.pause_concensus:
                text_filestream.write(f"\n\nPAUSE-CONSENSUS present at the coordinates {pause_concensus[0]}-{pause_concensus[1]}")

            cg_value.append(terminator.c_over_g)
            predictions = i+1

            csv_filestream.writerow([f'T{i+1}', x1, x2, c_over_g, strand, sum(scores)])

        text_filestream.write(f"\n\n\nTotal number of predicted Rho-dependent terminators: {predictions}")
        text_filestream.write(f"\nMean C/G content of predicted terminators: {str(np.mean(cg_value))}")
        text_filestream.write(f"\nStandard deviation: {str(np.std(cg_value))}")


    if csv_file and text_file:
        with (open(csv_file, "w", encoding="utf-8") as csv_filestream,
            open(text_file, mode="w", encoding="utf-8") as text_filestream):
            csv_writer = csv.writer(csv_filestream, delimiter=',')
            _writer_handeler(csv_writer, text_filestream)
    elif csv_file:
        with open(csv_file, "w", encoding="utf-8") as csv_filestream:
            csv_writer = csv.writer(csv_filestream, delimiter=',')
            _writer_handeler(csv_writer, DummyWriter())
    elif text_file:
        with open(text_file, mode="w", encoding="utf-8") as text_filestream:
            _writer_handeler(DummyWriter(), text_filestream)

def _print_results(final_list):
    cg_value = []
    predictions = 0
    for i, terminator in enumerate(final_list):
        x1 = terminator.start_rut
        x2 = terminator.end_rut
        w = terminator.term_seq
        s = terminator.downstream_seq
        c_over_g = terminator.c_over_g
        scores = terminator.scores
        strand = terminator.strand

        print(f"\n\n\nPREDICTED REGION NUMBER T{i} (STRAND {strand})")
        print(f"\nGenomic sequence of putative RUT site (Coordinates:  {x1}-{x2}, g/c = {c_over_g})   {w}")
        print(f"\nThe 150 nt long genomic region immediately downstream is {s}")
        print("\n")

        for palindrome in terminator.palindromes:
            upstr = palindrome[0]
            downstr = palindrome[1]
            term_seq = palindrome[2]
            score = palindrome[3]
            conseq = palindrome[4]
            writestring = f"\nPalindromic sequences found at coordinates {upstr[0]}-{upstr[1]} e {downstr[0]}-{downstr[1]} (Sequence:   {term_seq})"
            if conseq:
                writestring += " (PAUSE-CONSENSUS PRESENT)"
            writestring += f" (SCORE: {score})"
            print(writestring)


        for pause_concensus in terminator.pause_concensus:
            print(f"\n\nPAUSE-CONSENSUS present at the coordinates {pause_concensus[0]}-{pause_concensus[1]}")

        cg_value.append(terminator.c_over_g)
        predictions = i+1

    if not predictions:
        print("Total number of predicted Rho-dependent terminators: 0")
        return

    print(f"\n\n\nTotal number of predicted Rho-dependent terminators: {predictions}")
    print(f"\nMean C/G content of predicted terminators: {str(np.mean(cg_value))}")
    print(f"\nStandard deviation: {str(np.std(cg_value))}")

def main():
    """CLI handeler for RhoTermPredict"""
    parser = argparse.ArgumentParser(description='RhoTermPredict (Barrick Lab Fork)')

    parser.add_argument(
        '-i', '--input',
        action='store',
        metavar='str/filepath',
        dest='i',
        required=False,
        type=str,
        help="Input filename (FASTA) or DNA/RNA sequence.",
    )

    parser.add_argument(
        '-o', '--output',
        action='store',
        metavar= 'filepath',
        dest='o',
        required=False,
        type=str,
        help="Output file path. If not provided, results will output to the console",
    )

    parser.add_argument(
        '-t', '--type',
        action='store',
        metavar='[string|csv|fasta]',
        dest='t',
        required=False,
        type=str,
        help="Input type (overrides autodetection)",
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        dest='q',
        required=False,
        help="Run quietly (default is False)",
    )

    args = parser.parse_args()
    cli_args = {'input': args.i, 'output': args.o, 'type': args.t, 'quiet': args.q}
    if not any(cli_args.values()):
        parser.print_help()
        sys.exit(0)

        # Determine input type
    input_type = None
    specified_file_exists = False
    valid_string_check = re.compile('[ATGCU.-]', re.IGNORECASE)
    if 'type' in cli_args.keys() and cli_args['type']:  # Manual override
        if cli_args['type'] == 'fasta':
            input_type = 'fasta'
        elif cli_args['type']  == 'string':
            input_type = 'string'
        else:
            print(f"Unsupported file type {cli_args['type']}.")
            sys.exit(1)

    elif os.path.isfile(cli_args['input']) and not input_type:  # Get input type from file name
        filepath_test = Path(cli_args['input']).suffix
        if filepath_test in ['.fasta', '.fa', '.fna']:
            input_type = 'fasta'
        else:
            with open(cli_args['input'], 'r') as in_file:   # Try to determine input type from file contents
                specified_file_exists = True
                first_line = in_file.readline()
                if first_line[0] == '>':
                    input_type = 'fasta'

    elif valid_string_check.match(cli_args['input']):  # Check to see if input is a valid sequence
        input_type = 'string'

    if input_type is None:   # Error out
        if specified_file_exists:
            print('Unable to identify the type of file specified as inout (-i). Please define it using "-t".', file=sys.stderr)
        else:
            print('Fix input (-i). Provided value does not specify an existing file and is not a valid nucleotide sequence.', file=sys.stderr)
        sys.exit(1)

    input_sequence = None
    if input_type == 'fasta':
        fasta_processed = parse_fasta(cli_args['input'])
        if len(fasta_processed) > 1:
            print('RhoTermPredict does not currently support multifasta. Please provide a single sequence.', file=sys.stderr)
            sys.exit(1)
        input_sequence = [fasta_processed[0][1]]
    elif input_type == 'string':
        input_sequence = [cli_args['input']]
    assert input_sequence is not None  # Programming check. Open issue if this happens.
    rhotermpredict_results = rho_term_predict(input_sequence, cli_args['output'], cli_args['quiet'])
    return rhotermpredict_results


def parse_fasta(filepath):
    '''Takes a filepath to a fasta formatted file and returns a list of [header, sequence].'''
    sequences = []
    current_seq_name = None
    current_seq = ""
    with open(filepath, 'r') as infile:
        for line in infile:
            linestr = str(line)
            if linestr[0] == '>':
                if current_seq_name:
                    sequences.append([current_seq_name, current_seq])
                current_seq_name = linestr[1:].rstrip()
                current_seq = str()
                continue
            else:
                current_seq += linestr.rstrip()
    if current_seq_name:
        sequences.append([current_seq_name, current_seq])
    return sequences



if __name__ == "__main__":
    main()
