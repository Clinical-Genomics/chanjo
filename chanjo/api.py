from flask import Flask, jsonify
from sql import ElementAdapter
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

app = Flask(__name__)
adapter = ElementAdapter("tests/data/CCDS_test.db")

def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):

  if methods is not None:
    methods = ', '.join(sorted(x.upper() for x in methods))
  if headers is not None and not isinstance(headers, basestring):
    headers = ', '.join(x.upper() for x in headers)
  if not isinstance(origin, basestring):
    origin = ', '.join(origin)
  if isinstance(max_age, timedelta):
    max_age = max_age.total_seconds()

  def get_methods():
    if methods is not None:
      return methods

    options_resp = current_app.make_default_options_response()
    return options_resp.headers['allow']

  def decorator(f):
    def wrapped_function(*args, **kwargs):
      if automatic_options and request.method == 'OPTIONS':
        resp = current_app.make_default_options_response()
      else:
        resp = make_response(f(*args, **kwargs))
      if not attach_to_all and request.method != 'OPTIONS':
        return resp

      h = resp.headers

      h['Access-Control-Allow-Origin'] = origin
      h['Access-Control-Allow-Methods'] = get_methods()
      h['Access-Control-Max-Age'] = str(max_age)
      if headers is not None:
        h['Access-Control-Allow-Headers'] = headers
      return resp

    f.provide_automatic_options = False
    return update_wrapper(wrapped_function, f)
  return decorator

# =============================================================================
#   Routes
# -----------------------------------------------------------------------------
@app.route("/genes")
@crossdomain(origin='*')
def genes():
  genes = adapter.get("gene")[:20]

  res = {
    "genes": [gene.toDict() for gene in genes]
  }

  return jsonify(**res)

@app.route("/genes/<gene_id>")
@crossdomain(origin='*')
def gene(gene_id):
  gene = adapter.get("gene", gene_id)

  res = {
    "gene": gene.toDict(),
    "transcripts": [tx.toDict() for tx in gene.transcripts],
    "exons": [ex.toDict() for ex in gene.exons]
  }

  return jsonify(**res)

@app.route("/transcripts/<tx_id>")
@crossdomain(origin='*')
def transcripts(tx_id):
  tx = adapter.get("transcript", tx_id)

  res = {
    "transcript": tx.toDict(),
    "gene": tx.gene.toDict(),
    "exons": [ex.toDict() for ex in tx.exons]
  }

  return jsonify(**res)

@app.route("/exons/<exon_id>")
@crossdomain(origin='*')
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