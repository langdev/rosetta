from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html', topics=[])

@app.route("/topic/<int:topic_id>")
def topic(topic_id):
    topic = None
    return render_template('topic.html', topic=topic)

@app.route("/topic/new")
def write_topic():
    return render_template('write.html')

if __name__ == "__main__":
    app.run(debug=True)
