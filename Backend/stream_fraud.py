@app.route("/api/stream-fraud", methods=["GET"])
def stream_fraud():
    # Return last 10 flagged transactions as JSON
    return jsonify(flagged_transactions[-10:])
