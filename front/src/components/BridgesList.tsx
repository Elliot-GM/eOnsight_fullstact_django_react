import React, { useState, useCallback, useEffect } from 'react';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import Modal from 'react-bootstrap/Modal';
import Bridge from '../models/bridge';
import { Link } from 'react-router-dom';

type SortConfig = {
    key: keyof Bridge | null;
    direction: 'ascending' | 'descending';
};

interface BridgeListProps {
    bridges: Bridge[];
    setBridges: React.Dispatch<React.SetStateAction<Bridge[]>>;
}

const BridgeList: React.FC<BridgeListProps> = ({ bridges, setBridges }) => {
    const [sortConfig, setSortConfig] = useState<SortConfig>({ key: 'id', direction: 'ascending' });
    const [currentPage, setCurrentPage] = useState<number>(1);
    const [itemsPerPage] = useState<number>(10);
    const [alert, setAlert] = useState<{ message: string, variant: string } | null>(null);
    const [showModal, setShowModal] = useState<boolean>(false);
    const [bridgeToDelete, setBridgeToDelete] = useState<number | null>(null);

    useEffect(() => {
        setSortConfig({ key: 'id', direction: 'ascending' });
    }, [bridges]);

    const requestSort = (key: keyof Bridge) => {
        let direction: 'ascending' | 'descending' = 'ascending';
        if (sortConfig.key === key && sortConfig.direction === 'ascending') {
            direction = 'descending';
        }
        setSortConfig({ key, direction });
    };

    const sortedBridges = React.useMemo(() => {
        let sortableBridges = [...bridges];
        if (sortConfig.key !== null) {
            sortableBridges.sort((a, b) => {
                if (a[sortConfig.key!] < b[sortConfig.key!]) {
                    return sortConfig.direction === 'ascending' ? -1 : 1;
                }
                if (a[sortConfig.key!] > b[sortConfig.key!]) {
                    return sortConfig.direction === 'ascending' ? 1 : -1;
                }
                return 0;
            });
        }
        return sortableBridges;
    }, [bridges, sortConfig]);

    const getClassNamesFor = (key: keyof Bridge) => {
        if (!sortConfig.key) return '';
        return sortConfig.key === key ? sortConfig.direction : '';
    };

    const totalItems = sortedBridges.length;
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentItems = sortedBridges.slice(indexOfFirstItem, indexOfLastItem);

    const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

    const handleDelete = useCallback(async () => {
        if (bridgeToDelete === null) return;

        try {
            const response = await fetch(`http://127.0.0.1:8000/bridge/${bridgeToDelete}/`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            setBridges(bridges.filter(bridge => bridge.id !== bridgeToDelete));
            setAlert({ message: 'Bridge deleted successfully!', variant: 'success' });
        } catch (error) {
            console.error('Error:', error);
            setAlert({ message: 'Error deleting bridge. Please try again.', variant: 'danger' });
        } finally {
            setShowModal(false);
        }
    }, [bridgeToDelete, bridges, setBridges]);

    return (
        <div>
            {alert && (
                <Alert variant={alert.variant} onClose={() => setAlert(null)} dismissible>
                    {alert.message}
                </Alert>
            )}
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th onClick={() => requestSort('id')} className={getClassNamesFor('id')}>
                            ID {sortConfig.key === 'id' ? (sortConfig.direction === 'ascending' ? '↑' : '↓') : ''}
                        </th>
                        <th onClick={() => requestSort('name')} className={getClassNamesFor('name')}>
                            Name {sortConfig.key === 'name' ? (sortConfig.direction === 'ascending' ? '↑' : '↓') : ''}
                        </th>
                        <th onClick={() => requestSort('latitude')} className={getClassNamesFor('latitude')}>
                            Latitude {sortConfig.key === 'latitude' ? (sortConfig.direction === 'ascending' ? '↑' : '↓') : ''}
                        </th>
                        <th onClick={() => requestSort('longitude')} className={getClassNamesFor('longitude')}>
                            Longitude {sortConfig.key === 'longitude' ? (sortConfig.direction === 'ascending' ? '↑' : '↓') : ''}
                        </th>
                        <th onClick={() => requestSort('inspection_date')} className={getClassNamesFor('inspection_date')}>
                            Inspection Date {sortConfig.key === 'inspection_date' ? (sortConfig.direction === 'ascending' ? '↑' : '↓') : ''}
                        </th>
                        <th onClick={() => requestSort('status')} className={getClassNamesFor('status')}>
                            Status {sortConfig.key === 'status' ? (sortConfig.direction === 'ascending' ? '↑' : '↓') : ''}
                        </th>
                        <th onClick={() => requestSort('traffic_load')} className={getClassNamesFor('traffic_load')}>
                            Traffic Load {sortConfig.key === 'traffic_load' ? (sortConfig.direction === 'ascending' ? '↑' : '↓') : ''}
                        </th>
                        <th>
                            Actions
                        </th>
                    </tr>
                </thead>
                <tbody>
                    {currentItems.map((bridge) => (
                        <tr key={bridge.id}>
                            <td>{bridge.id}</td>
                            <td>{bridge.name}</td>
                            <td>{bridge.latitude}</td>
                            <td>{bridge.longitude}</td>
                            <td>{new Date(bridge.inspection_date).toLocaleDateString()}</td>
                            <td>{bridge.status}</td>
                            <td>{bridge.traffic_load}</td>
                            <td>
                                <Button variant="primary" size="sm" href={`/bridge/${bridge.id}`}>
                                    Edit
                                </Button>
                                {' '}
                                <Button variant="danger" size="sm" onClick={() => { setBridgeToDelete(bridge.id); setShowModal(true); }}>
                                    Delete
                                </Button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '10px' }}>
                <Button variant="secondary" size="sm" onClick={() => paginate(currentPage - 1)} disabled={currentPage === 1} style={{ margin: '0 5px' }}>
                    Previous
                </Button>{' '}
                <Button variant="secondary" size="sm" onClick={() => paginate(currentPage + 1)} disabled={indexOfLastItem >= sortedBridges.length} style={{ margin: '0 5px' }}>
                    Next
                </Button>{' '}
                <span style={{ margin: '0 5px' }}> Page {currentPage} of {totalPages} </span>{' '}
                <Link to="/add-bridge" style={{ margin: '0 5px' }}>
                    <Button variant='primary'>
                        Add Bridge
                    </Button>
                </Link>
            </div>

            <Modal show={showModal} onHide={() => setShowModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Confirm Delete</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Are you sure you want to delete this bridge?
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowModal(false)}>
                        Cancel
                    </Button>
                    <Button variant="danger" onClick={handleDelete}>
                        Delete
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
};

export default BridgeList;

