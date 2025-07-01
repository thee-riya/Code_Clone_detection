# 🔍 Code Clone Detection Using LLM Summaries

Welcome to **CodeClone-LLaMA** – an end-to-end pipeline for detecting code clones (functionally similar code snippets) by leveraging **Large Language Model (LLM) summaries**, sentence embeddings, and cosine similarity-based classification. This repository demonstrates how summarizing code into natural language lets you measure *semantic* similarity between code pairs — something traditional AST- or token-based approaches can struggle with.

---

## 🎯 Motivation

Code clones appear when developers copy-paste or reimplement similar logic. Detecting these clones is crucial for:

✅ Reducing bugs
✅ Improving maintainability
✅ Enabling large-scale refactoring
✅ Detecting plagiarism in educational or open-source contexts

Instead of directly comparing raw code tokens, this project uses an LLM (Meta LLaMA 3.1-8B) to **summarize the intent** of each code snippet, then measures similarity between summaries.

---

## ⚙️ Approach Overview

Our pipeline follows these high-level steps:

1️⃣ **Data Preparation**

* Use a collection of functions as raw input.
* Clone pairs of 6 types are present in the Big Clone Bench dataset: T1, T2, ST3, VST3, MT3, WT3\_T4.
* Sampling 300 pairs from each type for evaluation.

2️⃣ **Summarization**

* For each function in a pair, prompt an LLM to produce a concise natural-language summary explaining what the code does.

3️⃣ **Embedding**

* Transform each summary into a vector representation with a sentence transformer (`all-MiniLM-L6-v2`), capturing semantic meaning.

4️⃣ **Similarity Measurement**

* Compute cosine similarity between the summaries’ embeddings.
* Apply a threshold or classifier to decide if a pair is a clone.

5️⃣ **Evaluation & Visualization**

* Datasets contain true clone pairs (positives); hence, evaluation uses True Positives, False Negatives, and Recall as primary metrics.
* Visualize embeddings using t-SNE to observe clusters of clones.

---

## 🗂️ Project Structure

```
├── dataset/
│   ├── data.jsonl                # Original java functions or code snippets
├── summaries/
│   └── summary_pairs.csv         # LLM summaries saved after generation
├── results/
│   ├── results.json              # Evaluation results for each clone type
│   └── embeddings_tsne.png       # t-SNE visualization of summary embeddings
├── paper/
│   └── paper.pdf                 # Research papers used as baseline/reference
├── code_clone_detection.ipynb    # Main notebook orchestrating the entire pipeline
└── README.md                     # This file
```

---

## 🚀 Running the Pipeline

1️⃣ **Prepare the Dataset**

* Collect or curate raw functions in `dataset/data.jsonl`.
* Use the notebook to generate `generated_clone_pairs.csv`.

2️⃣ **Summarize with LLaMA**

* The notebook loads `meta-llama/Llama-3.1-8B` from Hugging Face.
* For each pair, prompt the model to produce summaries for both functions.

3️⃣ **Embed Summaries**

* Compute vector embeddings using `sentence-transformers/all-MiniLM-L6-v2`.

4️⃣ **Compute Similarities**

* For each pair, calculate cosine similarity between the two summaries’ embeddings.

5️⃣ **Classify & Evaluate**

* Apply a threshold or train a simple classifier.
* Evaluate classification metrics using your ground truth.

6️⃣ **Visualize Embedding Space**

* Reduce dimensions with t-SNE.
* Plot embeddings to see whether clone pairs form tight clusters.

---

## ✨ Highlights

✅ **LLM Summaries**: Summaries provide an interpretable and powerful way to describe code semantics.
✅ **Semantic Embeddings**: Instead of comparing raw syntax, you compare meaning captured in natural language.
✅ **Synthetic Data**: By generating clone/non-clone pairs, you can bootstrap training & evaluation without manual labeling.
✅ **Scalable Design**: Using Hugging Face Datasets’ batching allows you to efficiently process thousands of pairs.

---

## 📌 Notes

* **LLM Configuration**

  * The notebook loads `meta-llama/Llama-3.1-8B` directly, **without quantization**.
  * Summarization uses the Hugging Face `pipeline("text-generation")` interface.
  * The tokenizer is patched to set `pad_token_id` and `padding_side` for proper batching.

* **Batching**

  * Batching is implemented with `datasets.Dataset.map` for better GPU utilization.
  * Adjust `batch_size` (e.g., 4–16) based on your GPU memory.

* **Evaluation**

  * Since BigCloneBench provides only positive clone pairs, evaluation uses metrics like Recall; to incorporate precision/F1, you’d need negative (non-clone) pairs.

---

🚦 **Ready to start?**
Fire up `code_clone_detection.ipynb` and follow it cell by cell to:

* generate pairs,
* summarize,
* embed,
* classify,
* and visualize.

Happy clone hunting! 🚀