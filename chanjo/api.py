from flask import Flask, jsonify
from sql import ElementAdapter

app = Flask(__name__)
adapter = ElementAdapter("tests/data/CCDS_test.db")

@app.route("/genes/<gene_id>")
def genes(gene_id):
  gene = adapter.get("gene", gene_id)

  res = {
    "gene": gene.toDict(),
    "transcripts": [tx.toDict() for tx in gene.transcripts],
    "exons": [ex.toDict() for ex in gene.exons]
  }

  return jsonify(**res)

@app.route("/transcripts/<tx_id>")
def transcripts(tx_id):
  tx = adapter.get("transcript", tx_id)

  res = {
    "transcript": tx.toDict(),
    "gene": tx.gene.toDict(),
    "exons": [ex.toDict() for ex in tx.exons]
  }

  return jsonify(**res)

@app.route("/exons/<exon_id>")
def exons(exon_id):
  exon = adapter.get("exon", exon_id)

  res = {
    "exon": exon.toDict(),
    "genes": [gene.toDict() for gene in exon.genes],
    "transcripts": [tx.toDict() for tx in exon.transcripts]
  }

  return jsonify(**res)

if __name__ == "__main__":
    app.run(debug=True)