from .model import db, Topic

app = Flask(__name__)
app.config.from_pyfile('../default.cfg')
db.init_app(app)

@app.route("/")
def root():
    topics = Topic.query.all()
    return render_template('index.html', topics=topics)


@app.route('/topic/<int:topic_id>')
def topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    return render_template('topic.html', topic=topic)

@app.route("/topic/new")
def write_topic():
    return render_template('write.html')

