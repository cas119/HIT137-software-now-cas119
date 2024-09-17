'''Question 1 - Solved By Sayeed Anwar & A K M Shafiur Rahman;
Refined the code and Fixed Issues by Synthia Islam'''
# Github Link: https://github.com/cas119/HIT137-software-now-cas119

# -*- coding: utf-8 -*-

import csv
import os
import re
import pandas as pd
import spacy
import torch


from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from collections import Counter, defaultdict


# Task 1: Extract the text from multiple CSV files


class TextProcessor:
    '''Text Processor Class'''
    def __init__(self, output_directory, output_file, chunk_size=1024*1024):
        self.output_directory = output_directory
        self.output_file = output_file
        self.chunk_size = chunk_size
        self.output_path = os.path.join(output_directory, output_file)

    @staticmethod
    def create_output_directory(directory):
        """Create the output directory if it does not exist."""
        os.makedirs(directory, exist_ok=True)
        print("Created separate 'output' folder for result")

    def extract_csv_to_dataframe(self):
        """Return a list of DataFrames for CSV files in the current directory"""
        # Initialize an empty list to store DataFrames
        dfs = []
        # Get the current working directory
        current_directory = os.getcwd()
        print("Current Working Directory:", current_directory)

        # List all items in the directory
        items = os.listdir(current_directory)

        # Filter and check for CSV files, then read and store each one to dataframe
        for item in items:
            if os.path.isfile(os.path.join(current_directory, item)) and item.endswith('.csv'):
                file_path = os.path.join(current_directory, item)
                print(f"Reading {item}...")
                df = pd.read_csv(file_path)
                dfs.append(df)

        if not dfs:
            print("No CSV files found in the current directory.")
        return dfs

    # def extract_csv_from_zip(self):
    #     """Extract CSV files from the zip archive and return a list of DataFrames."""
    #     dfs = []
    #     with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
    #         for file_info in zip_ref.infolist():
    #             if file_info.filename.endswith('.csv'):
    #                 with zip_ref.open(file_info.filename) as file:
    #                     df = pd.read_csv(file)
    #                     dfs.append(df)
    #     return dfs

    @staticmethod
    def extract_and_clean_texts(dfs):
        """Extract and clean texts from a list of DataFrames and return a generator of cleaned texts."""
        for df in dfs:
            if 'TEXT' in df.columns:
                for text in df['TEXT'].dropna():
                    yield TextProcessor.clean_text(text)

    @staticmethod
    def clean_text(text):
        """Clean text by removing non-English characters and extra spaces."""
        cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        return cleaned_text.strip()

    def process_texts(self, dfs):
        """Process and clean texts from CSV files and save the combined cleaned text."""
        if not dfs:
            print("No data available for processing")
        else:
            self.create_output_directory(self.output_directory)

            with open(self.output_path, 'w', encoding='utf-8') as outfile:
                for cleaned_text in self.extract_and_clean_texts(dfs):
                    outfile.write(cleaned_text + '\n')
                print("'combined_texts.txt' file is created")


# zip_path = './CSV.zip'
output_directory = './output'
output_file = 'combined_texts.txt'

processor = TextProcessor(output_directory, output_file)
dfs = processor.extract_csv_to_dataframe()
processor.process_texts(dfs)

# Task 2: Install the necessary libraries

print("Installing...")
# !pip install spacy
# !pip install scispacy
# !pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_core_sci_sm-0.5.0.tar.gz
# !pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_ner_bc5cdr_md-0.5.0.tar.gz
# !pip install transformers
print("Done.")

# Task 3.1: Count the Top 30 most common words


class WordAnalyzer:
    '''Word Analyzer Class'''
    def __init__(self, file_path, chunk_size=1024*1024, word_number=30):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.word_number = word_number

    def count_words(self):
        """Count the occurrences of words in the file."""
        word_counter = Counter()

        with open(self.file_path, 'r', encoding='utf-8') as infile:
            while True:
                chunk = infile.read(self.chunk_size)
                if not chunk:
                    break

                # Process chunk
                words = chunk.split()
                word_counter.update(words)

        return word_counter.most_common(self.word_number)

    @staticmethod
    def save_to_csv(top_words, output_csv_path):
        """Save the top words and their counts to a CSV file."""
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Word', 'Count'])
            writer.writerows(top_words)

    def process(self, output_csv_path):
        """Run the word count and save the results to a CSV file."""
        top_words = self.count_words()
        self.save_to_csv(top_words, output_csv_path)


# Word Analyzer Result
file_path = './output/combined_texts.txt'
output_csv_path = './output/top_30_words.csv'

analyzer = WordAnalyzer(file_path)
analyzer.process(output_csv_path)
pd.read_csv('./output/top_30_words.csv').head(5)


# Task 3.2: Use AutoTokenizer from transformers and Count 30 most common tokens

class TokenAnalyzer:
    '''Token Analyzer Class'''
    def __init__(self, file_path, tokenizer_name="bert-base-uncased", chunk_size=512, token_number=30):
        self.file_path = file_path
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, clean_up_tokenization_spaces=True)
        self.chunk_size = chunk_size
        self.token_number = token_number

    def count_tokens(self):
        """Count the occurrences of tokens in the file."""
        token_counts = Counter()

        with open(self.file_path, 'r', encoding='utf-8') as infile:
            while True:
                chunk = infile.read(self.chunk_size)
                if not chunk:
                    break

                # Process chunk
                tokens = self.tokenizer.tokenize(chunk)
                token_counts.update(tokens)

        return token_counts.most_common(self.token_number)

    @staticmethod
    def save_to_csv(top_tokens, output_csv_path):
        """Save the top tokens and their counts to a CSV file."""
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Token', 'Count'])
            writer.writerows(top_tokens)

    def process(self, output_csv_path):
        """Run the token count and save the results to a CSV file."""
        top_tokens = self.count_tokens()
        self.save_to_csv(top_tokens, output_csv_path)


# Token Analyzer Result
file_path = './output/combined_texts.txt'
output_csv_path = './output/top_30_tokens.csv'

analyzer = TokenAnalyzer(file_path)
analyzer.process(output_csv_path)
pd.read_csv('./output/top_30_tokens.csv').head(5)


# Task 4: Named-Entity Recognition (NER)

# ***SciSpacy & en_ner_bc5cdr_md***

# ***BioBert***


class EntityAnalyzer:
    '''Entity Analyzer Class'''
    def __init__(self, file_path, chunk_size=1000000):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load spaCy model
        self.spacy_model_name = "en_ner_bc5cdr_md"
        self.nlp = spacy.load(self.spacy_model_name)

        # Load BioBERT model and tokenizer for disease NER
        self.biobert_model_disease = AutoModelForTokenClassification.from_pretrained("ugaray96/biobert_ncbi_disease_ner").to(self.device)
        self.biobert_tokenizer_disease = AutoTokenizer.from_pretrained("ugaray96/biobert_ncbi_disease_ner")

        # Load ClinicalNER-PT model and tokenizer for drug NER
        self.drug_model = AutoModelForTokenClassification.from_pretrained("pucpr/clinicalnerpt-chemical").to(self.device)
        self.drug_tokenizer = AutoTokenizer.from_pretrained("pucpr/clinicalnerpt-chemical")

        # Initialize NER pipelines for both disease and drug models
        self.biobert_ner_disease = pipeline("ner", model=self.biobert_model_disease, tokenizer=self.biobert_tokenizer_disease, device=0 if torch.cuda.is_available() else -1)
        self.drug_ner = pipeline("ner", model=self.drug_model, tokenizer=self.drug_tokenizer, device=0 if torch.cuda.is_available() else -1)

        self.spacy_diseases = {}
        self.spacy_drugs = {}
        self.biobert_diseases = {}
        self.biobert_drugs = {}

    def _process_text_with_spacy(self, text_chunk):
        """Process a text chunk with spaCy to extract diseases and drugs."""
        doc = self.nlp(text_chunk)
        for ent in doc.ents:
            if ent.label_ == "DISEASE":
                self.spacy_diseases[ent.text] = self.spacy_diseases.get(ent.text, 0) + 1
            elif ent.label_ == "CHEMICAL":
                self.spacy_drugs[ent.text] = self.spacy_drugs.get(ent.text, 0) + 1

    def _process_text_with_biobert(self, text_chunk):
        """Process a text chunk with BioBERT to extract diseases and drugs."""
        biobert_entities_disease = self.biobert_ner_disease(text_chunk)
        for ent in biobert_entities_disease:
            if ent['entity'] == "Disease":
                self.biobert_diseases[ent['word']] = self.biobert_diseases.get(ent['word'], 0) + 1

        drug_entities = self.drug_ner(text_chunk)
        for ent in drug_entities:
            if ent['entity'] in ["B-ChemicalDrugs", "I-ChemicalDrugs"]:
                self.biobert_drugs[ent['word']] = self.biobert_drugs.get(ent['word'], 0) + 1

    def process_text_file(self):
        """Read the text file in chunks and process it with both spaCy and BioBERT models."""
        with open(self.file_path, 'r', encoding='utf-8') as infile:
            while True:
                chunk = infile.read(self.chunk_size)
                if not chunk:
                    break
                chunk = chunk.strip()
                if chunk:
                    self._process_text_with_spacy(chunk)
                    self._process_text_with_biobert(chunk)
                break  # Used To Reduce Time....Just Comment this line#

    def get_results(self):
        """Get total counts and most common entities from both models."""
        total_spacy_diseases = len(self.spacy_diseases)
        total_spacy_drugs = len(self.spacy_drugs)
        most_common_spacy_diseases = Counter(self.spacy_diseases).most_common(10)
        most_common_spacy_drugs = Counter(self.spacy_drugs).most_common(10)

        total_biobert_diseases = len(self.biobert_diseases)
        total_biobert_drugs = len(self.biobert_drugs)
        most_common_biobert_diseases = Counter(self.biobert_diseases).most_common(10)
        most_common_biobert_drugs = Counter(self.biobert_drugs).most_common(10)

        return {
            "total_spacy_diseases": total_spacy_diseases,
            "most_common_spacy_diseases": most_common_spacy_diseases,
            "total_spacy_drugs": total_spacy_drugs,
            "most_common_spacy_drugs": most_common_spacy_drugs,
            "total_biobert_diseases": total_biobert_diseases,
            "most_common_biobert_diseases": most_common_biobert_diseases,
            "total_biobert_drugs": total_biobert_drugs,
            "most_common_biobert_drugs": most_common_biobert_drugs
        }

    @staticmethod
    def save_results_to_files(results, results_directory):
        """Save the results to text files in the specified directory."""
        # Create subfolders for the results
        spacy_folder = os.path.join(results_directory, "SciSpacy", "en_ner_bc5cdr_md")
        biobert_folder = os.path.join(results_directory, "BioBERT")
        os.makedirs(spacy_folder, exist_ok=True)
        os.makedirs(biobert_folder, exist_ok=True)

        # Save spaCy results
        with open(os.path.join(spacy_folder, 'total_entities.txt'), 'w', encoding='utf-8') as f:
            f.write(f"Total diseases detected (spaCy): {results['total_spacy_diseases']}\n")
            f.write(f"Total drugs detected (spaCy): {results['total_spacy_drugs']}\n")

        with open(os.path.join(spacy_folder, 'most_common_diseases.txt'), 'w', encoding='utf-8') as f:
            for disease, count in results['most_common_spacy_diseases']:
                f.write(f"{disease}: {count}\n")

        with open(os.path.join(spacy_folder, 'most_common_drugs.txt'), 'w', encoding='utf-8') as f:
            for drug, count in results['most_common_spacy_drugs']:
                f.write(f"{drug}: {count}\n")

        # Save BioBERT results
        with open(os.path.join(biobert_folder, 'total_entities.txt'), 'w', encoding='utf-8') as f:
            f.write(f"Total diseases detected (BioBERT): {results['total_biobert_diseases']}\n")
            f.write(f"Total drugs detected (BioBERT): {results['total_biobert_drugs']}\n")

        with open(os.path.join(biobert_folder, 'most_common_diseases.txt'), 'w', encoding='utf-8') as f:
            for disease, count in results['most_common_biobert_diseases']:
                f.write(f"{disease}: {count}\n")

        with open(os.path.join(biobert_folder, 'most_common_drugs.txt'), 'w', encoding='utf-8') as f:
            for drug, count in results['most_common_biobert_drugs']:
                f.write(f"{drug}: {count}\n")

    def compare_and_save_results(self, results, results_directory):
        """Compare results from spaCy and BioBERT and save the comparison to a file."""
        comparison_diseases = defaultdict(lambda: {'spaCy_count': 0, 'BioBERT_count': 0})
        comparison_drugs = defaultdict(lambda: {'spaCy_count': 0, 'BioBERT_count': 0})

        # Update comparison dictionaries with results from spaCy
        for disease, count in self.spacy_diseases.items():
            comparison_diseases[disease]['spaCy_count'] = count

        for drug, count in self.spacy_drugs.items():
            comparison_drugs[drug]['spaCy_count'] = count

        # Update comparison dictionaries with results from BioBERT
        for disease, count in self.biobert_diseases.items():
            comparison_diseases[disease]['BioBERT_count'] = count

        for drug, count in self.biobert_drugs.items():
            comparison_drugs[drug]['BioBERT_count'] = count

        # Save comparison results
        comparison_folder = os.path.join(results_directory, "Comparison")
        os.makedirs(comparison_folder, exist_ok=True)

        with open(os.path.join(comparison_folder, 'disease_comparison.txt'), 'w', encoding='utf-8') as f:
            f.write(f"{'Disease':<30} {'spaCy Count':<15} {'BioBERT Count':<15}\n")
            f.write("="*60 + "\n")
            for disease, counts in comparison_diseases.items():
                f.write(f"{disease:<30} {counts['spaCy_count']:<15} {counts['BioBERT_count']:<15}\n")

        with open(os.path.join(comparison_folder, 'drug_comparison.txt'), 'w', encoding='utf-8') as f:
            f.write(f"{'Drug':<30} {'spaCy Count':<15} {'BioBERT Count':<15}\n")
            f.write("="*60 + "\n")
            for drug, counts in comparison_drugs.items():
                f.write(f"{drug:<30} {counts['spaCy_count']:<15} {counts['BioBERT_count']:<15}\n")

    def run(self, results_directory):
        """Run the analysis and save results."""
        self.process_text_file()
        results = self.get_results()
        self.save_results_to_files(results, results_directory)
        self.compare_and_save_results(results, results_directory)


# Entity Analyzer Result
file_path = './output/combined_texts.txt'
results_directory = './output/entity_analysis_results'

analyzer = EntityAnalyzer(file_path)
analyzer.run(results_directory)
