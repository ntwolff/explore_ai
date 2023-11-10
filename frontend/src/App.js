import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Form, Button, ListGroup } from 'react-bootstrap';
import axios from 'axios';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Moment from 'react-moment';

function App() {
  const [input, setInput] = useState('');
  const [thread, setThread] = useState([]);

  useEffect(() => {
    // TODO: Fetch the existing thread history (if needed)
  }, []);

  const handleInputChange = (event) => {
    setInput(event.target.value);
  };

  const handleSendClick = () => {
    axios.post('http://localhost:5000/interact', { input })
      .then(response => {
        // Update local thread state with the new message
        setThread([...thread, { role: 'user', content: input, timestamp: new Date() }, response.data]);
        setInput('');  // Clear the input after sending
      })
      .catch(error => console.error('Error:', error));
  };

  const handleFileUpload = (event) => {
    const formData = new FormData();
    formData.append('file', event.target.files[0]);

    axios.post('http://localhost:5000/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then(response => {
      // Logic to handle successful file upload
      // Possibly send a message indicating the file was uploaded
      console.log(response.data);
    })
    .catch(error => console.error('Error:', error));
  };

  return (
    <Container>
      <Row>
        <Col>
          <Form>
            <Form.Group>
              <Form.Control type="text" placeholder="Type your message..." onChange={handleInputChange} value={input} />
            </Form.Group>
            <Button variant="primary" onClick={handleSendClick}>Send</Button>
            <Form.File label="Upload File" onChange={handleFileUpload} />
          </Form>
        </Col>
      </Row>
      <Row>
        <Col>
          <ListGroup>
            {thread.map((message, index) => (
              <ListGroup.Item key={index}>
                <strong>{message.role}:</strong> {message.content}
                <div><small><Moment fromNow>{message.timestamp}</Moment></small></div>
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Col>
      </Row>
    </Container>
  );
}

export default App;