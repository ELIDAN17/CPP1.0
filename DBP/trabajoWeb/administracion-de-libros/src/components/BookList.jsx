import React, { useContext } from 'react';
import { BooksContext } from '../context/BooksContext';
import { Table, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

function BookList() {
  const { books, deleteBook } = useContext(BooksContext);
  const navigate = useNavigate(); // <--- CAMBIO AQUÍ (navigate)

  const handleEdit = (id) => {
    navigate(`/edit/${id}`); // <--- CAMBIO AQUÍ (navigate)
  };

  return (
    <div>
      <h2>Book List</h2>
      {books.length === 0 ? (
        <p>No books available. Add some!</p>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Title</th>
              <th>Author</th>
              <th>ISBN</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {books.map((book) => (
              <tr key={book.id}>
                <td>{book.title}</td>
                <td>{book.author}</td>
                <td>{book.isbn}</td>
                <td>
                  <Button
                    variant="warning"
                    size="sm"
                    className="me-2"
                    onClick={() => handleEdit(book.id)}
                  >
                    Edit
                  </Button>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => deleteBook(book.id)}
                  >
                    Delete
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </div>
  );
}

export default BookList;