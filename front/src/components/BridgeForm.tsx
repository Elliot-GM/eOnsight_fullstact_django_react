import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Form, Button, Container, Modal } from 'react-bootstrap';
import createWKB from '../tools/createWKB';
import parseWKB from '../tools/parseWKB';

const defaultBridge = {
    name: '',
    latitude: 0,
    longitude: 0,
    inspection_date: '',
    status: 'Good',
    traffic_load: 0,
};

const BridgeForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    const [bridge, setBridge] = useState(defaultBridge);
    const [tmpBridge, setTmpBridge] = useState(defaultBridge);
    
    const [showCancelModal, setShowCancelModal] = useState(false);
    const [showSaveModal, setShowSaveModal] = useState(false);
    const [alertMessage, setAlertMessage] = useState('');
    const [showAlert, setShowAlert] = useState(false);

    useEffect(() => {
        if (id) {
            const fetchBridge = async () => {
                try {
                    const response = await fetch(`http://127.0.0.1:8000/bridge/${id}/`);
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    const data = await response.json();
                    const { latitude, longitude } = parseWKB(data.location);
                    const bridgeData = {
                        name: data.name,
                        location: data.location,
                        latitude: latitude,
                        longitude: longitude,
                        inspection_date: data.inspection_date,
                        status: data.status,
                        traffic_load: data.traffic_load,
                    };
                    setBridge(bridgeData);
                    setTmpBridge(bridgeData);
                } catch (error) {
                    console.error('Error fetching bridge:', error);
                }
            };

            fetchBridge();
        }
    }, [id]);

    const handleChange = (e:any) => {
        const { name, value } = e.target;
        setBridge({
            ...bridge,
            [name]: value,
        });
    };

    const handleSave = async () => {
        const bridgeData = {
            name: bridge.name,
            location: createWKB(bridge.longitude, bridge.latitude),
            inspection_date: bridge.inspection_date,
            status: bridge.status,
            traffic_load: bridge.traffic_load,
        };

        try {
            const method = id ? 'PUT' : 'POST';
            const url = id ? `http://127.0.0.1:8000/bridge/${id}/` : 'http://127.0.0.1:8000/bridges/';
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(bridgeData),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            setAlertMessage(id ? 'Changes saved successfully!' : 'Bridge added successfully!');
            setShowAlert(true);
            navigate(`/bridge/${id || data.id}`);
        } catch (error) {
            setAlertMessage('Error saving changes. Please try again.');
            setShowAlert(true);
        } finally {
            setShowSaveModal(false);
        }
    };

    const handleSubmit = (e:any) => {
        e.preventDefault();
        setShowSaveModal(true);
    };

    const handleCancel = () => {
        setShowCancelModal(true);
    };

    return (
        <Container>
            <h2>{id ? 'Edit Bridge' : 'Add New Bridge'}</h2>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formName">
                    <Form.Label>Name</Form.Label>
                    <Form.Control
                        type="text"
                        name="name"
                        value={bridge.name}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>
                <Form.Group controlId="formLatitude">
                    <Form.Label>Latitude</Form.Label>
                    <Form.Control
                        type="number"
                        name="latitude"
                        value={bridge.latitude}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>
                <Form.Group controlId="formLongitude">
                    <Form.Label>Longitude</Form.Label>
                    <Form.Control
                        type="number"
                        name="longitude"
                        value={bridge.longitude}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>
                <Form.Group controlId="formInspectionDate">
                    <Form.Label>Inspection Date</Form.Label>
                    <Form.Control
                        type="date"
                        name="inspection_date"
                        value={bridge.inspection_date}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>
                <Form.Group controlId="formStatus">
                    <Form.Label>Status</Form.Label>
                    <Form.Control
                        as="select"
                        name="status"
                        value={bridge.status}
                        onChange={handleChange}
                        required
                    >
                        <option value="Good">Good</option>
                        <option value="Fair">Fair</option>
                        <option value="Poor">Poor</option>
                        <option value="Bad">Bad</option>
                    </Form.Control>
                </Form.Group>
                <Form.Group controlId="formTrafficLoad">
                    <Form.Label>Traffic Load</Form.Label>
                    <Form.Control
                        type="number"
                        name="traffic_load"
                        value={bridge.traffic_load}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '10px' }}>
                    {id && (
                        <Button variant="warning" onClick={handleCancel} style={{ margin: '0 5px' }}>
                            Cancel Edit
                        </Button>
                    )}
                    <Button variant="primary" type="submit" style={{ margin: '0 5px' }}>
                        {id ? 'Save Changes' : 'Add Bridge'}
                    </Button>
                </div>
            </Form>

            <Modal show={showCancelModal} onHide={() => setShowCancelModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Cancel Edit</Modal.Title>
                </Modal.Header>
                <Modal.Body>Are you sure you want to discard the changes?</Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowCancelModal(false)}>
                        Close
                    </Button>
                    <Button variant="danger" onClick={() => {
                        setBridge(tmpBridge);
                        setShowCancelModal(false);
                    }}>
                        Discard Changes
                    </Button>
                </Modal.Footer>
            </Modal>

            <Modal show={showSaveModal} onHide={() => setShowSaveModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Confirm Save</Modal.Title>
                </Modal.Header>
                <Modal.Body>Are you sure you want to save the changes?</Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowSaveModal(false)}>
                        Close
                    </Button>
                    <Button variant="primary" onClick={handleSave}>
                        Save Changes
                    </Button>
                </Modal.Footer>
            </Modal>

            {showAlert && (
                <div className="mt-3">
                    <div className={`alert ${alertMessage.includes('Error') ? 'alert-danger' : 'alert-success'}`} role="alert">
                        {alertMessage}
                    </div>
                </div>
            )}
        </Container>
    );
};

export default BridgeForm;
